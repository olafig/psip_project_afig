
places: list=[
    {'name': 'Muzeum Sztuki Nowoczesnej w Warszawie', 'author': 'Tala Mandi', 'title': 'Becoming Brilliant II', 'date': '2013', 'medium': 'farba olejna na płótnie'},
    {'name': 'Muzeum Sztuki Nowoczesnej w Warszawie', 'author': 'Gustav Metzger', 'title': 'Eichmann and the Angel (Warsaw version)','date': '2005/2011', 'medium': 'rekonstrukcja kabiny Eichmanna (płyta wiórowa malowana, aluminium, szkło, tworzywo sztuczne), transmiter taśmowy, gazety, wydruk na papierze, litery winylowe, książki, czasopisma'},
    {'name': 'Muzeum Sztuki Nowoczesnej w Warszawie', 'author': 'Cezary Bodzianowski', 'title': 'Prognoza','date': '2012', 'medium': 'wydruk solwentowy na tkaninie poliestrowej powlekanej PCV'},
    {'name': 'Muzeum Sztuki Nowoczesnej w Warszawie', 'author': 'Aleksandra Waliszewska', 'title': 'Droga na skróty','date': '2012–2013', 'medium': 'gwasz, ołówek na papierze'},
    {'name': 'Muzeum Sztuki Nowoczesnej w Warszawie', 'author': 'Nikita Kadan', 'title': 'Drawing from the Pogrom series','date': '2016–2017', 'medium': 'węgiel na papierze'},
    {'name': 'Muzeum Sztuki w Łodzi', 'author': 'Janusz Maria Brzeski', 'title': 'Narodziny robota: Sielanka XX wieku','date': ' 1933', 'medium': ' fotokolaż, papier'},
    {'name': 'Muzeum Sztuki w Łodzi', 'author': 'Mieczysław Szczuka', 'title': 'Dymy nad miastem. Projekt okładki do tomiku poezji Władysława Broniewskiego','date': ' ok. 1926', 'medium': ' fotomontaż, papier, tusz'},
]

for place in places:
    print(f'Dzieło {place["title"]}, znajduje się w {place["name"]}, autor to {place["author"]}, data powstania to {place["date"]}, medium to {place["medium"]}')