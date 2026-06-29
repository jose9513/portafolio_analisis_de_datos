"""
Demo didáctica: ¿por qué los precios de divisas son un RANDOM WALK
y no filas independientes como en la pastelería?

Concepto central: el precio de hoy NACE del de ayer.
    precio_hoy = precio_ayer * (1 + retorno_aleatorio)

Tres ideas:
  - Trabajamos con RETORNOS (% de cambio), no con niveles.
  - El retorno tiene media 0 (no sabemos si sube/baja) y una desviación
    que ES la volatilidad (qué tan grande es el movimiento típico).
  - El precio se ACUMULA día a día (np.cumprod).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ----- 1) Versión mínima: el concepto en un bucle -----
def random_walk_basico(precio_inicial=1.10, dias=5, volatilidad=0.005, semilla=42):
    np.random.seed(semilla)
    precio = precio_inicial
    print(f"Arranca en {precio}\n")
    for dia in range(1, dias + 1):
        retorno = np.random.normal(0, volatilidad)   # cambio % diario
        precio = precio * (1 + retorno)              # hoy nace de ayer
        print(f"Día {dia}: retorno={retorno:+.3%}  ->  precio={precio:.4f}")
    return precio


# ----- 2) Versión vectorizada: una serie completa de golpe -----
def serie_random_walk(precio_inicial=1.10, dias=500, volatilidad=0.005, semilla=7):
    np.random.seed(semilla)
    retornos = np.random.normal(0, volatilidad, dias)
    return precio_inicial * np.cumprod(1 + retornos)   # acumular multiplicando


# ----- 3) El contraste: independiente (mal) vs random walk (bien) -----
def comparar(dias=500, base=1.10, semilla=7):
    np.random.seed(semilla)
    independiente = base + np.random.normal(0, 0.02, dias)   # sin memoria
    retornos = np.random.normal(0, 0.005, dias)
    walk = base * np.cumprod(1 + retornos)                   # con memoria

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5), sharey=True)
    ax1.plot(independiente, color="#C0392B", lw=0.9)
    ax1.set_title("MAL: días independientes (sin memoria)", fontweight="bold")
    ax1.set_xlabel("día"); ax1.set_ylabel("precio"); ax1.grid(alpha=.2)
    ax2.plot(walk, color="#1D9E75", lw=1.1)
    ax2.set_title("BIEN: random walk (cada día nace del anterior)", fontweight="bold")
    ax2.set_xlabel("día"); ax2.grid(alpha=.2)
    plt.tight_layout()
    plt.savefig("demo_random_walk.png", dpi=120, bbox_inches="tight")
    print("Gráfico guardado en demo_random_walk.png")


if __name__ == "__main__":
    random_walk_basico()
    print()
    comparar()
