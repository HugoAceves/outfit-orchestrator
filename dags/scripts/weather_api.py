import requests
import json
from datetime import datetime
import pytz

def get_weather():
    #URL de la API de pronóstico
    api_url = "http://api.openweathermap.org/data/2.5/forecast"
    city = "Puebla"
    api_key = "5da945ca87156a0085909a9efcac6ccd"

    #Parámetros de la solicitud
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'lang': 'es'
    }

    try:
        #Realizar la solicitud a la API
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        #Procesar los datos de la respuesta
        forecast_data = response.json()

        #Zona horaria local (el DAG está pensado para ejecutarse a las 7am, de modo que si se ejecuta a otra hora, dará error)
        #local_tz = pytz.timezone("America/Mexico_city")
        local_tz = pytz.timezone("Europe/London") #Usamos esta para probar el código de noche
        now = datetime.now(local_tz)
        today = now.date()

        #Horas deseadas
        target_hours = [9, 12, 15, 18, 21]

        #Filtrar los datos del día actual y las horas especificadas
        today_forecast = [
            {
                'time': datetime.fromisoformat(entry['dt_txt']).astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S"),
                'feels_like': entry['main']['feels_like'],
                'rain_chance': entry.get('rain', {}).get('3h', 0)  #Probabilidad de lluvia en 3h
            }
            for entry in forecast_data['list']
            if datetime.fromisoformat(entry['dt_txt']).astimezone(local_tz).date() == today
            and datetime.fromisoformat(entry['dt_txt']).astimezone(local_tz).hour in target_hours
            and datetime.fromisoformat(entry['dt_txt']).astimezone(local_tz) > now
        ]

        #Guardar los datos en un archivo JSON
        with open('weather_data.json', 'w') as json_file:
            json.dump(today_forecast, json_file, ensure_ascii=False, indent=4)

        if today_forecast:
            print("Datos del pronóstico guardados correctamente")
        else:
            print("No se encontraron datos relevantes para el día actual.")

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el pronóstico del clima: {e}")

#Prueba del script
if __name__ == "__main__":
    get_weather()
