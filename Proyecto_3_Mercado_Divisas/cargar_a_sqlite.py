"""
Carga el CSV de divisas a una base de datos SQLite (modelo en estrella).
  Dim_Par : catalogo (1 fila por par)  -> clave primaria Par_ID
  precios : hechos (1 fila por par y dia) -> clave foranea Par_ID

El CSV guarda el Par como texto ("EUR/USD"); la tabla de hechos guarda el
numero Par_ID. Por eso construimos un "diccionario traductor" nombre -> id.
"""

import sqlite3
import pandas as pd
from generador_datos_divisas import dim_par   # importa el catalogo SIN correr los prints (gracias al __name__)

DB = "divisas.db"
CSV = "precios_divisas_fake.csv"

conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys = ON")      # SQLite no activa las FK por defecto
cur = conn.cursor()

# Empezamos limpio cada vez (para no duplicar si corremos el script otra vez)
cur.execute("DROP TABLE IF EXISTS precios")
cur.execute("DROP TABLE IF EXISTS Dim_Par")

# 1) Crear las dos tablas (el modelo en estrella)
cur.execute("""
CREATE TABLE Dim_Par (
    Par_ID          INTEGER PRIMARY KEY AUTOINCREMENT,
    Par             TEXT UNIQUE,
    Moneda_Base     TEXT,
    Moneda_Cotizada TEXT,
    Tipo            TEXT,
    Region          TEXT
)""")

cur.execute("""
CREATE TABLE precios (
    Precio_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Fecha     DATE,
    Par_ID    INTEGER,
    Apertura  REAL,
    Maximo    REAL,
    Minimo    REAL,
    Cierre    REAL,
    Volumen   INTEGER,
    FOREIGN KEY (Par_ID) REFERENCES Dim_Par(Par_ID)
)""")

# 2) Cargar la dimension: 8 filas desde el catalogo
for fila in dim_par.itertuples():
    cur.execute("""INSERT INTO Dim_Par (Par, Moneda_Base, Moneda_Cotizada, Tipo, Region)
                   VALUES (?, ?, ?, ?, ?)""",
                (fila.Par, fila.Moneda_Base, fila.Moneda_Cotizada, fila.Tipo, fila.Region))

# 3) El diccionario traductor nombre -> Par_ID (lo armamos UNA vez)
#    Mejora sobre la pasteleria: alli resolviamos el id con un subquery en CADA fila.
mapa = {par: pid for par, pid in cur.execute("SELECT Par, Par_ID FROM Dim_Par")}

# 4) Cargar los hechos desde el CSV, traduciendo el Par a su numero
df = pd.read_csv(CSV)
for fila in df.itertuples():
    cur.execute("""INSERT INTO precios (Fecha, Par_ID, Apertura, Maximo, Minimo, Cierre, Volumen)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (fila.Fecha, mapa[fila.Par], fila.Apertura, fila.Maximo,
                 fila.Minimo, fila.Cierre, fila.Volumen))

conn.commit()

# 5) VERIFICACION: contar filas y probar que el "hilo" (la relacion) funciona con un JOIN
n_dim = cur.execute("SELECT COUNT(*) FROM Dim_Par").fetchone()[0]
n_hechos = cur.execute("SELECT COUNT(*) FROM precios").fetchone()[0]
print(f"Dim_Par: {n_dim} filas")
print(f"precios: {n_hechos} filas")

print("\nPrueba del JOIN (filas por tipo, cruzando las dos tablas):")
consulta = """
    SELECT d.Tipo, COUNT(*) AS filas
    FROM precios p
    JOIN Dim_Par d ON p.Par_ID = d.Par_ID
    GROUP BY d.Tipo
"""
for tipo, filas in cur.execute(consulta):
    print(f"  {tipo:<11} {filas}")

conn.close()
print(f"\nBase de datos creada: {DB}")
