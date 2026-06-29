# Cómo pensar como analista de datos — Playbook

Un marco mental para crear y moldear cualquier proyecto de datos desde cero. No es una receta fija; es una forma de mirar. Vale para una pastelería, para ventas de retail, para divisas o para lo que se te ocurra.

> La frase que resume todo el oficio: **"¿Comparado con qué?"** Un número solo no dice nada. 4,3 kg de merma no es bueno ni malo hasta que lo comparas con otro turno, con otro mes, con otro tamaño de lote, o con una meta. El analista vive en las comparaciones.

---

## 0. El cambio de mentalidad clave

El principiante empieza por **los datos** ("tengo esta tabla, ¿qué grafico?"). El analista empieza por **la decisión** ("¿qué va a hacer alguien distinto según lo que encuentre?").

Si un análisis no puede cambiar ninguna decisión, es trivia, no análisis. Antes de tocar una columna, pregúntate: *¿quién usaría esto y qué haría con la respuesta?* En la pastelería: el jefe de producción decide cuántas unidades hornear por tanda. Esa decisión es el norte de todo.

---

## 1. El esqueleto: ciclo de vida de cualquier proyecto

Todo proyecto recorre estas etapas. No es lineal — vas y vuelves — pero esta es la columna vertebral:

1. **Pregunta de negocio** — ¿qué decisión queremos informar?
2. **Conseguir y entender los datos** — qué hay, qué significa cada columna, de dónde viene.
3. **Limpiar** — tipos, nulos, duplicados, codificación, unidades.
4. **Explorar (EDA)** — distribuciones, conteos, rangos; conocer el terreno.
5. **Buscar relaciones (iterar)** — hipótesis → cortar → mirar → refinar. *Aquí está el 70% del trabajo real.*
6. **Validar** — ¿el hallazgo es real o es ruido/sesgo? Re-verifica.
7. **Comunicar** — storytelling para una audiencia concreta.
8. **Recomendar** — qué hacer, cuantificado.

La parte que te "salté" fue la 5. A eso le dedico la sección 3.

---

## 2. Los cuatro tipos de pregunta (te da el nivel de ambición)

Cualquier análisis cae en uno de estos niveles, de menos a más valioso:

- **Descriptivo — ¿qué pasó?** Totales, promedios, tendencias. ("La merma fue 5.841 kg.")
- **Diagnóstico — ¿por qué pasó?** Segmentar, correlacionar, comparar. ("La merma sube cuando el lote es pequeño.")
- **Predictivo — ¿qué va a pasar?** Modelos, proyecciones. ("Si seguimos así, el próximo trimestre...")
- **Prescriptivo — ¿qué deberíamos hacer?** Recomendación con impacto. ("Consolidar lotes ahorra 1.250 kg.")

Truco: **empieza descriptivo para conocer el terreno, pero apunta siempre a llegar a prescriptivo.** Un portafolio que solo describe ("aquí hay un gráfico de ventas") aburre. Uno que recomienda ("aquí está dónde pierdes dinero y cuánto recuperarías") contrata.

---

## 3. El bucle de exploración: cómo se encuentran relaciones de verdad

Esta es la parte de prueba y error. Es un **bucle**, no una línea recta. Lo repites decenas de veces:

```
Hipótesis  →  Cortar/segmentar  →  Mirar  →  ¿"y qué"?  →  Refinar o descartar
     ↑                                                              │
     └──────────────────────────────────────────────────────────────┘
```

1. **Forma una hipótesis ingenua.** "Sospecho que el turno noche tiene más merma." No tiene que ser correcta — la mayoría no lo serán, y eso está bien.
2. **Córtala.** Agrupa la métrica por esa dimensión (merma por turno).
3. **Mírala con honestidad.** ¿Hay diferencia real o es plana? En la pastelería: turno y familia salieron **planos**. Un principiante se frustra; el analista se alegra: *descartar una hipótesis también es información.* Acabas de aprender que el problema NO está ahí.
4. **Pregunta "¿y qué?".** Si encontraste algo, ¿cambia una decisión? Si no, sigue.
5. **Refina.** Los callejones sin salida te empujan a la siguiente hipótesis. "No es el turno... ni la familia... ni el producto... ¿qué tienen en común los lotes con más merma por unidad? Ah — son los pequeños." Ese salto solo aparece **después** de descartar lo obvio.

**La clave que casi nadie te dice:** los hallazgos buenos casi siempre llegan *después* de varias hipótesis muertas. El camino de prueba y error no es ineficiencia — es el método. Cuando yo te di la respuesta "en un segundo", me salté esos 8 callejones sin salida que son donde tú entrenas la intuición.

---

## 4. Las lentes: ángulos para interrogar cualquier dataset

Cuando no sabes por dónde empezar a explorar, pásale estas lentes a CUALQUIER conjunto de datos. Cada una revela un tipo distinto de patrón:

- **Tiempo** — ¿cómo cambia mes a mes, día a día, por estación? ¿Hay picos, caídas, ciclos?
- **Segmento/categoría** — ¿difiere por producto, región, cliente, canal, turno?
- **Normalización (ratios)** — *la lente más poderosa.* No compares totales, compara tasas: merma **por unidad**, ventas **por m²**, costo **por pedido**. Los totales engañan; los ratios revelan. (Todo el hallazgo de la pastelería vive aquí.)
- **Distribución** — no mires solo el promedio. ¿Está concentrado o disperso? ¿Hay una cola larga? El promedio esconde historias.
- **Outliers** — ¿quiénes son los casos extremos y por qué? A veces el outlier ES la historia.
- **Concentración (Pareto)** — ¿el 20% de X explica el 80% de Y? (El 32% de lotes generaba el 32% de la merma — y el problema se concentraba en los pequeños.)
- **Embudo (funnel)** — para procesos: ¿dónde se cae la gente entre paso y paso?
- **Cohorte** — agrupa por momento de entrada (clientes que llegaron en enero vs marzo) y sigue su comportamiento.
- **Correlación** — ¿dos variables se mueven juntas? (Cuidado: correlación ≠ causa.)
- **Benchmark/meta** — ¿comparado con un objetivo, con la competencia, con el mejor del grupo?

Pásale 4–5 de estas lentes a tus datos y casi siempre salta algo.

---

## 5. Hábitos y trampas del analista

Lo que separa un análisis confiable de uno que engaña:

- **Normaliza antes de comparar.** Un producto con más merma total puede ser simplemente el que más se produce. Divide.
- **Correlación no es causa.** Que dos cosas suban juntas no significa que una cause la otra. Puede haber una tercera variable.
- **Cuidado con la paradoja de Simpson.** Una tendencia puede invertirse al agrupar/desagrupar. Mira a varios niveles.
- **Base rate / "¿comparado con qué?"** Un 5% de algo no es alto ni bajo sin contexto.
- **Sesgo de supervivencia.** ¿Faltan datos de los casos que "no llegaron"? (Clientes que se fueron, lotes que se descartaron.)
- **El promedio miente.** Acompáñalo siempre de la dispersión o la distribución.
- **Verifica con un método independiente.** En la pastelería re-sumé los datos sin pandas para confirmar. Si solo lo calculaste de una forma, no lo sabes aún.
- **Desconfía de tu hallazgo favorito.** El que más te emociona es el que más debes intentar tumbar.

---

## 6. Cómo inventar proyectos desde cero (generar ideas)

Para un portafolio, tú creas el proyecto entero. Dos caminos:

**A) Desde un dominio que te interesa** (pastelería, fútbol, música, videojuegos):
1. Elige el dominio.
2. Imagina quién toma decisiones ahí (dueño, entrenador, jefe de producción).
3. Lista 3 decisiones reales que esa persona enfrenta.
4. Define qué datos necesitarías para informarlas.
5. Genera datos sintéticos realistas (como hicimos) o busca datasets públicos (Kaggle, datos.gob, etc.).

**B) Desde una técnica que quieres demostrar** (modelo estrella, cohortes, forecasting):
1. Elige la técnica.
2. Busca un dominio donde esa técnica sea natural.
3. Construye el dataset mínimo que la luzca.

**Para que un proyecto de portafolio impresione**, asegúrate de que demuestre: (1) que entiendes el negocio, no solo el código; (2) que sabes limpiar y modelar datos; (3) que llegas a una **recomendación cuantificada**, no solo a gráficos; (4) que lo comunicas con una historia clara. Eso es lo que un reclutador busca.

**Ideas de variación para tus datos de pastelería** (mismo dataset, ángulos nuevos):
- Añade **costo de materia prima** → convierte la merma en $ y calcula el ahorro en dinero, no en kg. (Mucho más persuasivo para un jefe.)
- Añade **demanda/ventas** → analiza sobreproducción vs faltantes.
- Simula **estacionalidad** real (más torta en diciembre) → análisis de planificación.
- Modela **un segundo año** → compara año contra año, mide si una mejora funcionó.

---

## 7. Comunicar: moldear la historia para la audiencia

El mismo análisis se cuenta distinto según quién escucha:

- **Para un ejecutivo:** una pantalla, el gran número arriba, la recomendación en una frase. Estructura **What / So What / Now What**.
- **Para un equipo técnico:** metodología, supuestos, cómo lo validaste, limitaciones.
- **Para un portafolio:** ambas — muestra el resultado bonito Y un apéndice de "cómo lo hice" que demuestre rigor.

Regla: **lidera con la conclusión, no con el método.** El jefe no quiere "hice un join y agrupé por turno"; quiere "perdemos 1.250 kg al año por hornear tandas pequeñas, y así se arregla".

---

## Checklist rápido para tu próximo proyecto

- [ ] ¿Cuál es la **decisión** que quiero informar? ¿Quién la toma?
- [ ] ¿Cuál es la **pregunta** central, en una frase?
- [ ] ¿Entiendo cada columna y de dónde viene?
- [ ] ¿Limpié tipos, nulos, duplicados, unidades?
- [ ] ¿Exploré con al menos 4 **lentes** distintas (tiempo, segmento, ratio, distribución…)?
- [ ] ¿Formé y **descarté** hipótesis antes de quedarme con una?
- [ ] ¿**Normalicé** antes de comparar?
- [ ] ¿**Validé** el hallazgo con un método independiente?
- [ ] ¿Llegué a una **recomendación cuantificada**?
- [ ] ¿La conté con una **historia** clara para una audiencia concreta?

---

*El oficio no es saber la respuesta rápido. Es saber hacer las preguntas correctas, en orden, y desconfiar de las respuestas fáciles. La velocidad llega sola con los años; la forma de pensar se entrena proyecto a proyecto.*
