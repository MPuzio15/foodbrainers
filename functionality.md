# Foodbrainers

1. Tworzenie konta i logowanie - my uzyjemy django.contrib.auth
2. Kategorie kuchni 
3. Lista restauracji - widok pojedynczej restauracji
    * twoje miasto
    * dane geolokalizacyjne
    * kuchnia (mozliwych kilka)
    * nazwa, 
    * logo (?), 
    * godziny otwarcia
    * opis
    * minimalna kwota zamówienia 
    * koszt dostawy -> wyliczalny
    * menu (wskazanie na produkty)
4. Danie:
    * nazwa
    * cena
    * opis - rowniez alergeny
    * czy ostre, bezglutenowe, wegetarianskie, weganskie
5. Koszyk z zamowieniem
* wybieranie pozycji z menu i dodawanie do koszyka
* relacja uzytkownika z produktami 

Widoki:
1. główny widok z polem adresu
2. widok wszystkich restauracji dla danego adresu z mozliwoscia filtrowania
3. widok pojedynczej restauracji