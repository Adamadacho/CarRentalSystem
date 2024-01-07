import os
from datetime import datetime

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
    def __init__(self, samochod, klient, data_rozpoczecia, data_zakonczenia, koszt):
        self.samochod = samochod
        self.klient = klient
        self.data_rozpoczecia = data_rozpoczecia
        self.data_zakonczenia = data_zakonczenia
        self.koszt = koszt
        self.samochod.dostepny = False
        self.klient.wypozyczenia.append(self)

    def __str__(self):
        return f"Wypożyczenie: {self.samochod} dla {self.klient} od {self.data_rozpoczecia} do {self.data_zakonczenia} koszt {self.koszt}"

class Wypozyczalnia:
    def __init__(self):
        self.samochody = []
        self.klienci = []
        self.wypozyczenia = []

def wyswietl_aktualne_wypozyczenia():
    try:
        with open('aktualneWypozyczenia.txt', 'r') as plik:
            wypozyczenia = plik.readlines()
            if not wypozyczenia:
                print("Brak aktualnych wypożyczeń.")
            else:
                for wiersz in wypozyczenia:
                    print(wiersz.strip())  # Usuwa znaki końca linii
    except FileNotFoundError:
        print("Plik 'aktualneWypozyczenia.txt' nie istnieje.")
    except Exception as e:
        print(f"Wystąpił błąd podczas odczytu pliku: {e}")

def wczytaj_klientow(nazwa_pliku):
    klienci = {}
    if os.path.exists(nazwa_pliku):
        with open(nazwa_pliku, 'r') as plik:
            for linia in plik:
                nazwisko, imie, numer_telefonu, licznik = linia.strip().split(',')
                klienci[(nazwisko, imie, numer_telefonu)] = int(licznik)
    return klienci

def zapisz_klientow(klienci, nazwa_pliku):
    with open(nazwa_pliku, 'w') as plik:
        for (nazwisko, imie, numer_telefonu), licznik in klienci.items():
            plik.write(f"{nazwisko},{imie},{numer_telefonu},{licznik}\n")

def oblicz_liczbe_dni(data_rozpoczecia, data_zakonczenia):
    # Format daty, np. 'YYYY-MM-DD'
    format_daty = "%Y-%m-%d"  
    rozpoczecie = datetime.strptime(data_rozpoczecia, format_daty)
    zakonczenie = datetime.strptime(data_zakonczenia, format_daty)
    roznica = zakonczenie - rozpoczecie
    return roznica.days

def dodaj_nowe_wypozyczenie(Wypozyczalnia):
    # 1. Zebranie informacji o kliencie
    nazwisko = input("Podaj nazwisko: ")
    imie = input("Podaj imię: ")
    numer_telefonu = input("Podaj numer telefonu: ")
    klient = Klient(nazwisko, imie, numer_telefonu)
    wypozyczalnia.klienci.append(klient)  # Dodanie klienta do listy klientów

    # 2. Wyświetlenie listy dostępnych samochodów
    samochody = wczytaj_samochody('samochody.txt')  # Załóżmy, że ta funkcja zwraca listę obiektów Samochod
    print("Dostępne samochody:")
    for idx, samochod in enumerate(samochody):
        if samochod.dostepny:
            print(f"{idx + 1}. {samochod}")

    # 3. Wybór samochodu przez użytkownika
    try:
        numer_linii = int(input("Podaj numer linii wybranego samochodu: ")) - 1
        if numer_linii < 0 or numer_linii >= len(samochody):
            print("Nieprawidłowy numer linii.")
            return

        wybrany_samochod = samochody[numer_linii]
        if not wybrany_samochod.dostepny:
            print("Samochód o wybranym numerze linii nie jest dostępny.")
            return
    except ValueError:
        print("Podano nieprawidłowy numer. Proszę podać wartość liczbową.")
        return

    # 4. Zapytanie o ilość dni wypożyczenia
    data_rozpoczecia = input("Podaj datę rozpoczęcia wynajmu (YYYY-MM-DD): ")
    data_zakonczenia = input("Podaj datę zakończenia wynajmu (YYYY-MM-DD): ")
    dni_wypozyczenia = oblicz_liczbe_dni(data_rozpoczecia, data_zakonczenia)
    
    if dni_wypozyczenia <= 0:
        print("Data zakończenia musi być późniejsza niż data rozpoczęcia.")
        return  # Zwraca z funkcji, jeśli daty są nieprawidłowe

    
    # Zmiana statusu samochodu na niedostępny
    wybrany_samochod.dostepny = False
    
    # 5. Obliczenie kosztu
    koszt = dni_wypozyczenia * wybrany_samochod.cena_za_dzien
    print(f"Całkowity koszt wypożyczenia: {koszt} zł")
    
    # Zapisanie wypożyczenia
    wypozyczenie = Wypozyczenie(wybrany_samochod, klient, data_rozpoczecia, data_zakonczenia, koszt)
    wypozyczalnia.wypozyczenia.append(wypozyczenie)  # Dodanie wypożyczenia do listy

    # Dopisanie klienta do pliku "klienci.txt" lub aktualizacja licznika
    klienci = wczytaj_klientow('klienci.txt')
    klucz_klienta = (nazwisko, imie, numer_telefonu)
    if klucz_klienta in klienci:
        klienci[klucz_klienta] += 1
    else:
        klienci[klucz_klienta] = 1
    zapisz_klientow(klienci, 'klienci.txt')

    # 6. Aktualizacja pliku samochodów
    zaktualizuj_plik_samochodow(samochody, 'samochody.txt')
    
    zapisz_wypozyczenie_do_pliku(wypozyczenie, 'aktualneWypozyczenia.txt')

def wczytaj_samochody(nazwa_pliku):
    samochody = []
    with open(nazwa_pliku, 'r') as plik:
        for linia in plik:
            dane = linia.strip().split(',')
            if len(dane) < 6:  # Sprawdź, czy linia zawiera co najmniej 6 elementów
                continue  # Jeśli nie, pomiń tę linię i kontynuuj z następną
            samochod = Samochod(dane[0], dane[1], dane[2], int(dane[3]), float(dane[4]), dane[5].lower() == 'true')
            samochody.append(samochod)
    return samochody

def wczytaj_samochody2(nazwa_pliku):
    samochody = []
    with open(nazwa_pliku, 'r') as plik:
        for linia in plik:
            dane = linia.strip().split(',')
            if len(dane) == 6:  # Upewnij się, że linia ma 6 elementów
                samochody.append(dane)
    return samochody

def zaktualizuj_plik_samochodow(samochody, nazwa_pliku):
    with open(nazwa_pliku, 'w') as plik:
        for samochod in samochody:
            dostepnosc = 'true' if samochod.dostepny else 'false'
            linia = f"{samochod.rejestracja},{samochod.marka},{samochod.model},{samochod.rok},{samochod.cena_za_dzien},{dostepnosc}\n"
            plik.write(linia)
            
def zapisz_wypozyczenie_do_pliku(wypozyczenie, nazwa_pliku):
    with open(nazwa_pliku, 'a') as plik:  # Użyj trybu 'a' do dopisywania do pliku
        linia = f"{wypozyczenie.samochod.rejestracja},{wypozyczenie.klient.nazwisko},{wypozyczenie.klient.imie},{wypozyczenie.data_rozpoczecia},{wypozyczenie.data_zakonczenia}\n"
        plik.write(linia)
        
def zapisz_samochody(samochody, nazwa_pliku):
    with open(nazwa_pliku, 'w') as plik:
        for samochod in samochody:
            plik.write(','.join(samochod) + '\n')

def przyjmij_zwrot():
    try:
        with open('aktualneWypozyczenia.txt', 'r') as plik:
            wypozyczenia = plik.readlines()
        
        # Wyświetl wypożyczenia
        print("Aktualne wypożyczenia:")
        for idx, wypozyczenie in enumerate(wypozyczenia):
            print(f"{idx + 1}: {wypozyczenie.strip()}")

        # Wybór wypożyczenia do usunięcia
        nr_linii = int(input("Podaj numer linii wypożyczenia do usunięcia: ")) - 1
        
        # Usunięcie wypożyczenia
        if 0 <= nr_linii < len(wypozyczenia):
            wiersz_do_usuniecia = wypozyczenia.pop(nr_linii)
            numer_rejestracyjny = wiersz_do_usuniecia.split(',')[0]

            # Aktualizacja pliku wypożyczeń
            with open('aktualneWypozyczenia.txt', 'w') as plik:
                plik.writelines(wypozyczenia)
            
            # Znalezienie i aktualizacja statusu samochodu
            samochody = wczytaj_samochody2('samochody.txt')
            for samochod in samochody:
                if samochod[0] == numer_rejestracyjny:
                    samochod[5] = 'true'  # Zakładając, że ostatni element to status dostępności
                    break
            
            # Zapisanie zaktualizowanej listy samochodów
            zapisz_samochody(samochody, 'samochody.txt')

            print("Wypożyczenie zostało usunięte i status samochodu zaktualizowany.")
        else:
            print("Nieprawidłowy numer linii.")
            
    except FileNotFoundError:
        print("Plik 'aktualneWypozyczenia.txt' nie istnieje.")
    except ValueError:
        print("Wprowadzono nieprawidłową wartość. Proszę podać numer.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def wyswietl_status_klientow(nazwa_pliku_klienci):
    try:
        with open(nazwa_pliku_klienci, 'r') as plik:
            klienci = plik.readlines()
        
        if not klienci:
            print("Brak zarejestrowanych klientów.")
            return
        
        print("Status klientów:")
        for idx, klient in enumerate(klienci):
            nazwisko, imie, numer_telefonu, licznik_wypozyczen = klient.strip().split(',')
            print(f"{idx + 1}: {nazwisko} {imie}, Tel: {numer_telefonu}, Wypożyczenia: {licznik_wypozyczen}")
    
    except FileNotFoundError:
        print(f"Plik '{nazwa_pliku_klienci}' nie istnieje.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def wyswietl_status_samochodow(nazwa_pliku_samochody):
    try:
        with open(nazwa_pliku_samochody, 'r') as plik:
            samochody = plik.readlines()
        
        if not samochody:
            print("Brak samochodów w bazie danych.")
            return
        
        print("Status samochodów:")
        for idx, samochod in enumerate(samochody):
            dane = samochod.strip().split(',')
            if len(dane) < 6:
                continue  # Pomiń niekompletne rekordy
            rejestracja, marka, model, rok, cena_za_dzien, dostepny = dane
            dostepnosc = 'dostępny' if dostepny.lower() == 'true' else 'niedostępny'
            print(f"{idx + 1}: {marka} {model}, Rok: {rok}, Cena: {cena_za_dzien}zł/dzień, Status: {dostepnosc}")
    
    except FileNotFoundError:
        print(f"Plik '{nazwa_pliku_samochody}' nie istnieje.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


def wyswietl_menu():
    print("_______________________________________________________")
    print("CarRentalSystem by Adam Kublinski")
    print("")
    print("Menu:")
    print("1. Dodaj nowe wypożyczenie")
    print("2. Przyjęcie zwrotu samochodu")
    print("3. Pokaż aktualne wypożyczenia")
    print("4. Pokaż status klientów")
    print("5. Pokaż status samochodów")
    print("6. Zakończ")
    print("")

def glowna_petla(wypozyczalnia):
    while True:
        wyswietl_menu()
        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            dodaj_nowe_wypozyczenie(Wypozyczalnia)
        elif wybor == "2":
            przyjmij_zwrot()
        elif wybor == "3":
            wyswietl_aktualne_wypozyczenia()
        elif wybor == "4":
            wyswietl_status_klientow('klienci.txt')
        elif wybor == "5":
            wyswietl_status_samochodow('samochody.txt')
        elif wybor == "6":
            print("Zakończenie programu.")
            break
        else:
            print("Nieprawidłowy wybór.")

            
if __name__ == "__main__":
    wypozyczalnia = Wypozyczalnia()
    glowna_petla(Wypozyczalnia)



