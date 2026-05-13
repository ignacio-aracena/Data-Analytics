# Clase 07 — CART · Guía del profesor

Documento de preparación para la tutorial. Recorrido celda por celda con:

- **Qué se ve** — el output que aparece en pantalla.
- **Cómo leerlo** — interpretación correcta del output.
- **Para decir en clase** — puntos pedagógicos a remarcar.
- **Trampa pedagógica** (cuando aplica) — error conceptual más probable del alumno.

---

## Marco general — antes de empezar

CART (**C**lassification **A**nd **R**egression **T**rees) aplica la misma lógica de partición recursiva a dos tipos de problema:

- Target categórico → `DecisionTreeClassifier` (Parte A).
- Target continuo → `DecisionTreeRegressor` (Parte B).

En cada nodo, el árbol elige el corte que **mejor separa los datos** según una métrica de impureza:

- Clasificación: **Gini** (o entropía). Mide qué tan mezcladas están las clases dentro de un nodo.
- Regresión: **MSE**. Mide qué tan dispersos están los valores del target dentro de un nodo.

El árbol baja recursivamente eligiendo cortes hasta que se cumple un criterio de parada (`max_depth`, `min_samples_leaf`, etc.).

**Ventajas frente a algoritmos vistos en clases anteriores:**

| Vs. | Ventaja de CART |
|---|---|
| Regresión lineal (Clase 04) | Captura relaciones no lineales sin necesidad de transformar variables. Robusto a outliers. |
| Regresión logística (Clase 05) | No supone linealidad en el log-odds. Produce reglas explícitas, fáciles de comunicar al área de negocio. |
| KNN (Clase 05) | No requiere escalado. Predicción mucho más rápida en producción. Salida interpretable. |

**Limitación:** un árbol individual tiende al overfitting. La solución (Random Forest, Gradient Boosting) se trabaja en las clases siguientes.

---

## Celda 0 — Header del caso

**Qué se ve:** el encuadre Netflix LATAM, las dos preguntas (churn + horas) y la nota de que la clase ocurre en la etapa de Modeling de CRISP-DM.

**Para decir en clase:**

- Subrayar que el dataset llega **limpio** — la limpieza fue parte de las Clases 02 y 04. Hoy el foco está en **modelar y evaluar**, no en preparar datos.
- Las dos preguntas planteadas son las que un equipo de Retention real se hace cada semana.

---

## Celda 1 — Imports

**Qué se ve:** carga silenciosa de librerías.

**Para decir:** señalar el bloque de `sklearn.tree` — importamos los dos modelos (`DecisionTreeClassifier`, `DecisionTreeRegressor`) y dos utilidades clave (`plot_tree` para visualización, `export_text` para reglas en formato plano).

---

## Celdas 3-5 — Carga y vistazo

**Qué se ve:**

- Cel. 3: shape del dataset (1500 × 11) más primeras filas.
- Cel. 4: `df.info()` confirma que no hay nulos y los tipos son correctos.
- Cel. 5: tabla de referencia con las variables disponibles.

**Cómo leerlo:** 1500 filas son suficientes para entrenar un árbol con `max_depth` acotado. Hay 11 columnas, incluyendo dos targets (`churn_30d` y `horas_proximo_mes`).

**Para decir en clase:**

- Al no haber nulos, no hace falta imputar.
- Tener **dos targets en el mismo dataset** (uno binario, uno continuo) es lo que permite resolver clasificación y regresión usando la misma base de datos.

---

## Celda 7 — Balance del target de clasificación

**Qué se ve:**

```
0    ~1320  (88%)
1    ~180   (12%)
```

**Cómo leerlo:** 12% es churn — **dataset desbalanceado**. Si el modelo predijera "todos se quedan", obtendría 88% de accuracy pero un recall de churn igual a cero, que es justamente lo opuesto al objetivo de negocio.

**Para decir en clase:**

- Esta es la justificación para usar `class_weight="balanced"` en la celda 15. Conviene anticiparlo acá, no más adelante.
- Pregunta para el grupo: *"si un modelo acierta 88% pero no detecta a ningún churner, ¿le sirve al equipo de Retention?"*. La respuesta es evidente, pero es útil que la formulen ellos.

**Conexión con la Clase 06 (Métricas):** accuracy es engañosa cuando hay desbalance. La métrica que importa en este caso es el **recall de la clase minoritaria** (Churn).

---

## Celda 8 — Tasa de churn por plan

**Qué se ve:** barplot ordenado de mayor a menor tasa de churn. `estandar_con_anuncios` lidera con tasa cercana al 25%; `premium` cierra abajo con tasa cercana al 5%.

**Cómo leerlo:** los planes más económicos concentran el churn — son los usuarios menos comprometidos con la plataforma.

**Para decir en clase:**

- Aclarar que esto no implica causalidad — los usuarios menos comprometidos eligen el plan barato, no es que el plan los expulse. Pero es una **señal predictiva fuerte** y el árbol va a aprovecharla.
- Es el primer indicio de que `plan` aparecerá como variable de corte en el árbol.

---

## Celda 9 — Boxplot: horas vistas el mes pasado, separado por churn

**Qué se ve:** dos cajas. La de "Se quedó" tiene mediana mayor (~35h), la de "Churn" más baja (~20h). Dentro de la caja "Se quedó" aparecen **varios puntos por encima del bigote superior** — outliers visibles.

**Cómo leerlo:**

- Los usuarios que permanecen consumen más horas, lo que es consistente con la hipótesis.
- Los puntos por encima del bigote corresponden a usuarios con 90+ horas mensuales — equivalentes a 3+ horas diarias. **Son observaciones legítimas, no errores de medición.**

**Trampa pedagógica importante (probable pregunta de los alumnos):**

> *"¿No deberíamos remover esos outliers?"*

**Respuesta a desarrollar en clase:**

1. **No son ruido.** Netflix efectivamente tiene usuarios que consumen 90-100 horas mensuales. Son la cola larga del comportamiento de consumo. Removerlos equivaldría a descartar a los usuarios de mayor LTV.
2. **CART es robusto a outliers por diseño.** El árbol divide por umbrales, por ejemplo `horas > 40`. Que un usuario haya visto 95 o 200 horas no afecta la decisión — cae del mismo lado del corte. La diferencia con algoritmos vistos antes:
   - **Regresión lineal (Clase 04):** un outlier alto distorsiona la pendiente. Por eso allí aplicábamos `log` o removíamos casos extremos.
   - **KNN (Clase 05):** un punto extremo queda lejísimos en distancias euclidianas, afectando las predicciones de los vecinos.
3. **Esta propiedad se generaliza a la familia de árboles** (Random Forest y Gradient Boosting la heredan).

**Frase de cierre del punto:** *"El árbol no necesita conocer la magnitud exacta del outlier — solo si está por encima o por debajo del umbral. Por esa razón, CART es la primera familia de modelos del curso que no requiere preprocesamiento de outliers ni escalado de variables."*

---

## Celda 10 — Observaciones del EDA

**Qué se ve:** markdown breve con tres puntos clave.

**Para decir:** dejar que los alumnos cierren el EDA con la conclusión: "ya tenemos las hipótesis, ahora vamos a verificar si el árbol las confirma".

---

## Celda 12 — One-hot encoding

**Qué se ve:** el dataset transformado pasa de 11 a aproximadamente 20 columnas. Las nuevas son indicadores binarios por categoría: `plan_estandar`, `plan_estandar_con_anuncios`, `plan_premium`, etc.

**Cómo leerlo:** `pd.get_dummies(..., drop_first=True)` crea una columna binaria por cada categoría, descartando una (la primera alfabéticamente) para evitar multicolinealidad perfecta.

**Para decir en clase:**

- sklearn requiere features numéricas. `get_dummies` es la herramienta estándar para convertir variables categóricas.
- `drop_first=True` evita la trampa de la dummy variable: con 4 planes y 4 columnas binarias, una es combinación lineal de las otras tres (suman siempre 1).

**Trampa pedagógica:**

> *"¿El árbol no podría manejar categóricas directamente?"*

Otros frameworks como LightGBM o CatBoost sí lo hacen de manera nativa. sklearn no — exige features numéricas. Mencionarlo porque va a aparecer en la documentación que consulten.

---

## Celda 13 — Train/test split

**Qué se ve:** `Train: 1050 filas | Test: 450 filas`. Particionado 70/30 con estratificación.

**Cómo leerlo:**

- 70% para entrenar, 30% para evaluar. Estratificado por `churn_30d` para mantener la proporción del 12% de churn en ambas particiones.
- `random_state=42` garantiza reproducibilidad.
- **Decisión metodológica importante:** un único split, reutilizado para los dos modelos. Esto hace que los resultados sean comparables.

**Para decir en clase:**

- Estratificar es **crítico** cuando hay desbalance — sin estratificación, podríamos terminar con un test set con 5% de churn por azar.
- Reutilizar el mismo split en clasificación y regresión es la práctica correcta y no opcional.

---

## Celda 15 — Entrenamiento del clasificador

**Qué se ve:** ejecución silenciosa de `fit`.

**Cómo leerlo:** se entrena el árbol con tres restricciones explícitas:

| Hiperparámetro | Valor | Justificación |
|---|---|---|
| `max_depth=4` | profundidad máxima 4 niveles | Mantiene el árbol **legible**. Mayor profundidad significa más nodos y árboles imposibles de explicar al área de negocio. |
| `min_samples_leaf=15` | mínimo 15 observaciones por hoja | Evita hojas pequeñas (reglas espurias que no generalizan). |
| `class_weight="balanced"` | pondera la clase minoritaria | Sin este parámetro, el árbol prioriza la clase mayoritaria y el recall de churn cae por debajo del 5%. |

**Para decir en clase:**

- **`max_depth` es el control principal contra el overfitting.** Profundidad chica subajusta (poca capacidad), profundidad grande sobreajusta (memoriza el training set). 4 es un valor razonable para este problema.
- **`class_weight="balanced"`** fue introducido en la Clase 05 con regresión logística. Misma lógica aquí.
- Los tres hiperparámetros responden a decisiones concretas: `max_depth` resuelve interpretabilidad, `min_samples_leaf` resuelve robustez estadística, `class_weight` resuelve desbalance.

**Pregunta probable:**

> *"¿Por qué `max_depth=4` y no `max_depth=10`?"*

No existe un valor universalmente correcto. Es un trade-off: mayor profundidad implica mejor ajuste en training, peor generalización en test, y un árbol ilegible. En esta clase se prioriza interpretabilidad porque el caso lo requiere — el equipo de Retention necesita reglas explicables. En contextos donde la explicabilidad no es prioritaria (por ejemplo, predicción interna sin reporte), se podría aumentar la profundidad y compensar el overfitting con un ensemble.

---

## Celda 16 — Métricas de clasificación

**Qué se ve:**

```
Matriz de confusión:
[[~340  ~55]    ← de los que se quedaron, ~55 falsos positivos
 [ ~12  ~43]]   ← de los churners reales, ~12 no detectados, ~43 detectados

Reporte de clasificación:
                precision  recall  f1-score
Se queda        0.97       0.86    0.91
Churn           0.44       0.78    0.56
```

(Los valores exactos varían levemente según `random_state`.)

**Cómo leerlo — punto central de la clase:**

- **Precision de Churn ≈ 0.44:** de cada 100 usuarios marcados como churners, 44 lo serán realmente. El resto son falsos positivos.
- **Recall de Churn ≈ 0.78:** de cada 100 churners reales, el modelo detecta 78. Pierde 22.
- **F1 ≈ 0.56:** la media armónica entre precision y recall.

**El trade-off a explicar:**

- Precision baja con recall alto indica que el modelo es **más inclusivo que selectivo**: marca muchos usuarios como riesgo, captura la mayoría de los churners reales, pero incluye también usuarios que iban a permanecer.
- **¿Es un problema?** Depende del costo de cada error. Enviar un cupón a un falso positivo tiene un costo bajo. NO detectar a un churner real implica perder el LTV completo del cliente. Por esta razón, en Retention **el recall pesa más que la precision**.

**Para decir en clase:**

- Este es el contenido de la Clase 06 (Métricas) aplicado en un caso real. Si los alumnos no internalizan esta sección, no comprenden CART aplicado.
- Pregunta para el grupo: *"si Retention solo tuviera presupuesto para contactar 50 usuarios por semana, ¿priorizarían precision alta o recall alto?"*. La respuesta cambia con la restricción de capacidad y obliga a los alumnos a razonar.

---

## Celda 17 — Matriz de confusión visual

**Qué se ve:** la misma matriz presentada como heatmap en escala de rojos.

**Cómo leerlo:** misma información que la celda anterior, en formato visual. Útil para presentaciones al área de negocio.

**Para decir:** mantener el comentario breve — la celda relevante en términos pedagógicos es la siguiente.

---

## Celda 18 — Visualización del árbol (`plot_tree`)

**Qué se ve:** **el árbol completo** con cajas de colores. Cada caja muestra:

- La regla del corte (por ejemplo, `dias_desde_ultima_sesion <= 12.5`).
- El `gini` del nodo (impureza, 0 significa nodo puro).
- `samples` (número de observaciones que caen en ese nodo).
- `value` (distribución de clases — al usar `class_weight="balanced"`, estos valores están **ponderados**, no son crudos).
- `class` (la clase mayoritaria en ese nodo).

Código de colores: azul corresponde a "Se queda", rojo/naranja a "Churn". La intensidad refleja la pureza del nodo.

**Cómo leerlo paso a paso:**

1. **Nodo raíz:** muestra la primera variable que el árbol elige como corte. En este caso, casi con certeza será `dias_desde_ultima_sesion` — la recencia es el predictor más fuerte de churn.
2. **Recorrer una rama:** cada nodo es una pregunta sí/no. La hoja final indica que esa combinación de reglas predice una clase específica.
3. **Hojas oscuras de rojo:** segmentos de mayor riesgo. Son los usuarios que Retention debe contactar prioritariamente.
4. **Hojas azules:** clientes con riesgo bajo. No requieren intervención.

**Para decir en clase — esta es la sección más importante:**

- *"Lo que se ve en pantalla resume la diferencia entre CART y regresión logística: la salida no es una probabilidad opaca, es un conjunto de reglas explícitas. El equipo de Retention puede leer el árbol y construir su workflow de contacto sin necesidad de comprender machine learning."*
- Dedicar 2-3 minutos a recorrer una hoja en voz alta:
  - *"Si los días sin entrar son mayores a 14 y las horas vistas son menores a 5, hay 80% de probabilidad de churn → llamar mañana."*
- Este ejercicio aterriza toda la teoría del nodo y la regla de decisión.

**Trampa pedagógica:**

Los valores `value=[X, Y]` están ponderados por `class_weight`. Al sumarlos no coinciden con `samples`. Aclarar: "los `samples` son las observaciones reales, los `value` son la representación ponderada que utiliza el árbol internamente para decidir los cortes".

---

## Celda 19 — Lectura del árbol (markdown)

**Qué se ve:** observación breve sobre la lectura del árbol.

**Para decir:** permitir que el grupo extraiga la conclusión central — la recencia es el predictor #1, el plan queda en segundo plano. Este resultado **invierte la intuición inicial**: uno esperaría que el plan tuviera más peso predictivo.

---

## Celda 21 — Entrenamiento del regresor

**Qué se ve:** ejecución silenciosa de `fit`.

**Cómo leerlo:** misma estructura de árbol pero con `DecisionTreeRegressor`. Cambios respecto al clasificador:

- Se elimina `class_weight` (el target es continuo, no hay clases).
- `min_samples_leaf=30`, ligeramente más alto, para que el promedio de cada hoja sea estable.
- La métrica interna que minimiza es MSE en lugar de Gini.

**Para decir en clase:**

- Enfatizar: **misma estructura, mismo `max_depth`, mismo `random_state`**. Solo cambian la clase del estimador y el target.
- Es el corazón conceptual de la clase: dos problemas distintos resueltos con el mismo algoritmo.

---

## Celda 22 — Métricas de regresión

**Qué se ve:**

```
MSE:  ~280
RMSE: ~17 horas
R2:   ~0.27
```

**Cómo leerlo:**

- **RMSE ≈ 17 horas:** error típico de la predicción. Si el modelo predice 30h y el usuario consume 47h, el error es de 17h.
- **R² ≈ 0.27:** el modelo explica el 27% de la variabilidad de las horas consumidas. **Es un valor moderado.** No es malo en términos prácticos — el consumo de horas es volátil — pero conviene ser transparente: un árbol único no produce predicciones muy precisas en esta tarea.

**Para decir en clase:**

- **R² no debe leerse como una calificación absoluta.** Un R² de 0.27 puede ser excelente en un dominio (comportamiento humano) y deficiente en otro (sistemas físicos deterministas). Lo razonable en este caso es lo que los datos permiten.
- **RMSE expresado en unidades del target** es la métrica que el área de negocio comprende. "Error promedio de 17 horas" es más útil que "R² 0.27" para Contenido o Pricing.

**Pregunta probable:**

> *"¿Qué pasaría si subimos `max_depth` a 10?"*

R² en training subiría considerablemente; R² en test probablemente se mantendría o caería. Es el patrón clásico de overfitting. Si hay tiempo, conviene demostrarlo en vivo. Si no, queda como ejercicio del TP.

**Conexión:** las métricas presentadas corresponden a la Clase 06.

---

## Celda 24 — Tabla de 5 nuevos suscriptores

**Qué se ve:** una tabla con cinco filas hipotéticas, cada una representando un perfil distinto:

1. **Nuevo + plan barato + recencia alta** → candidato fuerte a churn.
2. **Veterano + premium + alto consumo + sesión reciente** → cliente saludable.
3. **Medio + estándar + consumo medio** → cliente promedio.
4. **Nuevo + básico + recencia alta + dos cambios de plan** → riesgo.
5. **Veterano + premium + consumo muy alto + sesión actual** → cliente top.

**Para decir:** estos no son datos reales, son perfiles representativos. La intención es mostrar cómo el modelo produce una respuesta operativa para cada uno.

---

## Celda 25 — Predicción y asignación de acción

**Qué se ve:** la misma tabla con tres columnas adicionales: `prob_churn`, `horas_proximo_mes`, `accion_retention`. La acción se determina con reglas simples:

- Probabilidad ≥ 0.50 → "Contactar urgente"
- 0.25 ≤ probabilidad < 0.50 → "Mandar promo"
- Probabilidad < 0.25 → "No tocar"

**Cómo leerlo:** este es el output que se entrega al área de negocio. Convierte probabilidades en **acciones operativas concretas**.

**Para decir en clase:**

- *"Los modelos no le aportan valor al negocio hasta que se traducen en acción. Una probabilidad por sí sola no es accionable."*
- Los thresholds (0.50, 0.25) son decisiones de negocio, no decisiones del modelo. Modificarlos cambia el volumen de usuarios contactados — es una palanca operativa.
- En producción esto se implementa como un proceso diario que corre sobre toda la base de usuarios y entrega un archivo al equipo de Retention. **Esta es la forma habitual de operar ML en negocios.**

---

## Celdas 26-39 — "Para casa"

**Qué se ve:** sección con seis ejercicios complementarios:

1. `describe(include="all")` completo.
2. Boxplot de recencia (segunda señal de churn).
3. `export_text` — reglas en texto plano.
4. Importancia de variables (`feature_importances_`).
5. Visualización del árbol de regresión.
6. Predicho vs real (scatter del regresor).

**Para decir en clase:**

- Mostrar los ejercicios por arriba, **sin profundizar**. *"Esto lo cubrimos por arriba, lo trabajan en casa."*
- Aclarar que **el material puede aparecer en el parcial**. No es opcional, es complementario.

**Puntos breves a mencionar en cada uno:**

- **`export_text`:** cuando el negocio solicita las reglas "para copiar en un documento", esta es la herramienta. Es el mismo árbol que el visual, en formato texto.
- **Importancia de variables:** confirma cuantitativamente lo que el árbol mostró visualmente (recencia y horas como top features). Más concisa que el árbol completo para presentaciones ejecutivas.
- **Predicho vs real:** el gráfico estándar para diagnóstico de un regresor. Puntos cerca de la diagonal indican buena predicción; la desviación corresponde al error.

---

## Celda 40 — Cierre

**Qué se ve:** tabla resumen y tres ideas finales.

**Para decir al cerrar:**

1. **Recapitular la tabla.** Misma técnica aplicada a dos problemas distintos. Es la idea central de la clase.
2. **Interpretabilidad como ventaja competitiva.** Cada predicción de un árbol viene acompañada por la secuencia de reglas que la generó. Esta propiedad es lo que el área de negocio valora especialmente.
3. **Enlace con la próxima clase.** Un árbol individual tiene tendencia al overfitting. La solución industrial es combinar muchos árboles: Random Forest y Gradient Boosting. La próxima clase aborda estos ensembles.

---

## Preguntas frecuentes (anticipar en clase si surgen)

### "¿Por qué Gini y no entropía?"

Ambos criterios suelen producir árboles muy similares. Gini es el default de sklearn y se calcula un poco más rápido. Si se quiere comparar, basta con cambiar `criterion="entropy"` y reentrenar — la diferencia será mínima.

### "¿El árbol está overfiteado?"

Con `max_depth=4` y `min_samples_leaf=15` es poco probable. Para verificarlo, comparar accuracy en training contra accuracy en test:

```python
print(f"Accuracy train: {arbol_clf.score(X_train, yclf_train):.3f}")
print(f"Accuracy test:  {arbol_clf.score(X_test, yclf_test):.3f}")
```

Una diferencia menor a 0.05 indica que el modelo no está overfitteando significativamente.

### "¿Por qué no usar KNN aquí?"

KNN podría aplicarse, pero requiere escalado, predice lentamente en producción y **no produce reglas legibles**. Para un caso donde la interpretabilidad es prioritaria, CART es la elección correcta.

### "¿Cómo elegir `max_depth`?"

Búsqueda en grilla con `GridSearchCV` — herramienta que se introduce en clases posteriores. Como heurística: 3-5 niveles para problemas con 10-20 features y miles de observaciones.

### "¿Qué pasa si el dataset cambia mes a mes?"

CART aprende del dataset que se le entrega — no se actualiza automáticamente. Cada nuevo mes de datos requiere un reentrenamiento que reemplaza el árbol en producción.

---

## Timing sugerido (clase de 60 minutos)

| Bloque | Tiempo |
|---|---|
| Header + carga + tabla de variables (0-5) | 5 min |
| EDA + balance + tratamiento de outliers (6-10) | 10 min |
| One-hot + split (11-13) | 5 min |
| **Parte A: clasificación (14-19)** — bloque central | 18 min |
| Parte B: regresión (20-22) | 8 min |
| Predicción operativa (23-25) | 8 min |
| Cierre + repaso de "Para casa" (26-40) | 6 min |
| **Total** | **60 min** |

Si la clase corre corta, "Para casa" se muestra en 2 minutos. Si corre larga, el gráfico predicho-vs-real puede quedar como ejercicio domiciliario sin perder continuidad.
