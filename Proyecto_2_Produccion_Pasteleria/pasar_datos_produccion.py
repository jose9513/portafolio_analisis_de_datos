import csv, sqlite3

conn = sqlite3.connect('produccion_pasteleria.db')
cur = conn.cursor()
conn.execute("PRAGMA foreign_keys = ON")

cur.execute(''' CREATE TABLE IF NOT EXISTS Dim_Producto (
                Producto_ID integer PRIMARY KEY AUTOINCREMENT,
                Producto varchar(50) UNIQUE,
                Familia_Preparacion varchar(50)
            )''')

cur.execute(''' CREATE TABLE IF NOT EXISTS produccion (
                Lote_ID varchar(10) PRIMARY KEY,
                Fecha_Produccion date,
                Turno varchar(10),
                Producto_ID integer,
                Unidades_Producidas integer,
                Tiempo_Horneado_Min integer,
                Merma_Kg float,
                FOREIGN KEY (Producto_ID) REFERENCES Dim_Producto(Producto_ID)
            )''')

with open('Proyecto_2_Produccion_Pasteleria\\produccion_pasteleria_fake.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for fila in reader:
        cur.execute('''INSERT OR IGNORE INTO Dim_Producto (Producto, Familia_Preparacion) 
                       VALUES (?, ?)''', (fila['Producto'], fila['Familia_Preparacion']))
        
        cur.execute('''INSERT OR IGNORE INTO produccion (Lote_ID, Fecha_Produccion, Turno, Producto_ID, Unidades_Producidas, Tiempo_Horneado_Min, Merma_Kg) 
                       VALUES (?, ?, ?, (SELECT Producto_ID FROM Dim_Producto WHERE Producto = ?), ?, ?, ?)''', 
                    (fila['Lote_ID'], fila['Fecha_Produccion'], fila['Turno'], fila['Producto'], fila['Unidades_Producidas'], fila['Tiempo_Horneado_Min'], fila['Merma_Kg']))
        
conn.commit()
conn.close()