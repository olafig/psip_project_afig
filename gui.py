

from tkinter import *
import requests
import tkintermapview
from bs4 import BeautifulSoup


def main():
    class Exhibition:
        def __init__(self, name, type, author, title, date, medium, location):
            self.name = name
            self.type = type
            self.author = author
            self.title = title
            self.date = date
            self.medium = medium
            self.location = location
            self.coordinates = self.get_coordinates()
            self.marker = map_widget.set_marker(
                self.coordinates[0],
                self.coordinates[1],
                text=f'{self.name} - {self.author}',
            )

        def get_coordinates(self):
            try:
                url = f'https://pl.wikipedia.org/wiki/{self.location}'
                response = requests.get(url)
                response_html = BeautifulSoup(response.text, 'html.parser')
                latitude = float(response_html.select_one('.latitude').text.replace(',', '.'))
                longitude = float(response_html.select_one('.longitude').text.replace(',', '.'))
                return [latitude, longitude]
            except Exception as e:
                print(f"Błąd pobierania współrzędnych dla {self.location}: {e}")
                return [52.0, 21.0]  # Domyślne współrzędne (Warszawa)

    exhibitions = []

    def show_exhibitions():
        listbox_lista_wystaw.delete(0, END)
        for idx, exhibition in enumerate(exhibitions):
            listbox_lista_wystaw.insert(idx, f'{exhibition.name} | {exhibition.type} | {exhibition.author}')

    def add_exhibition():
        name = entry_name.get()
        type = entry_type.get()
        author = entry_author.get()
        title = entry_title.get()
        date = entry_date.get()
        medium = entry_medium.get()
        location = entry_location.get()

        new_exhibition = Exhibition(name, type, author, title, date, medium, location)
        exhibitions.append(new_exhibition)
        show_exhibitions()

        # Clear input fields after adding
        entry_name.delete(0, END)
        entry_type.delete(0, END)
        entry_author.delete(0, END)
        entry_title.delete(0, END)
        entry_date.delete(0, END)
        entry_medium.delete(0, END)
        entry_location.delete(0, END)

    def delete_user():
        selected_index = listbox_lista_wystaw.curselection()
        if selected_index:
            idx = selected_index[0]
            exhibitions[idx].marker.delete()
            exhibitions.pop(idx)
            show_exhibitions()

    def show_exhibition_details():
        selected_index = listbox_lista_wystaw.curselection()
        if selected_index:
            idx = selected_index[0]
            exhibition = exhibitions[idx]
            label_szczegoly_name_wartosc.config(text=exhibition.name)
            label_szczegoly_type_wartosc.config(text=exhibition.type)
            label_szczegoly_author_wartosc.config(text=exhibition.author)
            label_szczegoly_location_wartosc.config(text=exhibition.location)
            map_widget.set_position(exhibition.coordinates[0], exhibition.coordinates[1])
            map_widget.set_zoom(12)

    root = Tk()
    root.geometry("1000x800")
    root.title("EXHIBITION_API")

    # Frames
    ramka_mapa = Frame(root, padx=100, pady=20)
    ramka_lista_wystaw = Frame(root, bg="#9E6189", padx=10, pady=10)
    ramka_info = Frame(root, bg="#9E6189", padx=10, pady=10)
    ramka_szczegoly_obiektu = Frame(root, bg="#9E6189", padx=10, pady=10)

    # Place map frame at the top
    ramka_mapa.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # Place list and details below the map
    ramka_lista_wystaw.grid(row=1, column=0, sticky="nsew")
    ramka_info.grid(row=1, column=1, sticky="nsew")
    ramka_szczegoly_obiektu.grid(row=2, column=0, columnspan=2, sticky="nsew")

    # Map widget
    map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=800, height=400)
    map_widget.set_position(52.0, 21.0)
    map_widget.set_zoom(6)
    map_widget.pack(fill=BOTH, expand=True)

    # List of exhibitions
    Label(ramka_lista_wystaw, text="Lista galerii i wystaw:", bg="#9E6189", fg="black").grid(row=0, column=0, sticky=W, padx=80)
    listbox_lista_wystaw = Listbox(ramka_lista_wystaw, width=50)
    listbox_lista_wystaw.grid(row=1, column=0, columnspan=2)
    Button(ramka_lista_wystaw, text="Pokaż szczegóły", command=show_exhibition_details).grid(row=2, column=0, pady=5, padx=80)
    Button(ramka_lista_wystaw, text="Usuń obiekt", command=delete_user).grid(row=2, column=1, pady=5, padx=80)

    # Form to add exhibitions
    Label(ramka_info, text="Dodaj obiekt:", bg="#9E6189", fg="black").grid(row=0, column=0, columnspan=2, sticky=W)

    Label(ramka_info, text="Nazwa:", bg="#9E6189").grid(row=1, column=0, sticky=W)
    entry_name = Entry(ramka_info)
    entry_name.grid(row=1, column=1)

    Label(ramka_info, text="Typ:", bg="#9E6189").grid(row=2, column=0, sticky=W)
    entry_type = Entry(ramka_info)
    entry_type.grid(row=2, column=1)

    Label(ramka_info, text="Autor:", bg="#9E6189").grid(row=3, column=0, sticky=W)
    entry_author = Entry(ramka_info)
    entry_author.grid(row=3, column=1)

    Label(ramka_info, text="Tytuł:", bg="#9E6189").grid(row=4, column=0, sticky=W)
    entry_title = Entry(ramka_info)
    entry_title.grid(row=4, column=1)

    Label(ramka_info, text="Data powstania:", bg="#9E6189").grid(row=5, column=0, sticky=W)
    entry_date = Entry(ramka_info)
    entry_date.grid(row=5, column=1)

    Label(ramka_info, text="Medium:", bg="#9E6189").grid(row=6, column=0, sticky=W)
    entry_medium = Entry(ramka_info)
    entry_medium.grid(row=6, column=1)

    Label(ramka_info, text="Lokalizacja:", bg="#9E6189").grid(row=7, column=0, sticky=W)
    entry_location = Entry(ramka_info)
    entry_location.grid(row=7, column=1)

    Button(ramka_info, text="Dodaj obiekt", command=add_exhibition).grid(row=8, column=0, columnspan=2, pady=5)

    # Object details
    Label(ramka_szczegoly_obiektu, text="Szczegóły obiektu:", bg="#9E6189", fg="black").grid(row=0, column=0, sticky=W, padx=80)
    label_szczegoly_name_wartosc = Label(ramka_szczegoly_obiektu, text="...")
    label_szczegoly_name_wartosc.grid(row=1, column=1)

    root.mainloop()


if __name__ == '__main__':
    main()
