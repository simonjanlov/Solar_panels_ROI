import requests
import pandas as pd

def city_to_lat_lon(city):

    api_key = 'b75a85a55f630b5c79dc87feece0d6bd'
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

