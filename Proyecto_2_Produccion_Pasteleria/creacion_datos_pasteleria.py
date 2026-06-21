import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# 1. Inicializamos Faker en español
fake = Faker('es_ES')

# 2. Definimos las reglas de tu negocio (El catálogo de la pastelería)
menu_produccion = {
    "Masas Quebradas": ["Tartaleta de fresa", "Pie de limon"],
    "Bizcochos": ["Torta de chocolate", "Tres leches", "Red velvet"],
    "Hojaldres": ["Mil hojas", "Croissant", "Empanada dulce"]
}

#3 lista vacia que guardara los registros
registros_cocina = []

#creamos un bucle con 5000 registros
print("⏳ Fabricando 5,000 registros de producción...")
for i in range(5000):
    # Fabricamos la fecha (cualquier día del último año)
    fecha = fake.date_between(start_date='-1y', end_date='today')
    
    # Asignamos el turno al azar
    turno = random.choice(["Mañana", "Tarde"])
    
    # Creamos un ID único para la tanda que sale del horno (Ej. LOTE-4592)
    lote_id = f"LOTE-{random.randint(1000, 9999)}"
    
    #Elegimos una Familia al azar, y luego un Producto de esa Familia
    familia_elegida = random.choice(list(menu_produccion.keys()))
    producto_elegido = random.choice(menu_produccion[familia_elegida])
    
    # Simulamos la realidad de la cocina (Métricas)
    unidades = random.randint(10, 60) # Salen entre 10 y 60 unidades por lote
    tiempo_horno = random.randint(15, 55) # Minutos que el horno estuvo bloqueado
    merma = round(random.uniform(0.1, 3.0), 2) # Kilos desperdiciados (entre 100 gramos y 3 kilos)
    
    # Metemos todos estos datos en una fila y la guardamos en nuestra "bandeja"
    registros_cocina.append([fecha, turno, lote_id, familia_elegida, producto_elegido, unidades, tiempo_horno, merma])
    
# Convertimos la bandeja en una tabla de Pandas y le ponemos los títulos a las columnas
df_produccion = pd.DataFrame(registros_cocina, columns=[
    'Fecha_Produccion', 'Turno', 'Lote_ID', 'Familia_Preparacion', 
    'Producto', 'Unidades_Producidas', 'Tiempo_Horneado_Min', 'Merma_Kg'
])

#Exportamos a CSV
df_produccion.to_csv('produccion_pasteleria_fake.csv', index=False)
print("¡Listo! Las 5,000 tandas de producción han sido registradas y guardadas en el CSV.")