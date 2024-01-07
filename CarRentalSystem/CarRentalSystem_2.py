class Samochod:
    def __init__(self, rejestracja, marka, model, rok, cena_za_dzien, dostepny=True):
        self.rejestracja = rejestracja
        self.marka = marka
        self.model = model
        self.rok = rok
        self.cena_za_dzien = cena_za_dzien
        self.dostepny = dostepny

    def __str__(self):
        dostepnosc = 'dostępny' if self.dostepny else 'niedostępny'
        return f"{self.rejestracja} {self.marka} {self.model} ({self.rok}) - {self.cena_za_dzien} zł/dzień, Status: {dostepnosc}"

class Klient:
    def __init__(self, nazwisko, imie, numer_telefonu):
        self.nazwisko = nazwisko
        self.imie = imie
        self.numer_telefonu = numer_telefonu
        self.wypozyczenia = []  # Lista wypożyczeń dla klienta

    def __str__(self):
        return f"{self.nazwisko}, tel: {self.numer_telefonu}, Wypożyczenia: {len(self.wypozyczenia)}"


class Wypozyczenie:
    def __init__(self, samochod, klient, data_rozpoczecia, data_zakonczenia):
        self.samochod = samochod
        self.klient = klient
        self.data_rozpoczecia = data_rozpoczecia
        self.data_zakonczenia = data_zakonczenia
        self.samochod.dostepny = False
        self.klient.wypozyczenia.append(self)

    def __str__(self):
        return f"Wypożyczenie: {self.samochod} dla {self.klient} od {self.data_rozpoczecia} do {self.data_zakonczenia}"

class Wypozyczalnia:
    def __init__(self):
        self.samochody = []
        self.klienci = []
        self.wypozyczenia = []

    # Metody do obsługi nowych funkcji...

    def dodaj_nowe_wypozyczenie(self):
        # Implementacja dodawania nowego wypożyczenia
        pass

    def przyjmij_zwrot(self):
        # Implementacja przyjmowania zwrotu samochodu
        pass

    def pokaz_status_samochodow(self):
        for samochod in self.samochody:
            print(samochod)

    def pokaz_status_klientow(self):
        for klient in self.klienci:
            print(klient)

    def dodaj_samochod_do_garazu(self, samochod):
        self.samochody.append(samochod)
        print(f"Dodano samochód: {samochod}")

    def usun_samochod_z_garazu(self, identyfikator):
        # identyfikator może być np. rejestracją lub indeksem samochodu
        pass

    def dodaj_samochod_do_garazu(self, rejestracja, marka, model, rok, cena_za_dzien):
        # Sprawdź, czy samochód o tej rejestracji już istnieje w garażu
        if rejestracja in self.samochody:
            print(f"Samochód o rejestracji {rejestracja} już istnieje w garażu.")
            return
        
        # Tworzenie nowego obiektu Samochod
        nowy_samochod = Samochod(rejestracja, marka, model, rok, cena_za_dzien)
        self.samochody[rejestracja] = nowy_samochod
        print(f"Dodano samochód: {nowy_samochod}")
        
    def wczytaj_samochody_z_pliku(self, sciezka_do_pliku):
        with open(sciezka_do_pliku, 'r', encoding='utf-8') as plik:
            for linia in plik:
                dane = linia.strip().split(',')
                # Zakładamy, że plik zawiera linie w formacie:
                # rejestracja,marka,model,rok,cena_za_dzien,dostepnosc
                if len(dane) == 6:
                    rejestracja, marka, model, rok, cena_za_dzien, dostepnosc = dane
                    dostepny = dostepnosc.strip().lower() == 'dostępny'
                    samochod = Samochod(rejestracja, marka, model, int(rok), float(cena_za_dzien), dostepny)
                    self.samochody[rejestracja] = samochod
                else:
                    print(f"Nieprawidłowy format linii: {linia}")




def wyswietl_menu():
    print("1. Dodaj nowe wypożyczenie")
    print("2. Przyjęcie zwrotu samochodu")
    print("3. Pokaż status wszystkich samochodów")
    print("4. Pokaż status wszystkich klientów")
    print("5. Zakończ")

def glowna_petla(wypozyczalnia):
    while True:
        wyswietl_menu()
        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            wypozyczalnia.dodaj_nowe_wypozyczenie()
        elif wybor == "2":
            wypozyczalnia.przyjmij_zwrot()
        elif wybor == "3":
            wypozyczalnia.pokaz_status_samochodow()
        elif wybor == "4":
            wypozyczalnia.pokaz_status_klientow()
        elif wybor == "5":
            print("Zakończenie programu.")
            break
        else:
            print("Nieprawidłowy wybór.")

            
if __name__ == "__main__":
    wypozyczalnia = Wypozyczalnia()
    wypozyczalnia.wczytaj_samochody_z_pliku('samochody.txt')
    # Tutaj możesz wywołać główną pętlę programu lub inne funkcje


