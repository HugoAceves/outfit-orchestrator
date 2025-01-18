import json
import csv
import random
from datetime import datetime

def make_recommendation():
    """
    Genera una recomendación de combinación de ropa basada en el clima, los eventos y el inventario.
    """
    try:
        #Cargar datos del clima
        with open('dags/scripts/weather_data.json', 'r', encoding='utf-8') as weather_file:
            weather_data = json.load(weather_file)
        
        #Determinar el clima predominante (temperatura más baja y probabilidad de lluvia)
        min_temp = min(entry['feels_like'] for entry in weather_data)
        rain_chance = any(entry['rain_chance'] > 0 for entry in weather_data)
        
        #Cargar eventos relevantes
        with open('dags/scripts/blue_events.json', 'r', encoding='utf-8') as events_file:
            events = json.load(events_file)
        
        outside = len(events) > 0  #Estará fuera de casa si hay eventos

        #Cargar inventario
        with open('dags/scripts/inventory.csv', 'r', encoding='utf-8') as inventory_file:
            reader = csv.DictReader(inventory_file)
            inventory = list(reader)

        #Filtrar el inventario basado en las condiciones
        calzado = [item for item in inventory if item['nivel'] == 'Calzado']
        pantalon = [item for item in inventory if item['nivel'] == 'Pantalón']
        top = [item for item in inventory if item['nivel'] == 'Top']
        accesorio = []

        #Reglas de selección
        if min_temp < 10:  #Frío
            top = [item for item in top if item['tipo'] == 'Suéter']
            accesorio = [item for item in inventory if item['nivel'] == 'Accesorio' and item['tipo'] == 'Chamarra']
        elif min_temp < 16:  #Fresco
            top = [item for item in top if item['tipo'] in ['Suéter', 'Camisa']]
        else:  #Cálido o caluroso
            top = [item for item in top if item['tipo'] == 'Camisa']

        if rain_chance:
            accesorio += [item for item in inventory if item['nivel'] == 'Accesorio' and item['impermeable'] == 'Sí']
        if outside and not accesorio:
            accesorio += [item for item in inventory if item['nivel'] == 'Accesorio' and item['tipo'] == 'Chamarra']

        #Seleccionar una prenda aleatoria de cada categoría
        selected_combination = {
            'calzado_id': random.choice(calzado)['id'] if calzado else None,
            'pantalon_id': random.choice(pantalon)['id'] if pantalon else None,
            'top_id': random.choice(top)['id'] if top else None,
            'accesorio_id': random.choice(accesorio)['id'] if accesorio else None
        }

        #Guardar la combinación en combinations.csv
        combination_id = f"comb_{int(datetime.now().timestamp())}"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('dags/scripts/combinations.csv', 'a', encoding='utf-8', newline='') as combinations_file:
            writer = csv.DictWriter(combinations_file, fieldnames=['id', 'timestamp', 'calzado_id', 'pantalon_id', 'top_id', 'accesorio_id'])
            if combinations_file.tell() == 0:
                writer.writeheader()
            writer.writerow({
                'id': combination_id,
                'timestamp': timestamp,
                **selected_combination
            })

        print(f"Recomendación generada: {selected_combination}")
        return selected_combination

    except Exception as e:
        print(f"Error al generar la recomendación: {e}")
        return None

#Prueba del script
if __name__ == '__main__':
    recommendation = make_recommendation()
    if recommendation:
        print("Recomendación generada exitosamente.")
