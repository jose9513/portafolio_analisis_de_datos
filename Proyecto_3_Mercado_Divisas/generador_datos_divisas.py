"""
Generador de datos sinteticos del mercado de divisas.
Se construye por BLOQUES.

BLOQUE 1 - El catalogo de pares (Dim_Par)
BLOQUE 2 - El calendario de dias habiles
BLOQUE 3 - El motor random walk (precio de Cierre por par)
BLOQUE 4 - Aplicar el motor a los 8 pares
BLOQUE 5 - Derivar el OHLC (Apertura, Maximo, Minimo) desde el Cierre
"""

import numpy as np
import pandas as pd

# ====================================================================
# BLOQUE 1 - El catalogo de pares (Dim_Par)
# ====================================================================
pares = [
    {"Par": "EUR/USD", "Moneda_Base": "EUR", "Moneda_Cotizada": "USD",
     "Tipo": "Major", "Region": "Europa", "Precio_Inicial": 1.08, "Volatilidad_Diaria": 0.004},
    {"Par": "GBP/USD", "Moneda_Base": "GBP", "Moneda_Cotizada": "USD",
     "Tipo": "Major", "Region": "Reino Unido", "Precio_Inicial": 1.27, "Volatilidad_Diaria": 0.005},
    {"Par": "USD/JPY", "Moneda_Base": "USD", "Moneda_Cotizada": "JPY",
     "Tipo": "Major", "Region": "Japon", "Precio_Inicial": 150.0, "Volatilidad_Diaria": 0.005},
    {"Par": "AUD/USD", "Moneda_Base": "AUD", "Moneda_Cotizada": "USD",
     "Tipo": "Commodity", "Region": "Australia", "Precio_Inicial": 0.66, "Volatilidad_Diaria": 0.006},
    {"Par": "USD/CAD", "Moneda_Base": "USD", "Moneda_Cotizada": "CAD",
     "Tipo": "Commodity", "Region": "Canada", "Precio_Inicial": 1.36, "Volatilidad_Diaria": 0.005},
    {"Par": "USD/MXN", "Moneda_Base": "USD", "Moneda_Cotizada": "MXN",
     "Tipo": "Emergente", "Region": "Mexico", "Precio_Inicial": 17.5, "Volatilidad_Diaria": 0.008},
    {"Par": "USD/BRL", "Moneda_Base": "USD", "Moneda_Cotizada": "BRL",
     "Tipo": "Emergente", "Region": "Brasil", "Precio_Inicial": 5.00, "Volatilidad_Diaria": 0.011},
    {"Par": "USD/COP", "Moneda_Base": "USD", "Moneda_Cotizada": "COP",
     "Tipo": "Emergente", "Region": "Colombia", "Precio_Inicial": 3950.0, "Volatilidad_Diaria": 0.009},
]
dim_par = pd.DataFrame(pares)

# ====================================================================
# BLOQUE 2 - El calendario de dias habiles
# ====================================================================
FECHA_INICIO = "2024-01-01"
FECHA_FIN = "2025-12-31"
fechas = pd.bdate_range(start=FECHA_INICIO, end=FECHA_FIN)

# ====================================================================
# BLOQUE 3 - El motor random walk (un par): genera el Cierre
# ====================================================================
def simular_precios(precio_inicial, volatilidad, n_dias, semilla=None):
    if semilla is not None:
        np.random.seed(semilla)
    retornos = np.random.normal(0, volatilidad, n_dias)
    precios = precio_inicial * np.cumprod(1 + retornos)
    return precios

# ====================================================================
# BLOQUE 4 + 5 - Aplicar el motor a los 8 pares y derivar el OHLC
#   Apertura = cierre del dia anterior (el dia 1 abre en su precio inicial)
#   Maximo   = el mayor de (apertura, cierre) + una "mecha" hacia arriba
#   Minimo   = el menor de (apertura, cierre) - una "mecha" hacia abajo
#   La mecha es proporcional a la volatilidad del par.
# ====================================================================
def generar_precios(semilla=42):
    np.random.seed(semilla)
    n = len(fechas)
    frames = []
    for fila in dim_par.itertuples():
        vol = fila.Volatilidad_Diaria
        cierre = simular_precios(fila.Precio_Inicial, vol, n)

        # Apertura: hoy abre donde cerro ayer
        apertura = np.empty(n)                 # array vacio del tamano correcto
        apertura[0] = fila.Precio_Inicial      # el primer dia no tiene "ayer"
        apertura[1:] = cierre[:-1]             # del 2o dia en adelante: cierre de ayer

        # Maximo / Minimo a partir del cuerpo de la vela (apertura-cierre)
        base_alta = np.maximum(apertura, cierre)   # el mayor de los dos, dia a dia
        base_baja = np.minimum(apertura, cierre)   # el menor de los dos, dia a dia
        maximo = base_alta * (1 + np.random.uniform(0, vol, n))  # mecha hacia arriba
        minimo = base_baja * (1 - np.random.uniform(0, vol, n))  # mecha hacia abajo

        df_par = pd.DataFrame({
            "Fecha": fechas,
            "Par": fila.Par,
            "Apertura": apertura,
            "Maximo": maximo,
            "Minimo": minimo,
            "Cierre": cierre,
        })
        frames.append(df_par)
    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    precios = generar_precios()

    print("Tabla 'precios' con OHLC (primeras filas de EUR/USD):")
    print(precios.head().round(4).to_string(index=False))
    print(f"\nForma: {precios.shape[0]} filas x {precios.shape[1]} columnas")

    # VERIFICACION: la ley de hierro del OHLC debe cumplirse SIEMPRE
    cuerpo_alto = precios[["Apertura", "Cierre"]].max(axis=1)
    cuerpo_bajo = precios[["Apertura", "Cierre"]].min(axis=1)
    ok_max = (precios["Maximo"] >= cuerpo_alto).all()
    ok_min = (precios["Minimo"] <= cuerpo_bajo).all()
    print("\nVerificacion ley OHLC:")
    print(f"  Maximo siempre >= apertura y cierre: {ok_max}")
    print(f"  Minimo siempre <= apertura y cierre: {ok_min}")
