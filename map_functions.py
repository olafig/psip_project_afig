import folium
import requests
from bs4 import BeautifulSoup

def single_user_map(users:list):
    for user in users:
        print(user['city'])
        url:str=f'https://pl.wikipedia.org/wiki/{user["city"]}'
        response = requests.get(url)
        # print(response.text)
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude:float=float(response_html.select('.latitude')[1].text.replace(',','.'))
        print(latitude)
        longitude:float=float(response_html.select('.longitude')[1].text.replace(',','.'))
        print(longitude)
        my_map=folium.Map(location=[latitude,longitude], zoom_start=11)
        folium.Marker(location=[latitude,longitude],popup=f"{user['city']},{user['name']}").add_to(my_map)
        my_map.save(f'map_{user["city"]}.html')


def multi_user_map(users:list):
    my_map = folium.Map(location=[51.919231, 19.134422], zoom_start=11)
    for user in users:
        print(user['city'])
        url: str = f'https://pl.wikipedia.org/wiki/{user["city"]}'
        response = requests.get(url)
        # print(response.text)
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude: float = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        print(latitude)
        longitude: float = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        print(longitude)

        folium.Marker(location=[latitude, longitude], popup=f"{user['city']},{user['name']}").add_to(my_map)
    my_map.save(f'_generalna.html')