"""
Generador de datos sinteticos del mercado de divisas.
Se construye por BLOQUES.

BLOQUE 1 - El catalogo de pares (Dim_Par)
BLOQUE 2 - El calendario de dias habiles
BLOQUE 3 - El motor random walk (precio de Cierre por par)
BLOQUE 4 - Aplicar el motor a los 8 pares
BLOQUE 5 - Derivar el OHLC (Apertura, Maximo, Minimo) desde el Cierre
BLOQUE 6 - Volumen sintetico (mas alto en dias de mayor movimiento)
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
# BLOQUE 4 + 5 + 6 - Aplicar el motor a los 8 pares, derivar OHLC y volumen
#   OHLC: apertura = cierre de ayer; maximo/minimo = cuerpo +/- mecha
#   Volumen = base * (amplificado por el rango del dia) * ruido aleatorio
#             -> dias mas agitados tienen mas volumen (es una RELACION, no azar puro)
# ====================================================================
VOLUMEN_BASE = 1_000_000

def generar_precios(semilla=42):
    np.random.seed(semilla)
    n = len(fechas)
    frames = []
    for fila in dim_par.itertuples():
        vol = fila.Volatilidad_Diaria
        cierre = simular_precios(fila.Precio_Inicial, vol, n)

        # OHLC
        apertura = np.empty(n)
        apertura[0] = fila.Precio_Inicial
        apertura[1:] = cierre[:-1]
        base_alta = np.maximum(apertura, cierre)
        base_baja = np.minimum(apertura, cierre)
        maximo = base_alta * (1 + np.random.uniform(0, vol, n))
        minimo = base_baja * (1 - np.random.uniform(0, vol, n))

        # Volumen
        rango = (maximo - minimo) / apertura          # que tan agitado estuvo el dia (en %)
        ruido = np.random.uniform(0.7, 1.3, n)        # variacion aleatoria +-30%
        volumen = (VOLUMEN_BASE * (1 + 50 * rango) * ruido).astype(int)  # operaciones = enteros

        df_par = pd.DataFrame({
            "Fecha": fechas,
            "Par": fila.Par,
            "Apertura": apertura,
            "Maximo": maximo,
            "Minimo": minimo,
            "Cierre": cierre,
            "Volumen": volumen,
        })
        frames.append(df_par)
    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    precios = generar_precios()

    print("Tabla 'precios' completa (primeras filas de EUR/USD):")
    print(precios.head().round(4).to_string(index=False))
    print(f"\nForma: {precios.shape[0]} filas x {precios.shape[1]} columnas")

    # VERIFICACION 1: ley de hierro del OHLC
    cuerpo_alto = precios[["Apertura", "Cierre"]].max(axis=1)
    cuerpo_bajo = precios[["Apertura", "Cierre"]].min(axis=1)
    print("\nVerificacion OHLC:")
    print(f"  Maximo >= cuerpo siempre: {(precios['Maximo'] >= cuerpo_alto).all()}")
    print(f"  Minimo <= cuerpo siempre: {(precios['Minimo'] <= cuerpo_bajo).all()}")

    # VERIFICACION 2: el volumen debe subir en dias de mayor movimiento
    rango_check = (precios["Maximo"] - precios["Minimo"]) / precios["Apertura"]
    corr = rango_check.corr(precios["Volumen"])
    print(f"\nCorrelacion rango-del-dia vs volumen (debe ser positiva): {corr:.3f}")
