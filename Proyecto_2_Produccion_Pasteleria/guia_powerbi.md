# Guía Power BI — Dashboard de Merma (Pastelería)

Guía paso a paso para construir, desde cero, el dashboard que cuenta la historia del análisis: **la merma se gobierna por el tamaño del lote**. Sígue los pasos a tu ritmo; las fórmulas DAX están listas para copiar y pegar.

---

## 0. Qué vamos a construir

Una sola página de Power BI con cuatro zonas:

1. **Fila de KPIs** (arriba): merma total, merma por 100 unidades, % de lotes pequeños, ahorro potencial.
2. **Gráfico héroe**: merma por unidad según el tamaño del lote (el hallazgo central).
3. **Gráfico de apoyo**: dispersión tamaño de lote vs merma/unidad.
4. **Contexto**: tendencia mensual + cortes planos por turno/familia (para mostrar que *ahí* no está el problema).

Más una columna de **filtros** (slicers): fecha, turno, familia, producto. Y dos cajas de texto con las **conclusiones** (What / So What / Now What).

---

## 1. Conectar Power BI a la base SQLite (vía ODBC)

Power BI no lee SQLite directamente; usamos el puente ODBC que ya tienes configurado.

1. Abre **Power BI Desktop**.
2. Cinta **Inicio → Obtener datos → Más…**
3. En el buscador escribe `ODBC` → selecciona **ODBC** → **Conectar**.
4. En "Nombre del origen de datos (DSN)" elige tu DSN (`PasteleriaDB`) → **Aceptar**.
5. Si pide credenciales, deja **Predeterminado o personalizado** → **Conectar**.
6. En el **Navegador** marca las dos tablas: `Dim_Producto` y `produccion` → **Cargar**.

> Si no aparecen las tablas: revisa que el DSN apunte al archivo `produccion_pasteleria.db` correcto y que tengas instalado el **SQLite3 ODBC Driver** (el del "3").

**Importación vs DirectQuery:** elige **Importar** (predeterminado). Es más rápido y suficiente para este volumen (3.820 filas). DirectQuery solo si necesitaras datos en vivo.

---

## 2. Modelar la relación

1. Ve a la vista **Modelo** (icono de tablas conectadas, barra izquierda).
2. Verás las dos tablas. Si Power BI no creó la relación solo, arrástrala:
   - Desde `Dim_Producto[Producto_ID]` hacia `produccion[Producto_ID]`.
3. Verifica que la relación sea **1 a muchos** (`Dim_Producto` 1 → `produccion` *), con dirección de filtro **única**. Doble clic en la línea para revisarlo.

Esto permite filtrar la producción por `Familia_Preparacion` y `Producto`, que viven en la dimensión.

---

## 3. Crear las medidas y la columna de tamaño de lote (DAX)

DAX es el lenguaje de cálculo de Power BI. Una **medida** se recalcula según los filtros del visual; una **columna calculada** se calcula fila por fila y se guarda en la tabla.

### 3.1 Columna calculada: rango de tamaño de lote

La necesitamos para el gráfico héroe. En la vista **Datos**, selecciona la tabla `produccion` → cinta **Herramientas de tabla → Nueva columna** → pega:

```DAX
Rango_Lote =
SWITCH(
    TRUE(),
    produccion[Unidades_Producidas] <= 15, "1-15",
    produccion[Unidades_Producidas] <= 25, "16-25",
    produccion[Unidades_Producidas] <= 35, "26-35",
    produccion[Unidades_Producidas] <= 45, "36-45",
    "46+"
)
```

> Para que las barras salgan ordenadas (1-15, 16-25, …) y no alfabéticas: selecciona la columna `Rango_Lote` → **Ordenar por columna** → elige una columna numérica auxiliar. La forma simple: crea otra columna `Orden_Lote` con el mismo SWITCH pero devolviendo 1,2,3,4,5, y ordena `Rango_Lote` por ella.

```DAX
Orden_Lote =
SWITCH(
    TRUE(),
    produccion[Unidades_Producidas] <= 15, 1,
    produccion[Unidades_Producidas] <= 25, 2,
    produccion[Unidades_Producidas] <= 35, 3,
    produccion[Unidades_Producidas] <= 45, 4,
    5
)
```

### 3.2 Medidas base

Crea cada una con **Herramientas de tabla → Nueva medida** (sobre `produccion`). Pega una a una:

```DAX
Unidades Producidas = SUM(produccion[Unidades_Producidas])
```

```DAX
Merma Total (kg) = SUM(produccion[Merma_Kg])
```

```DAX
Merma por 100u =
DIVIDE([Merma Total (kg)], [Unidades Producidas]) * 100
```

`DIVIDE` evita el error de dividir por cero. Este es tu **KPI principal**: kg de merma por cada 100 unidades.

### 3.3 Medidas de la oportunidad de negocio

```DAX
N Lotes = DISTINCTCOUNT(produccion[Lote_ID])
```

```DAX
N Lotes Pequenos =
CALCULATE([N Lotes], produccion[Unidades_Producidas] < 26)
```

```DAX
% Lotes Pequenos =
DIVIDE([N Lotes Pequenos], [N Lotes])
```
(Formatéala como porcentaje: selecciona la medida → **Formato → %**.)

```DAX
Ahorro Potencial (kg) =
VAR EficienciaGrande = 0.029   -- kg de merma por unidad en lotes de 46+ (2,9 / 100)
VAR MermaActualPeq =
    CALCULATE([Merma Total (kg)], produccion[Unidades_Producidas] < 26)
VAR UnidadesPeq =
    CALCULATE([Unidades Producidas], produccion[Unidades_Producidas] < 26)
VAR MermaIdeal = UnidadesPeq * EficienciaGrande
RETURN
    MermaActualPeq - MermaIdeal
```

Esta medida estima cuánta merma se evitaría si los lotes pequeños (<26 u) se produjeran a la eficiencia de los grandes. Con los datos actuales da **≈1.250 kg/año**.

---

## 4. Construir los visuales

En la vista **Informe**. Cada visual: clic en un tipo en el panel **Visualizaciones**, luego arrastra campos a sus huecos.

### 4.1 Fila de tarjetas KPI (arriba)

Cuatro visuales tipo **Tarjeta** (card), uno por medida:

| Tarjeta | Campo |
|---|---|
| Merma total | `Merma Total (kg)` |
| Merma por 100u | `Merma por 100u` |
| % lotes pequeños | `% Lotes Pequenos` |
| Ahorro potencial | `Ahorro Potencial (kg)` |

Ponlas en fila arriba. Renómbralas con títulos claros (panel **Formato → Título**).

### 4.2 Gráfico héroe — merma por unidad según tamaño de lote

- Tipo: **Gráfico de columnas agrupadas** (barras verticales).
- **Eje X**: `Rango_Lote` (ordenado por `Orden_Lote`, paso 3.1).
- **Eje Y**: `Merma por 100u`.
- Activa **etiquetas de datos** (Formato → Etiquetas de detalles) para ver 12,6 / 7,5 / 5,0 / 3,9 / 2,9.
- Título: "Lotes pequeños desperdician 4,3x más por unidad".
- Truco visual: en **Formato → Columnas → colores**, pon el rango 1-15 en rojo/coral y 46+ en verde, para que la historia se vea sola.

### 4.3 Dispersión — tamaño vs merma por unidad

- Tipo: **Gráfico de dispersión** (scatter).
- **Eje X**: `Unidades_Producidas` (resumen: No resumir).
- **Eje Y**: una medida de merma por unidad por lote. La más simple: arrastra `Merma_Kg` y `Unidades_Producidas` y pon **Detalles** = `Lote_ID` para que cada punto sea un lote.
- Verás la nube cayendo en forma de curva: confirma visualmente la relación −0,60.

### 4.4 Tendencia mensual

- Tipo: **Gráfico de líneas**.
- **Eje X**: `Fecha_Produccion` (Power BI crea jerarquía Año/Mes; usa el nivel **Mes**).
- **Eje Y**: `Merma por 100u`.
- Sirve para mostrar que la merma es estable en el tiempo (≈4,2–4,9), sin picos raros.

### 4.5 Cortes planos (apoyo)

Dos **gráficos de barras** pequeños:
- Por turno: Eje = `Turno`, Valor = `Merma por 100u`.
- Por familia: Eje = `Familia_Preparacion`, Valor = `Merma por 100u`.

Salen casi iguales a propósito: demuestran que el problema **no** está ahí.

### 4.6 Filtros (slicers)

Cuatro visuales tipo **Segmentación de datos** (slicer):
- `Fecha_Produccion` (estilo "entre" / rango).
- `Turno`.
- `Familia_Preparacion`.
- `Producto`.

Colócalos en una columna a la izquierda o en una barra superior. Filtran todos los visuales a la vez.

---

## 5. Conclusiones en el dashboard (storytelling)

Agrega **cuadros de texto** (cinta **Insertar → Cuadro de texto**) con la estructura del portafolio:

- **What:** "La merma (5.841 kg/año) no depende del turno, la familia ni el producto — esos cortes son planos."
- **So What:** "El 32% de los lotes se hornean pequeños (<26 u) y generan el 32% de toda la merma, por un costo fijo de ~1,53 kg por lote."
- **Now What:** "Consolidar los lotes pequeños ahorraría ~1.250 kg/año (21% del desperdicio)."

Tip de diseño: un título grande arriba ("¿Dónde perdemos más producto, y por qué?") y las conclusiones en una franja al pie.

---

## 6. Guardar y exportar

- **Guardar:** `Archivo → Guardar como` → guarda el `.pbix` en la carpeta del proyecto.
- **Para el portafolio:** `Archivo → Exportar → PDF` genera una versión que puedes adjuntar sin que abran Power BI. O publica en **Power BI Service** (cuenta gratuita) para un enlace web.

---

## Resumen de fórmulas (copiar rápido)

| Medida | Para qué |
|---|---|
| `Merma por 100u` | KPI principal |
| `% Lotes Pequenos` | Tamaño del problema |
| `Ahorro Potencial (kg)` | La recomendación, cuantificada |
| `Rango_Lote` (columna) | Eje del gráfico héroe |

Cualquier duda con un paso concreto, dime en cuál te trabaste y lo vemos juntos en pantalla.
