from django.urls import path

from . import views

app_name = "restaurants"

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('all/', views.AllRestaurants.as_view(), name='all'),
    path('restaurants/<int:restaurant_id>',
         views.RestaurantDetails.as_view(), name='details'),
    path('add_to_card/<int:course_id>', views.add_to_card, name='add_to_card'),
    path('cart/', views.cart, name='cart'),
    path('create_order/', views.CreateOrder.as_view(), name='create_order'),
    path('signup/', views.signup, name='signup'),
]

# widok funkcyjny- funkcja ktora django wywoluje z parametrami, dlatego podajemy
# tylko referencje, a nie wywolujemy, w przypadku widokow klasowych  dodajemy asView(),
#  ktora przeksztalca klase w widok
