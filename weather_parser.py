import requests
import datetime

TOKEN = "9ff2206588d4121162efd6d4bba6c220"


def get_response(city_name: str, token: str = TOKEN):
    """Uzatilgan URL address bo'yicha GET so'riv yuboradi va javobni qaytaradi"""

    params = {
        "q": city_name,
        "appid": TOKEN,
        "units": "metric",
    }

    response = requests.get(url=f"https://api.openweathermap.org/data/2.5/weather", params=params)

    try:
        response.raise_for_status()
        return response.json()

    except requests.HTTPError:
        print(f"Shahar topilmadi, status kod: {response.status_code}")
        return None


def get_weather_info(city_name: str):
    """Uzatilgan shaharda hozirgi paytdagi ob-havo ma'lumotini qaytaradi"""

    data = get_response(city_name=city_name)

    if data is None:
        return None

    sunrise = data["sys"]["sunrise"]
    sunset = data["sys"]["sunset"]
    timezone = str(data["timezone"] // 3600)
    sunrise = datetime.datetime.fromtimestamp(sunrise).time()
    sunset = datetime.datetime.fromtimestamp(sunset).time()
    description = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    temp_min = data["main"]["temp_min"]
    temp_max = data["main"]["temp_max"]
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    country = data["sys"]["country"]

    text = f"""Bugun {city_name.capitalize()} da
Havo: {description.capitalize()}
    
Harorat: {temp} °C
Min. harorat: {temp_min} °C
Max. harorat: {temp_max} °C

Bosim: {pressure} Pa
Namlik: {humidity} %

Quyish chiqishi: {str(sunrise)}
Quyosh botishi: {str(sunset)}

Vaqt farqi: {"+" + timezone + ":00" if int(timezone) > 0 else timezone + ":00"}
Davlat: {country} 
"""

    return text
