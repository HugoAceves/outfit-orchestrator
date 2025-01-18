import csv
import json

def calculate_statistics():
    """
    Calcula los ítems más usados por categoría y guarda los resultados en statistics.json.
    """
    try:
        #Inicializar diccionarios para contar ocurrencias
        usage_count = {
            "calzado": {},
            "pantalon": {},
            "top": {},
            "accesorio": {}
        }

        #Leer datos del archivo CSV y asegurar que los encabezados sean correctos
        with open('dags/scripts/combinations.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            #Asegurar que no haya espacios en los nombres de las columnas
            for row in reader:
                row = {key.strip(): value.strip() for key, value in row.items()}

                for category, field in [("calzado", "calzado_id"), 
                                        ("pantalon", "pantalon_id"), 
                                        ("top", "top_id"), 
                                        ("accesorio", "accesorio_id")]:
                    
                    if row[field]:  #Verificar que el campo no esté vacío
                        usage_count[category][row[field]] = usage_count[category].get(row[field], 0) + 1

        #Encontrar el ítem más usado por categoría
        statistics = {}
        for category, items in usage_count.items():
            if items:
                most_used_item = max(items, key=items.get)
                statistics[f"{category}_mas_usado"] = {
                    "item": most_used_item,
                    "usos": items[most_used_item]
                }
            else:
                statistics[f"{category}_mas_usado"] = {"item": "N/A", "usos": 0}

        #Guardar estadísticas en archivo JSON
        with open('dags/scripts/statistics.json', 'w', encoding='utf-8') as json_file:
            json.dump(statistics, json_file, ensure_ascii=False, indent=4)

        print("Estadísticas guardadas exitosamente en statistics.json")

    except Exception as e:
        print(f"Error al calcular estadísticas: {e}")

#Ejecutar función
if __name__ == '__main__':
    calculate_statistics()
