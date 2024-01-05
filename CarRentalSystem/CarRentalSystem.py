
class Samochod:
    def __init__(self, marka, model, rok, cena_za_dzien):
        self.marka = marka
        self.model = model
        self.rok = rok
        self.cena_za_dzien = cena_za_dzien

    def __str__(self):
        return f"{self.marka} {self.model} ({self.rok}) - {self.cena_za_dzien} zl/dzien"

class Klient:
    def __init__(self, nazwisko, numer_telefonu):
        self.nazwisko = nazwisko
        self.numer_telefonu = numer_telefonu

    def __str__(self):
        return f"{self.nazwisko}, tel: {self.numer_telefonu}"

class Wypozyczenie:
    def __init__(self, samochod, klient, data_rozpoczecia, data_zakonczenia):
        self.samochod = samochod
        self.klient = klient
        self.data_rozpoczecia = data_rozpoczecia
        self.data_zakonczenia = data_zakonczenia

    def __str__(self):
        return f"Wypozyczenie: {self.samochod} dla {self.klient} od {self.data_rozpoczecia} do {self.data_zakonczenia}"

class Wypozyczalnia:
    def __init__(self):
        self.samochody = []
        self.klienci = []
        self.wypozyczenia = []

    def dodaj_samochod(self, samochod):
        self.samochody.append(samochod)

    def dodaj_klienta(self, klient):
        self.klienci.append(klient)

    def rejestruj_wypozyczenie(self, samochod, klient, data_rozpoczecia, data_zakonczenia):
        wypozyczenie = Wypozyczenie(samochod, klient, data_rozpoczecia, data_zakonczenia)
        self.wypozyczenia.append(wypozyczenie)
        print("Zarejestrowano wypozyczenie:", wypozyczenie)

    # Tutaj mo¿na dodaæ wiêcej metod, np. do wyszukiwania samochodów/klientów, wyœwietlania list, etc.

# Utworzenie instancji wypo¿yczalni
wypozyczalnia = Wypozyczalnia()

# Dodanie samochodów
wypozyczalnia.dodaj_samochod(Samochod("Toyota", "Corolla", 2020, 150))
wypozyczalnia.dodaj_samochod(Samochod("Ford", "Focus", 2019, 130))

# Dodanie klientów
wypozyczalnia.dodaj_klienta(Klient("Nowak", "123456789"))
wypozyczalnia.dodaj_klienta(Klient("Kowalski", "987654321"))

# Rejestracja wypo¿yczenia
wypozyczalnia.rejestruj_wypoz
