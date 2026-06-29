# Guía de diseño — Dashboard de Merma

El orden importa: estos pasos están ordenados de **mayor a menor impacto visual**. Si solo tuvieras 20 minutos, haz del 1 al 4 y ya se ve otra cosa. La regla de oro de todo dashboard ejecutivo: **una pantalla, una historia, cero ruido**.

---

## 1. Cuadrícula y alineación (lo que más se nota)

El 80% de la sensación "amateur vs profesional" es alineación. Un dashboard ordenado en una rejilla invisible se ve serio aunque los colores sean simples.

- Define una rejilla mental de zonas: franja de **título** arriba, fila de **KPIs** debajo, bloque de **gráficos** en el centro, columna de **filtros** a un lado.
- Selecciona cada visual y usa el panel **Formato → General → Propiedades → Posición y tamaño** para darles valores redondos (ej. ancho 400, alto 280) y que coincidan entre sí. Dos gráficos de la misma fila deben tener exactamente el mismo alto.
- Activa **Ver → Mostrar cuadrícula** y **Ajustar a cuadrícula** para que todo encaje solo.
- Deja **márgenes iguales** entre visuales (ej. 16 px). El aire uniforme es lo que da elegancia.

## 2. Limpia los títulos y los nombres de campo

Ahora mismo tienes títulos automáticos feos como "Suma de Unidades_Producidas y Suma de Merma_Kg por Lote_ID". Eso grita "sin terminar".

- En cada visual: **Formato → General → Título** → escribe un título humano y con intención:
  - Héroe: "Los lotes pequeños desperdician 4,3x más por unidad"
  - Scatter: "Cuanto más grande el lote, menos merma por unidad"
  - Mes: "La merma es estable todo el año (sin picos)"
  - Turno / Familia: "El turno no explica la merma" / "La familia tampoco"
- Renombra las medidas para que no salga "Suma de": doble clic en el campo y quita el "Merma_Kg" técnico, o usa medidas con nombre limpio (ya tienes `Merma por 100u`). Un buen título dice la **conclusión**, no la fórmula.

## 3. Disciplina de color (menos es más)

- Elige **un color de marca** (un azul o un verdoso) para casi todo, y **reserva un color de alerta** (rojo/coral) solo para lo que importa.
- En el gráfico héroe, mantén el truco que ya tienes: barra **1-15 en rojo/coral** (el problema) y **46+ en verde** (la meta), el resto en gris/azul neutro. Que el color cuente la historia.
- Los gráficos "planos" (turno, familia) ponlos en **gris** a propósito: visualmente dicen "aquí no pasa nada", que es justo el mensaje.
- Nunca uses más de 2–3 colores con significado. El arcoíris es enemigo de lo profesional.

## 4. Tipografía y formato de números

- Una sola tipografía en todo (la predeterminada Segoe UI está bien). Varía solo **tamaño y peso**, no la fuente.
- Formatea los números: `Merma por 100u` con **1 decimal**; `% Lotes Pequenos` como **porcentaje**; `Ahorro Potencial` con separador de miles y "kg". Se hace en **Herramientas de medida → Formato**.
- Quita decimales innecesarios de los ejes (3,9 mejor que 3,8765).

## 5. Fila de KPIs arriba (el gancho de 3 segundos)

Un jefe mira 3 segundos. Dale los números clave de inmediato con 3–4 **tarjetas** en una fila superior:

- Merma total (kg/año) · Merma por 100u · % lotes pequeños · **Ahorro potencial (kg)**
- Pon la tarjeta de **Ahorro potencial** destacada (fondo de color suave) — es tu "gran número", el que justifica todo el dashboard.

## 6. Quita el ruido (declutter)

- **Apaga las líneas de cuadrícula** y los ejes que no aporten (Formato → Eje Y → desactivar, o quitar líneas).
- Quita bordes gruesos por defecto; usa **fondos de tarjeta** sutiles con esquina redondeada (Formato → Efectos → Fondo + Bordes redondeados).
- Menos etiquetas: si las barras ya tienen etiqueta de dato, no necesitas también el eje Y.

## 7. Título y narrativa de la página

- Arriba del todo, un **cuadro de texto** grande con la pregunta de negocio: **"¿Dónde perdemos más producto, y por qué?"** Eso enmarca todo y se ve intencional.
- Al pie o en un lateral, tres cuadros de texto cortos con tu storytelling **What / So What / Now What** (ya los tienes redactados en `analisis_negocio.md`). Una frase cada uno.

## 8. Aplica un tema (atajo de 1 clic)

- **Ver → Temas → Examinar temas** y aplica uno limpio, o descarga un tema `.json` minimalista. Un buen tema unifica colores y fuentes de golpe y te ahorra el 5 y 6 a mano.
- Evita los temas con muchos colores vivos; busca paletas sobrias (grises + 1 acento).

## 9. Fondo y respiración

- Fondo de página en **gris muy claro** (no blanco puro) y los visuales en tarjetas blancas: ese contraste sutil es el look "dashboard moderno".
- Deja espacio en blanco. No llenes cada hueco; el aire transmite control.

---

## Orden recomendado para esta noche

1. Aplica un **tema limpio** (paso 8) — punto de partida instantáneo.
2. **Alinea y dimensiona** todo en la rejilla (paso 1).
3. **Reescribe los títulos** con la conclusión (paso 2).
4. Añade la **fila de KPIs** y destaca el ahorro (paso 5).
5. Ajusta **color y formato de números** (pasos 3 y 4).
6. **Quita ruido** y añade **título + conclusiones** (pasos 6 y 7).

Con eso pasa de "hoja de trabajo" a algo que un jefe mira y entiende en 10 segundos. Si quieres, mañana te genero un archivo de **tema .json** a medida (paleta pastelería: crema + un acento) para que lo apliques de un clic.
