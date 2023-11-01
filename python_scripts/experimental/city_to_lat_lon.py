import requests
import pandas as pd
import sys
from pathlib import Path
<<<<<<< HEAD
sys.path.append(str(Path('.').absolute().parent) + '\\final_project')
from config import *

def city_to_lat_lon(city):

    api_key = openweather_API_KEY
=======

sys.path.append(str(Path('.').absolute().parent) + '\\final_project')

from config import *


def city_to_lat_lon(city):

    api_key = OpenWeather_API_KEY
>>>>>>> 27ba8d13d18edd38486f42644353c58fa6b5fdf5
    api_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city},&limit=1&appid={api_key}'
    response = requests.get(api_url)
    data = response.json()
    df = pd.json_normalize(data)
    lat = df["lat"][0]
    lon = df["lon"][0]
    return lat, lon
# if response.status_code == requests.codes.ok:
#     print(response.text)
# else:
#     print("Error:", response.status_code, response.text)
        

if __name__ == "__main__":
    print(city_to_lat_lon('Göteborg'))

