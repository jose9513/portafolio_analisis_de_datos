import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# 1. Inicializamos Faker en español
fake = Faker('es_ES')

# 2. Definimos las reglas de tu negocio (El catálogo de la joyería)
categorias = ['Collares', 'Anillos', 'Pulseras', 'Pendientes']
materiales = ['Acero 316L', 'Acero con Baño PVD', 'Plata 925']

# Aquí guardaremos todas las filas antes de exportarlas
datos_ventas = []

# 3. Configuramos la máquina del tiempo (Último año de ventas)
fecha_inicio = datetime.now() - timedelta(days=365)

print("⏳ Fabricando 5,000 registros de ventas...")

# 4. El bucle creador: Haremos 5000 transacciones
for i in range(5000):
    # Generamos una fecha aleatoria dentro del último año
    dias_aleatorios = random.randint(0, 365)
    fecha_venta = fecha_inicio + timedelta(days=dias_aleatorios)
    
    # Seleccionamos un producto al azar usando las listas de tu negocio
    categoria = random.choice(categorias)
    material = random.choice(materiales)
    
    # Creamos un SKU (Ej: COL-316L-9482)
    sku = f"{categoria[:3].upper()}-{material[:3].upper()}-{random.randint(1000, 9999)}"
    
    # Inventamos datos financieros lógicos
    costo_adquisicion = round(random.uniform(15.0, 45.0), 2)
    # El precio de venta será entre 1.5 y 3 veces el costo (para tener márgenes reales)
    precio_venta = round(costo_adquisicion * random.uniform(1.5, 3.0), 2)
    
    # Cantidad vendida (lo normal es 1, rara vez compran 5 de golpe)
    cantidad = random.choices([1, 2, 3, 4, 5], weights=[70, 15, 10, 3, 2])[0]
    
    # Cliente falso
    cliente = fake.name()
    ciudad = fake.city()

    # 5. Metemos toda esta fila a nuestra lista maestra
    datos_ventas.append([
        fecha_venta.strftime("%Y-%m-%d"), 
        sku, 
        categoria, 
        material, 
        costo_adquisicion, 
        precio_venta, 
        cantidad, 
        cliente, 
        ciudad
    ])

# 6. Convertimos la lista en una tabla bonita usando Pandas
columnas = ['Fecha', 'SKU', 'Categoria', 'Material', 'Costo_Adquisicion', 'Precio_Venta', 'Cantidad', 'Cliente', 'Ciudad']
df_ventas = pd.DataFrame(datos_ventas, columns=columnas)

# 7. Lo exportamos a un archivo CSV
df_ventas.to_csv('ventas_joyeria_fake.csv', index=False)

print("✅ ¡Listo! Se ha creado el archivo 'ventas_joyeria_fake.csv' con éxito.")