# import bibliotek
from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

# tworzenie list
dane_galerie = []
dane_wystawy = []
dane_dziela = []
dane_pracownicy = []
markers = []

#funkcja startowa
def start_app():
    def check_login(): # funkcja do logowania
        username = entry_username.get()
        password = entry_password.get()
        if (username == "admin" and password == "admin") or (username == "uzytkownik" and password == "uzytkownik"):
            login_window.destroy()
            manage_mode(username == "admin")

#utworzenie okna logowania
    login_window = Tk()
    login_window.geometry("300x200")
    login_window.title("Logowanie")

    login_window.configure(bg = "#D9B0DE")

    Label(login_window, text="Nazwa użytkownika:",bg="#D9B0DE").pack(pady=5)
    entry_username = Entry(login_window)
    entry_username.pack(pady=5)

    Label(login_window, text="Hasło:", bg="#D9B0DE").pack(pady=5)
    entry_password = Entry(login_window, show="*")
    entry_password.pack(pady=5)

    Button(login_window, text="Zaloguj", bg="#D9B0DE", command=check_login).pack(pady=10)
    login_window.mainloop()

#funkcja do zarządzania
def manage_mode(is_admin):
    root = Tk()
    root.geometry("1300x1000")
    root.title("EXHIBITION_MANAGE_API")

    root.configure(bg="#D9B0DE")

#funkcja do usuwania znaczników na mapie, wyszukiwanie po indeksie i
    def find_marker_index(object_name):
        for i, marker_data in enumerate(markers):
            if marker_data[0] == object_name:
                return i
        return -1

    def delete_marker_by_name(object_name):
        idx = find_marker_index(object_name)
        if idx != -1: #jeśli znajdzie marker o liczbie większej niż 0 lub 0 to zwraca marker jeżeli nie znajdzie to zwraca -1
            marker_obj = markers[idx][1]
            marker_obj.delete()
            del markers[idx] #usuniecie z listy

    ramka_mapa = Frame(root, padx=300, pady=30)
    ramka_mapa.grid(row=0, column=0, columnspan=2, sticky="nsew")

    ramka_mapa.configure(bg = "#D9B0DE")

    map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=800, height=400)
    map_widget.set_position(52.0, 21.0)
    map_widget.set_zoom(6)
    map_widget.pack(fill=BOTH, expand=True)

    def get_coordinates(location):
        url: str = f'https://pl.wikipedia.org/wiki/{location}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(',', '.')),
            float(response_html.select('.longitude')[1].text.replace(',', '.'))
        ]

# funkcja do okna otwierania galerii
    def open_galerie_window():
        window = Toplevel(root) #okno toplevel podrzędne względem root
        window.title("Galerie sztuki")

        window.configure(bg="#D9B0DE")

        def refresh_listbox():
            listbox_details.delete(0, END)
            for i, galeria in enumerate(dane_galerie):
                listbox_details.insert(
                    END,
                    f"{i+1}. [Nazwa: {galeria[0]}, Lokalizacja: {galeria[1]}]"
                )

        def show_details():
            refresh_listbox()

        def wprowadz_dane():
            nazwa = entry_nazwa.get().strip()
            lokalizacja = entry_lokalizacja.get().strip()
            if nazwa and lokalizacja:
                dane_galerie.append([nazwa, lokalizacja])
                entry_nazwa.delete(0, END)
                entry_lokalizacja.delete(0, END)
                refresh_listbox()


        def edytuj_dane():
            selection = listbox_details.curselection() #pobranie indeksu zaznaczzonej rzeczy
            if not selection:
                return
            index = selection[0] #pobieranie indeksu
            current = dane_galerie[index]
            old_name = current[0]
            new_nazwa = entry_nazwa.get().strip()
            new_lokalizacja = entry_lokalizacja.get().strip()
            if new_nazwa or new_lokalizacja:
                if new_nazwa:
                    delete_marker_by_name(old_name)
                    current[0] = new_nazwa
                if new_lokalizacja:
                    current[1] = new_lokalizacja
                entry_nazwa.delete(0, END)
                entry_lokalizacja.delete(0, END)
                refresh_listbox()

        def usun_dane():
            selection = listbox_details.curselection()
            if not selection:
                return
            index = selection[0]
            galeria_do_usuniecia = dane_galerie[index][0]
            delete_marker_by_name(galeria_do_usuniecia)
            dane_galerie.pop(index)
            refresh_listbox()

        frame_details = Frame(window,bg="#D9B0DE", padx=10, pady=10)
        frame_details.pack()
        Button(frame_details, text="Pokaż szczegóły", bg = "#B194BD", command=show_details).pack()
        listbox_details = Listbox(frame_details, width=80)
        listbox_details.pack()

        frame_data = Frame(window, padx=10, pady=10)
        frame_data.pack()
        Label(frame_data, text="Dane:").pack()
        Label(frame_data, text="Nazwa:").pack()
        entry_nazwa = Entry(frame_data)
        entry_nazwa.pack()
        Label(frame_data, text="Lokalizacja:").pack()
        entry_lokalizacja = Entry(frame_data)
        entry_lokalizacja.pack()

        button_frame = Frame(window, padx=10, pady=10)
        button_frame.pack()
        Button(button_frame, text="Wprowadź", bg = "#64C285", command=wprowadz_dane).pack(side=LEFT, padx=5)
        Button(button_frame, text="Edytuj",bg = "#B8AE45", command=edytuj_dane).pack(side=LEFT, padx=5)
        Button(button_frame, text="Usuń",bg = "#FF4043", command=usun_dane).pack(side=LEFT, padx=5)

    def open_wystawy_window():
        window = Toplevel(root)
        window.title("Wystawy")

        window.configure(bg="#D9B0DE")

        def refresh_listbox():
            listbox_details.delete(0, END)
            for i, wystawa in enumerate(dane_wystawy):
                listbox_details.insert(
                    END,
                    f"{i+1}. [Nazwa: {wystawa[0]}, Lokalizacja: {wystawa[1]}]"
                )

        def show_details():
            refresh_listbox()

        def wprowadz_dane():
            nazwa = entry_nazwa.get().strip()
            lokalizacja = entry_lokalizacja.get().strip()
            if nazwa and lokalizacja:
                dane_wystawy.append([nazwa, lokalizacja])
                entry_nazwa.delete(0, END)
                entry_lokalizacja.delete(0, END)
                refresh_listbox()

        def edytuj_dane():
            selection = listbox_details.curselection()
            if not selection:
                return
            index = selection[0]
            current = dane_wystawy[index]
            old_name = current[0]
            new_nazwa = entry_nazwa.get().strip()
            new_lokalizacja = entry_lokalizacja.get().strip()
            if new_nazwa or new_lokalizacja:
                if new_nazwa:
                    delete_marker_by_name(old_name)
                    current[0] = new_nazwa
                if new_lokalizacja:
                    current[1] = new_lokalizacja
                entry_nazwa.delete(0, END)
                entry_lokalizacja.delete(0, END)
                refresh_listbox()

        def usun_dane():
            selection = listbox_details.curselection()
            if not selection:
                return
            index = selection[0]
            wystawa_do_usuniecia = dane_wystawy[index][0]
            delete_marker_by_name(wystawa_do_usuniecia)
            dane_wystawy.pop(index)
            refresh_listbox()

        frame_details = Frame(window, bg="#D9B0DE", padx=10, pady=10)
        frame_details.pack()
        Button(frame_details, text="Pokaż szczegóły", bg = "#B194BD", command=show_details).pack()
        listbox_details = Listbox(frame_details, width=80)
        listbox_details.pack()

        frame_data = Frame(window, padx=10, pady=10)
        frame_data.pack()
        Label(frame_data, text="Dane:").pack()
        Label(frame_data, text="Nazwa:").pack()
        entry_nazwa = Entry(frame_data)
        entry_nazwa.pack()
        Label(frame_data, text="Lokalizacja:").pack()
        entry_lokalizacja = Entry(frame_data)
        entry_lokalizacja.pack()

        button_frame = Frame(window, padx=10, pady=10)
        button_frame.pack()
        Button(button_frame, text="Wprowadź",bg = "#64C285", command=wprowadz_dane).pack(side=LEFT, padx=5)
        Button(button_frame, text="Edytuj",bg = "#B8AE45", command=edytuj_dane).pack(side=LEFT, padx=5)
        Button(button_frame, text="Usuń",bg = "#FF4043", command=usun_dane).pack(side=LEFT, padx=5)

    def open_dziela_window():
        window = Toplevel(root)
        window.title("Dzieła")

        window.configure(bg="#D9B0DE")

        def refresh_listbox():
            listbox_details.delete(0, END)
            for i, dzielo_data in enumerate(dane_dziela):
                listbox_details.insert(
                    END,
                    f"{i+1}. [Tytuł: {dzielo_data[0]}, Autor: {dzielo_data[1]}, Miejsce: {dzielo_data[2]}]"
                )

        def show_details():
            refresh_listbox()

        def wprowadz_dane():
            tytul = entry_tytul.get().strip()
            autor = entry_autor.get().strip()
            powiazanie = entry_powiazanie.get().strip()
            if tytul and autor and powiazanie:
                dane_dziela.append([tytul, autor, powiazanie])
                entry_tytul.delete(0, END)
                entry_autor.delete(0, END)
                entry_powiazanie.delete(0, END)
                refresh_listbox()

        def edytuj_dane():
            selection = listbox_details.curselection()
            if not selection:
                return
            index = selection[0]
            current = dane_dziela[index]
            new_tytul = entry_tytul.get().strip()
            new_autor = entry_autor.get().strip()
            new_powiazanie = entry_powiazanie.get().strip()
            if new_tytul or new_autor or new_powiazanie:
                if new_tytul:
                    current[0] = new_tytul
                if new_autor:
                    current[1] = new_autor
                if new_powiazanie:
                    current[2] = new_powiazanie
                entry_tytul.delete(0, END)
                entry_autor.delete(0, END)
                entry_powiazanie.delete(0, END)
                refresh_listbox()

        def usun_dane():
            selection = listbox_details.curselection()
            if not selection:
                return
            index = selection[0]
            dane_dziela.pop(index)
            refresh_listbox()

        frame_details = Frame(window,bg="#D9B0DE",  padx=10, pady=10)
        frame_details.pack()
        Button(frame_details, text="Pokaż szczegóły", bg = "#B194BD", command=show_details).pack()
        listbox_details = Listbox(frame_details, width=80)
        listbox_details.pack()

        frame_data = Frame(window, padx=10, pady=10)
        frame_data.pack()
        Label(frame_data, text="Dane:").pack()
        Label(frame_data, text="Tytuł dzieła:").pack()
        entry_tytul = Entry(frame_data)
        entry_tytul.pack()
        Label(frame_data, text="Autor dzieła:").pack()
        entry_autor = Entry(frame_data)
        entry_autor.pack()
        Label(frame_data, text="Galeria sztuki lub Wystawa:").pack()
        entry_powiazanie = Entry(frame_data)
        entry_powiazanie.pack()

        button_frame = Frame(window, padx=10, pady=10)
        button_frame.pack()
        Button(button_frame, text="Wprowadź",bg = "#64C285", command=wprowadz_dane).pack(side=LEFT, padx=5)
        Button(button_frame, text="Edytuj",bg = "#B8AE45", command=edytuj_dane).pack(side=LEFT, padx=5)
        Button(button_frame, text="Usuń",bg = "#FF4043", command=usun_dane).pack(side=LEFT, padx=5)

    def open_pracownicy_window():
        window = Toplevel(root)
        window.title("Pracownicy")

        window.configure(bg="#D9B0DE")

        def refresh_listbox():
            listbox_details.delete(0, END)
            for i, pracownik in enumerate(dane_pracownicy):
                listbox_details.insert(
                    END,
                    f"{i+1}. [Imię: {pracownik[0]}, Nazwisko: {pracownik[1]}, Miejsce: {pracownik[2]}]"
                )

        def show_details():
            refresh_listbox()

        def wprowadz_dane():
            imie = entry_imie.get().strip()
            nazwisko = entry_nazwisko.get().strip()
            powiazanie = entry_powiazanie.get().strip()
            if imie and nazwisko and powiazanie:
                dane_pracownicy.append([imie, nazwisko, powiazanie])
                entry_imie.delete(0, END)
                entry_nazwisko.delete(0, END)
                entry_powiazanie.delete(0, END)
                refresh_listbox()

        def edytuj_dane():
            selection = listbox_details.curselection()
            if not selection:
                return
            index = selection[0]
            current = dane_pracownicy[index]
            new_imie = entry_imie.get().strip()
            new_nazwisko = entry_nazwisko.get().strip()
            new_powiazanie = entry_powiazanie.get().strip()
            if new_imie or new_nazwisko or new_powiazanie:
                if new_imie:
                    current[0] = new_imie
                if new_nazwisko:
                    current[1] = new_nazwisko
                if new_powiazanie:
                    current[2] = new_powiazanie
                entry_imie.delete(0, END)
                entry_nazwisko.delete(0, END)
                entry_powiazanie.delete(0, END)
                refresh_listbox()

        def usun_dane():
            selection = listbox_details.curselection()
            if not selection:
                return
            index = selection[0]
            dane_pracownicy.pop(index)
            refresh_listbox()

        frame_details = Frame(window,bg="#D9B0DE",  padx=10, pady=10)
        frame_details.pack()
        Button(frame_details, text="Pokaż szczegóły", bg = "#B194BD", command=show_details).pack()
        listbox_details = Listbox(frame_details, width=80)
        listbox_details.pack()

        frame_data = Frame(window, padx=10, pady=10)
        frame_data.pack()
        Label(frame_data, text="Dane:").pack()
        Label(frame_data, text="Imię:").pack()
        entry_imie = Entry(frame_data)
        entry_imie.pack()
        Label(frame_data, text="Nazwisko:").pack()
        entry_nazwisko = Entry(frame_data)
        entry_nazwisko.pack()
        Label(frame_data, text="Galeria sztuki lub Wystawa:").pack()
        entry_powiazanie = Entry(frame_data)
        entry_powiazanie.pack()

        button_frame = Frame(window, padx=10, pady=10)
        button_frame.pack()
        Button(button_frame, text="Wprowadź",bg = "#64C285", command=wprowadz_dane).pack(side=LEFT, padx=5)
        Button(button_frame, text="Edytuj", bg = "#B8AE45",command=edytuj_dane).pack(side=LEFT, padx=5)
        Button(button_frame, text="Usuń",bg = "#FF4043", command=usun_dane).pack(side=LEFT, padx=5)

    ramka_przyciski = Frame(root, padx=10, pady=10)
    ramka_przyciski.grid(row=1, column=0, sticky="nsew")

    ramka_wyswietlanie = Frame(root, bg="#EFEFEF", padx=10, pady=10)
    ramka_wyswietlanie.grid(row=1, column=1, sticky="nsew")

    Label(ramka_wyswietlanie, text="Zebrane dane:").pack()
    dane_text = Text(ramka_wyswietlanie, height=15, width=60)
    dane_text.pack()

    Label(ramka_wyswietlanie, text="Wyszukaj nazwę galerii lub wystawy:").pack(pady=(10, 0))
    search_entry = Entry(ramka_wyswietlanie, width=30)
    search_entry.pack(pady=5)

    def search_data():
        dane_text.delete("0", END)
        query = search_entry.get()
        if not query:
            return
        znaleziono = False
        for galeria in dane_galerie:
            if galeria[0] == query:
                dane_text.insert(END, f"Galeria Sztuki: {galeria[0]} ({galeria[1]})")
                coords = get_coordinates(galeria[1])
                if coords:
                    map_widget.set_position(coords[0], coords[1])
                    map_widget.set_zoom(12)
                    delete_marker_by_name(galeria[0])
                    marker = map_widget.set_marker(coords[0], coords[1], text=galeria[0])
                    markers.append([galeria[0], marker])
                for dzielo in dane_dziela:
                    if dzielo[2] == galeria[0]:
                        dane_text.insert(END, f" - Dzieło: {dzielo[0]} (autor: {dzielo[1]})")
                for pracownik in dane_pracownicy:
                    if pracownik[2] == galeria[0]:
                        dane_text.insert(END, f" - Pracownik: {pracownik[0]} {pracownik[1]}")
                znaleziono = True
        for wystawa in dane_wystawy:
            if wystawa[0] == query:
                dane_text.insert(END, f"Wystawa artystyczna: {wystawa[0]} ({wystawa[1]})")
                coords = get_coordinates(wystawa[1])
                if coords:
                    map_widget.set_position(coords[0], coords[1])
                    map_widget.set_zoom(12)
                    delete_marker_by_name(wystawa[0])
                    marker = map_widget.set_marker(coords[0], coords[1], text=wystawa[0])
                    markers.append([wystawa[0], marker])
                for dzielo in dane_dziela:
                    if dzielo[2] == wystawa[0]:
                        dane_text.insert(END, f" - Dzieło: {dzielo[0]} (autor: {dzielo[1]})")
                for pracownik in dane_pracownicy:
                    if pracownik[2] == wystawa[0]:
                        dane_text.insert(END, f" - Pracownik: {pracownik[0]} {pracownik[1]}")
                znaleziono = True
        if not znaleziono:
            dane_text.insert(END, "Nie znaleziono Galerii Sztuki ani Wystawy.")

    def search_data():
        dane_text.delete(1.0, END)  #czyszczenie pola przed wpisaniem nowego
        query = search_entry.get().strip() #zmienna query
        if not query:
            return
        znaleziono = False # zmienna znaleziono
        for galeria in dane_galerie:
            if galeria[0].strip().lower() == query.lower():
                dane_text.insert(END, f"Galeria Sztuki: {galeria[0]} ({galeria[1]})") # jeęli jest galeria to wstawia do pola
                coords = get_coordinates(galeria[1]) # wywolanie coords z argumentem galeria - lokalizacja
                if coords: #jesli istnieje przesuwanie stareg znacznika dodawanie nowego
                    map_widget.set_position(coords[0], coords[1]) #Ustawia środek mapy w punkcie
                    map_widget.set_zoom(12)
                    delete_marker_by_name(galeria[0])
                    marker = map_widget.set_marker(coords[0], coords[1], text=galeria[0]) #nowy znacznik
                    markers.append([galeria[0], marker])
                for dzielo in dane_dziela:
                    if dzielo[2] == galeria[0]:
                        dane_text.insert(END, f" - Dzieło: {dzielo[0]} (autor: {dzielo[1]})\n")
                for pracownik in dane_pracownicy:
                    if pracownik[2] == galeria[0]:
                        dane_text.insert(END, f" - Pracownik: {pracownik[0]} {pracownik[1]}\n")
                dane_text.insert(END, "\n")
                znaleziono = True
        for wystawa in dane_wystawy:
            if wystawa[0].strip().lower() == query.lower():
                dane_text.insert(END, f"Wystawa artystyczna: {wystawa[0]} ({wystawa[1]})\n")
                coords = get_coordinates(wystawa[1])
                if coords:
                    map_widget.set_position(coords[0], coords[1])
                    map_widget.set_zoom(12)
                    delete_marker_by_name(wystawa[0])
                    marker = map_widget.set_marker(coords[0], coords[1], text=wystawa[0])
                    markers.append([wystawa[0], marker])
                for dzielo in dane_dziela:
                    if dzielo[2] == wystawa[0]:
                        dane_text.insert(END, f" - Dzieło: {dzielo[0]} (autor: {dzielo[1]})\n")
                for pracownik in dane_pracownicy:
                    if pracownik[2] == wystawa[0]:
                        dane_text.insert(END, f" - Pracownik: {pracownik[0]} {pracownik[1]}\n")
                dane_text.insert(END, "\n")
                znaleziono = True
        if not znaleziono:
            dane_text.insert(END, "Nie znaleziono Galerii Sztuki ani Wystawy.\n")

    Button(ramka_wyswietlanie, text="Szukaj", command=search_data).pack(pady=5)

    Button(ramka_przyciski, text="Galerie sztuki", bg="#8280FF", command=open_galerie_window).pack(pady=5, fill=X)
    Button(ramka_przyciski, text="Wystawy",bg="#8280FF", command=open_wystawy_window).pack(pady=5, fill=X)
    Button(ramka_przyciski, text="Dzieła",bg="#8280FF" ,command=open_dziela_window).pack(pady=5, fill=X)
    Button(ramka_przyciski, text="Pracownicy",bg="#8280FF", command=open_pracownicy_window).pack(pady=5, fill=X)

    root.mainloop()

if __name__ == "__main__":
    start_app()



