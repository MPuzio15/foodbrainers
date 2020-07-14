from django.db import models
from django.contrib.auth.models import User


class Cuisine(models.Model):
    name = models.CharField(max_length=20)
    # bedziemy widziec nasza kuchnie w panelu admina

    def __str__(self):
        return self.name


# w przypadku stringa nie pozwalamy na wartosc null przy liczbie mozemy podac null=True- baza danych zrozumie,
# ze jest mozliwosc podawania wartosci null
# musimy podac relacje do kuchni
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    # dlugosc i szerokosc geograficzna
    latitude = models.FloatField()
    longitude = models.FloatField()
    # bedzie przechowywalo relacje do wielu kuchni
    # manyToMany - pole many to many fields,
    # pozwala nam przypisac kilka kuchni do restauracji i kilka restauracji do kuchni
    # trzymane jest to w tabeli pośredniczącej, łączącej ze sobą dane z dwóch modeli
    # gdybysmy chcieli zapisywac wiecej informacji w tej tabeli posredniczacej, tak jak w przypadku
    # orderEntry dodalismy quantity - kolumne dodatkowa - zeby to dodac musimy stworzyc sobie parametr
    # throught="nazwaKlasy", ktora sami musimy stworzyc
    cuisines = models.ManyToManyField(Cuisine)
    logo = models.ImageField(upload_to="logo", null=True, blank=True)
    opening_hours = models.CharField(max_length=20)
    min_order_amount = models.PositiveIntegerField(default=0)
    # delivery_cost -> calculable

    # menu = models.ManyToManyField(
    #     "Course", blank=True, related_name='restaurant_set')  # powstanie tu wirtualne pole restaurant_set

    # podajemy "" bo klasa Course jest tworzona pozniej -Django zrozumie go jak juz ten model bedzie dostepny

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.PositiveIntegerField()
    is_spicy = models.BooleanField()
    is_vegan = models.BooleanField()
    is_glutenfree = models.BooleanField()
    # related_name='courses')
    restaurant = models.ForeignKey(
        Restaurant, null=True,  on_delete=models.CASCADE, related_name='menu')

    def __str__(self):
        return self.name


class Order(models.Model):
    # relacja jeden do wielu bo jeden user moze zamowic kilka dan z roznych restauracji
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    courses = models.ManyToManyField(Course, through='OrderEntry')
    amount = models.PositiveIntegerField(default=0)
    delivery_cost = models.PositiveIntegerField(default=0)
    delivery = models.CharField(max_length=50)


# tabela posredniczaca - musimy miec dwa pola, ktore wskazuja na lewo i prawo czyli musimy miec oba pole
# miedzy ktorymi chcemy stworzyc dodatkowa relacje
# i to quantity w tym przypadku to bedzie dodatkowa kolumna ktora sobie stworzymy dla tej relacji
class OrderEntry(models.Model):
    # orderEntry posredniczy miedzy Order i Course
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
