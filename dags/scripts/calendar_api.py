from __future__ import print_function
import datetime
import os
import pickle
import pytz
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

#Si se modifican estos alcances, elimine el archivo token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar():
    """Muestra los próximos eventos en color azul del calendario."""
    creds = None
    #Rutas relativas a la estructura del proyecto
    token_path = 'dags/scripts/token.pickle'
    credentials_path = 'dags/scripts/credentials.json'
    blue_events_path = 'dags/scripts/blue_events.json'

    #Verificar si existe el archivo token.pickle para usar credenciales existentes
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    #Si no hay credenciales válidas, solicitar autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            #creds = flow.run_console()  #Cambiado para evitar `run_local_server`
            creds = flow.run_local_server(port=7454)

        
        #Guardar las credenciales para futuras ejecuciones
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    try:
        #Construir el servicio de Google Calendar
        service = build('calendar', 'v3', credentials=creds)

        #Obtener la zona horaria local
        local_tz = pytz.timezone("America/Mexico_City")
        now = datetime.datetime.now(local_tz).isoformat()

        #Llamada a la API de Google Calendar
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        blue_events = []

        if not events:
            print('No hay próximos eventos encontrados.')
            return

        print('Próximos eventos en color azul:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            if event.get('colorId') == '9':  #Color azul en Google Calendar
                start_time = datetime.datetime.fromisoformat(start).astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")
                end_time = datetime.datetime.fromisoformat(end).astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")
                blue_events.append({
                    'summary': event['summary'],
                    'start': start_time,
                    'end': end_time
                })
                print(start_time, end_time, event['summary'])

        #Guardar los datos en un archivo JSON
        os.makedirs(os.path.dirname(blue_events_path), exist_ok=True)
        with open(blue_events_path, 'w') as json_file:
            json.dump(blue_events, json_file, ensure_ascii=False, indent=4)

        if blue_events:
            print("Datos de eventos en color azul guardados correctamente.")
        else:
            print("No se encontraron eventos en color azul.")

    except Exception as e:
        print(f"Error al obtener eventos del calendario: {e}")

#Prueba del script
if __name__ == '__main__':
    get_calendar()
