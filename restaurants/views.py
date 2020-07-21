from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
# obiekt F sluzy do odwolywania sie do pol i do kolumn w zapytaniu, jest jeszcze obiekt Q
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, FormView
import googlemaps

from .forms import AddressForm, OrderEntryForm
from .models import Restaurant, Course, Order, OrderEntry


class MainPage(TemplateView):
    template_name = 'restaurants/main_page.html'
    extra_context = {
        'title': "Najlepsze jedzenie",
        'form': AddressForm(),
    }


class AllRestaurants(ListView):
    # context object name ustawia nam nazwe wynikow, pod ktora nazwa one trafiaja do templates
    context_object_name = 'restaurants'

    paginate_by = 4
    template_name = 'restaurants/all.html'

    def get_context_data(self, **kwargs):
        context = {
            'title': "Restauracje w Twojej okolicy",
            'address': self.address,
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_coordinates(self):
        client = googlemaps.Client(
            key=settings.GMAPS_KEY)
        geocode_results = client.geocode(self.address)
        if geocode_results:
            return (
                geocode_results[0]['geometry']['location']['lat'],
                geocode_results[0]['geometry']['location']['lng'],
            )
        return None, None
# adnotacja - dodaje wirtualna kolumne do naszego wyniku

    def get_queryset(self):

        qs = Restaurant.objects.all().prefetch_related(
            'cuisines')  # redukuje z n+1 do 1+1 -
        # zapytanie o restauracje i osobne zapytanie ktore pobiera nam wszystkie kuchnie

        if self.address:
            lat, lng = self.get_coordinates()
            if lat and lng:
                complex_F = (
                    (F('latitude') - lat) ** 2
                    +
                    (F('longitude') - lng) ** 2
                ) ** 0.5
                return qs.annotate(
                    distance=complex_F, delivery_cost=F('distance')*1000
                ).order_by('distance')
                Restaurant.objects.annotate(
                    distance=complex_F).order_by('distance')
        return qs

    def get_ordering(self):
        return self.request.GET.get('o', 'name')

    def get(self, request, *args, **kwargs):
        self.address = request.GET.get('address', '')
        return super().get(request, *args, **kwargs)


# pk_url_kwarg zbiera argumenty z url tutaj musimy je umiscic


class RestaurantDetails(DetailView):
    # w szablonie musze sie odwolywac do tego name i bedzie to moj obiekt
    context_object_name = "restaurant"
    pk_url_kwarg = 'restaurant_id'
    queryset = Restaurant.objects.all()
    template_name = 'restaurants/details.html'

    # self.object przechowuje OBIEKT sciagniety z bazy danych przez widok
    def get_context_data(self, **kwargs):
        context = {
            'title': self.object.name,
        }
        context.update(kwargs)
        return super().get_context_data(**context)

# sesja - cos w stylu slownika - dostep do tej sesji odbywa sie poprzez
# obiekt request request.session


def add_to_card(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if 'cart' not in request.session:
        request.session['cart'] = list()
    # pk -primary_key to to samo co id, mozemy uzywac ich zamiennie,
    # id wystepuje w nazwie kolumny w bazie danych, ale django zpopularyzowal
    # pk
    request.session['cart'].append(course.pk)
    # tutaj musimy podac true zeby django wykrylo zmiane w obiekcie sesji
    request.session.modified = True
    messages.success(request, f'Dodano "{course}" do koszyka')

    if 'next' in request.GET:
        return redirect(request.GET['next'])
    return redirect('restaurants:all')


def cart(request):
    cart = []
    order_amount = 0
    if 'cart' in request.session:
        course_set = set(request.session['cart'])
        # wyciagamy wszystkie dania po id do tego sluzy to pk__in
        qs = Course.objects.filter(
            pk__in=course_set).select_related('restaurant')
        # n+1 zapytanie - zeby uniknac tego ze przy kazdej restauracji przechodzimy przez wszystkie dania przy zapytaniu,
        # ustawiamy joina, i wybieramy tylko to co nas interesuje - z relacji foreign_key pobiera nam obiekty,
        # zebysmy ich nie musieli pozyskiwac osobnymi zaputaniami

        for course in qs:
            x = request.session['cart'].count(
                course.pk)
            cart.append(
                {
                    # dajemy restaurant_set.first() -pierwsza opcja - bo danie tworzymy do restauracji a nie zeby jedno danie bylo w kilku restauracjach na raz
                    # to jest nasz foreign_key - dlatego wskazujemy ze ma szukac tylko po course.restaurant - dziala to tylko
                    # przy foreign_key , przy relacji M2M ustawiamy prefetch_related
                    'restaurant': course.restaurant,
                    'course': course,
                    'quantity': x,
                    'amount': x * course.price,
                }
            )
            order_amount += x * course.price
    context = {
        "title": "Koszyk",
        "cart": cart,
        'order_amount': order_amount,
    }
    return render(request, 'restaurants/cart.html', context)

# formset_factory - fabryka ktora generuje nam obiekty


class CreateOrder(LoginRequiredMixin, FormView):
    form_class = formset_factory(OrderEntryForm, extra=0)
    success_url = '/'
    template_name = 'restaurants/create_order.html'

    # metoda dispatch wczytuje sie na samym poczatku
    # i mozemy sobie tu pobierac dane ktore nam potrzebne z bazy danych, jak np ten adres
    def dispatch(self, request, *args, **kwargs):
        self.address = request.GET.get('address', '')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'title': 'Złóż zamówienie',
            'address': self.address,
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_initial(self):
        cart = []
        if 'cart' in self.request.session:
            course_set = set(self.request.session['cart'])
            qs = Course.objects.filter(
                pk__in=course_set)

        for course in qs:
            x = self.request.session['cart'].count(
                course.pk)
            cart.append(
                {
                    'course': course,
                    'quantity': x,
                }
            )

        return cart

    def form_valid(self, form):
        # w cleaned_data jest przechowywana lista słowników z danymi z formularza
        order = Order(
            user=self.request.user,
            amount=sum([x['course'].price * x['quantity']
                        for x in form.cleaned_data]),
            delivery_cost=0,
            delivery=self.address,
        )
        order.save()
        order_entries = [
            OrderEntry(
                order=order, course=entry['course'], quantity=entry['quantity'])
            for entry in form.cleaned_data
        ]
        # zamiast n zapytan bulk tworzy nam jedno - bulk create - utworz wiele
        OrderEntry.objects.bulk_create(order_entries)
        messages.success(self.request, 'Złożono zamówienie')
        # czysci cala sesje- czyli caly slownik danego uzytkownika, zarazem wylogowyhe tez uzytkownika z sesji
        # self.request.session.flush()
        # w ten sposob usuniemy tylko koszyk:
        del self.request.session['cart']
        # lub funkcja clear() ktora czysci caly koszyk, ale nie wylogowuje
        return super().form_valid(form)
