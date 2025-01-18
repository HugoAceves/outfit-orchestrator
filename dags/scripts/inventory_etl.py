import csv
import os

def process_inventory():
    """
    Lee el archivo inventory.csv y organiza las prendas en un diccionario estructurado por tipo de prenda.
    """
    inventory_file = 'dags/scripts/inventory.csv'  #Cambiar al archivo correcto
    
    #Verifica si el archivo existe
    if not os.path.exists(inventory_file):
        print(f"Error: El archivo {inventory_file} no existe.")
        return
    
    inventory_data = {
        'calzado': [],
        'pantalón': [],
        'top': [],
        'accesorio': []
    }

    try:
        #Lee el archivo CSV
        with open(inventory_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                #Clasifica las prendas por el nivel
                nivel = row['nivel'].lower()
                if nivel in inventory_data:
                    inventory_data[nivel].append({
                        'id': row['id'],
                        'color': row['color'],
                        'tipo': row.get('tipo', '-'),
                        'impermeable': row.get('impermeable', 'N/A')
                    })
                else:
                    print(f"Advertencia: Nivel desconocido '{nivel}' en el archivo CSV.")
        
        print("Inventario procesado exitosamente.")
        return inventory_data

    except KeyError as e:
        print(f"Error: Falta la columna esperada en el archivo CSV: {e}")
    except Exception as e:
        print(f"Error al procesar el archivo {inventory_file}: {e}")

#Prueba del script
if __name__ == '__main__':
    inventory = process_inventory()
    if inventory:
        print("Estructura del inventario:")
        for nivel, items in inventory.items():
            print(f"{nivel.capitalize()} ({len(items)}): {items}")
