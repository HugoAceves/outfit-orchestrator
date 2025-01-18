import csv
import os
from datetime import datetime

def get_combinations():
    """
    Lee el archivo combinations.csv y devuelve una lista de combinaciones existentes.
    """
    combinations_file = 'dags/scripts/combinations.csv'
    
    #Verifica si el archivo existe
    if not os.path.exists(combinations_file):
        print(f"Error: El archivo {combinations_file} no existe.")
        return []
    
    combinations_data = []

    try:
        #Lee el archivo CSV
        with open(combinations_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                #Convierte el timestamp a un objeto datetime
                try:
                    timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    print(f"Advertencia: Formato de timestamp inválido en la fila: {row}")
                    continue
                
                combinations_data.append({
                    'id': row['id'],
                    'timestamp': timestamp,
                    'calzado_id': row['calzado_id'],
                    'pantalon_id': row['pantalon_id'],
                    'top_id': row['top_id'],
                    'accesorio_id': row['accesorio_id']
                })
        
        print("Combinaciones procesadas exitosamente.")
        return combinations_data

    except Exception as e:
        print(f"Error al procesar el archivo {combinations_file}: {e}")
        return []

#Prueba del script
if __name__ == '__main__':
    combinations = get_combinations()
    if combinations:
        print("Combinaciones existentes:")
        for comb in combinations:
            print(comb)
