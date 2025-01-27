
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
            url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
            response = requests.get(url)
            response_html = BeautifulSoup(response.text, 'html.parser')
            return [
                float(response_html.select('.latitude')[1].text.replace(',', '.')),
                float(response_html.select('.longitude')[1].text.replace(',', '.'))
            ]


    exhibitions = []

    def validate_inputs():
        inputs = [entry_name, entry_type, entry_author, entry_title, entry_date, entry_medium, entry_location]
        for entry in inputs:
            if not entry.get().strip():
                return False
        return True

    def show_exhibitions():
        listbox_lista_wystaw.delete(0, END)
        for idx, exhibition in enumerate(exhibitions):
            listbox_lista_wystaw.insert(idx, f'{exhibition.name} | {exhibition.type} | {exhibition.author}')

    def add_exhibition():
        if not validate_inputs():
            print("Wszystkie pola muszą być wypełnione!")
            return

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

        clear_inputs()

    def clear_inputs():
        entries = [entry_name, entry_type, entry_author, entry_title, entry_date, entry_medium, entry_location]
        for entry in entries:
            entry.delete(0, END)

    def delete_exhibition():
        selected_index = listbox_lista_wystaw.curselection()
        if selected_index:
            idx = selected_index[0]
            exhibitions[idx].marker.delete()
            exhibitions.pop(idx)
            show_exhibitions()

    def edit_exhibition():
        selected_index = listbox_lista_wystaw.curselection()
        if selected_index:
            idx = selected_index[0]
            exhibition = exhibitions[idx]

            entry_name.insert(0, exhibition.name)
            entry_type.insert(0, exhibition.type)
            entry_author.insert(0, exhibition.author)
            entry_title.insert(0, exhibition.title)
            entry_date.insert(0, exhibition.date)
            entry_medium.insert(0, exhibition.medium)
            entry_location.insert(0, exhibition.location)

            button_add.config(text='Zapisz zmiany', command=lambda: update_exhibition(idx))

    def update_exhibition(idx):
        if not validate_inputs():
            print("Wszystkie pola muszą być wypełnione!")
            return

        exhibition = exhibitions[idx]
        exhibition.name = entry_name.get()
        exhibition.type = entry_type.get()
        exhibition.author = entry_author.get()
        exhibition.title = entry_title.get()
        exhibition.date = entry_date.get()
        exhibition.medium = entry_medium.get()
        exhibition.location = entry_location.get()
        exhibition.coordinates = exhibition.get_coordinates()

        exhibition.marker.delete()
        exhibition.marker = map_widget.set_marker(exhibition.coordinates[0], exhibition.coordinates[1])

        clear_inputs()
        button_add.config(text='Dodaj obiekt', command=add_exhibition)
        show_exhibitions()

    def show_exhibition_details():
        selected_index = listbox_lista_wystaw.curselection()
        if selected_index:
            idx = selected_index[0]
            exhibition = exhibitions[idx]
            label_szczegoly_name_wartosc.config(text=exhibition.name)
            label_szczegoly_type_wartosc.config(text=exhibition.type)
            label_szczegoly_author_wartosc.config(text=exhibition.author)
            label_szczegoly_title_wartosc.config(text=exhibition.title)
            label_szczegoly_date_wartosc.config(text=exhibition.date)
            label_szczegoly_medium_wartosc.config(text=exhibition.medium)
            label_szczegoly_location_wartosc.config(text=exhibition.location)
            map_widget.set_position(exhibition.coordinates[0], exhibition.coordinates[1])
            map_widget.set_zoom(12)

    root = Tk()
    root.geometry("1000x900")
    root.title("EXHIBITION_API")

    ramka_mapa = Frame(root, padx=100, pady=20)
    ramka_lista_wystaw = Frame(root, bg="#9E6189", padx=10, pady=10)
    ramka_info = Frame(root, bg="#9E6189", padx=10, pady=10)
    ramka_szczegoly_obiektu = Frame(root, bg="#9E6189", padx=10, pady=10)

    ramka_mapa.grid(row=0, column=0, columnspan=2, sticky="nsew")
    ramka_lista_wystaw.grid(row=1, column=0, sticky="nsew")
    ramka_info.grid(row=1, column=1, sticky="nsew")
    ramka_szczegoly_obiektu.grid(row=2, column=0, columnspan=2, sticky="nsew")

    map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=800, height=400)
    map_widget.set_position(52.0, 21.0)
    map_widget.set_zoom(6)
    map_widget.pack(fill=BOTH, expand=True)

    Label(ramka_lista_wystaw, text="Lista galerii i wystaw:", bg="#9E6189", fg="black").grid(row=0, column=0, sticky=W, padx=80)
    listbox_lista_wystaw = Listbox(ramka_lista_wystaw, width=50)
    listbox_lista_wystaw.grid(row=1, column=0, columnspan=2)
    Button(ramka_lista_wystaw, text="Pokaż szczegóły", command=show_exhibition_details).grid(row=2, column=0, pady=5, padx=80)
    Button(ramka_lista_wystaw, text="Usuń obiekt", command=delete_exhibition).grid(row=2, column=1, pady=5, padx=80)
    Button(ramka_lista_wystaw, text="Edytuj obiekt", command=edit_exhibition).grid(row=3, column=1, pady=5, padx=80)

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

    button_add = Button(ramka_info, text="Dodaj obiekt", command=add_exhibition)
    button_add.grid(row=8, column=0, columnspan=2, pady=5)

    Label(ramka_szczegoly_obiektu, text="Szczegóły obiektu:", bg="#9E6189", fg="black").grid(row=0, column=0, sticky=W, padx=80)

    Label(ramka_szczegoly_obiektu, text="Nazwa:", bg="#9E6189").grid(row=1, column=0, sticky=W)
    label_szczegoly_name_wartosc = Label(ramka_szczegoly_obiektu, text="...")
    label_szczegoly_name_wartosc.grid(row=1, column=1)

    Label(ramka_szczegoly_obiektu, text="Typ:", bg="#9E6189").grid(row=2, column=0, sticky=W)
    label_szczegoly_type_wartosc = Label(ramka_szczegoly_obiektu, text="...")
    label_szczegoly_type_wartosc.grid(row=2, column=1)

    Label(ramka_szczegoly_obiektu, text="Autor:", bg="#9E6189").grid(row=3, column=0, sticky=W)
    label_szczegoly_author_wartosc = Label(ramka_szczegoly_obiektu, text="...")
    label_szczegoly_author_wartosc.grid(row=3, column=1)

    Label(ramka_szczegoly_obiektu, text="Tytuł:", bg="#9E6189").grid(row=4, column=0, sticky=W)
    label_szczegoly_title_wartosc = Label(ramka_szczegoly_obiektu, text="...")
    label_szczegoly_title_wartosc.grid(row=4, column=1)

    Label(ramka_szczegoly_obiektu, text="Data:", bg="#9E6189").grid(row=5, column=0, sticky=W)
    label_szczegoly_date_wartosc = Label(ramka_szczegoly_obiektu, text="...")
    label_szczegoly_date_wartosc.grid(row=5, column=1)

    Label(ramka_szczegoly_obiektu, text="Medium:", bg="#9E6189").grid(row=6, column=0, sticky=W)
    label_szczegoly_medium_wartosc = Label(ramka_szczegoly_obiektu, text="...")
    label_szczegoly_medium_wartosc.grid(row=6, column=1)

    Label(ramka_szczegoly_obiektu, text="Lokalizacja:", bg="#9E6189").grid(row=7, column=0, sticky=W)
    label_szczegoly_location_wartosc = Label(ramka_szczegoly_obiektu, text="...")
    label_szczegoly_location_wartosc.grid(row=7, column=1)

    root.mainloop()

if __name__ == '__main__':
    main()
