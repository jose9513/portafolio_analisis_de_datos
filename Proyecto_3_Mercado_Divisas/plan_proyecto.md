# Plan del proyecto — Análisis del mercado de divisas (Research)

> Documento de referencia. Se escribe ANTES de codificar: primero la decisión y las hipótesis, después los datos. (Playbook: "empieza por la decisión, no por las columnas".)

## Ángulo elegido

**Research / analista de mercado.** Producir insight para que un inversor, tesorería o estratega entienda el riesgo y el comportamiento del mercado de divisas. Datos sintéticos (fake), con fines de aprendizaje y portafolio. No es asesoría de inversión.

## Decisión que informa

Ayudar a entender: qué divisas son más riesgosas (volatilidad), cuáles se mueven juntas (diversificación) y qué patrones temporales muestran.

## Pregunta central

*"¿Cómo se comportan las principales divisas — cuáles son más volátiles, cómo se relacionan entre sí, y qué patrones temporales muestran?"*

## Hipótesis a explorar (definen qué datos necesito)

1. Unos pares son mucho más volátiles que otros (emergentes > majors).
2. Ciertos pares se mueven juntos (EUR/USD y GBP/USD deberían correlacionar fuerte).
3. Hay regímenes: periodos de calma y de turbulencia agrupados (volatility clustering), no repartidos al azar.
4. Puede haber estacionalidad o efecto día de la semana.
5. El dólar como factor común: cuando el USD se fortalece, varios pares reaccionan a la vez.

## Esquema de datos (modelo en estrella)

**`Dim_Par`** — dimensión de pares:
- `Par` (ej. "EUR/USD")
- `Moneda_Base`, `Moneda_Cotizada`
- `Tipo` ("Major" / "Commodity" / "Emergente") ← clave para la hipótesis 1
- `Region`

**`precios`** — hechos, una fila por par y día:
- `Fecha`
- `Par` (FK)
- `Apertura`, `Maximo`, `Minimo`, `Cierre` (OHLC)
- `Volumen` (sintético, opcional)

Pares: EUR/USD, GBP/USD, USD/JPY (majors); AUD/USD, USD/CAD (commodity); USD/MXN, USD/BRL, USD/COP (emergentes). ~2 años de días hábiles ≈ 8.000 filas.

## Concepto técnico central

Los precios NO son filas independientes y aleatorias (como los lotes de la pastelería). Son una **caminata aleatoria (random walk)**: cada precio depende del anterior. Para que el dato sintético sea realista hay que reproducir:

- **Retornos, no niveles** — se simula el % de cambio diario y se acumula para formar el precio.
- **Volatility clustering** — la volatilidad viene en rachas → crea los regímenes (hipótesis 3).
- **Correlaciones** — un "shock del dólar" común hace que varios pares se muevan juntos (hipótesis 5).

## Stack

Python (`numpy`, `pandas`), SQLite, Power BI. Mismo flujo que proyectos anteriores: generar datos → CSV → SQLite → Power BI → análisis con storytelling.

## Estado

- [x] Plan definido
- [ ] Entender el random walk (demo)
- [ ] Generador de datos sintéticos
- [ ] Carga a SQLite
- [ ] EDA y prueba de hipótesis
- [ ] Dashboard + storytelling
