# Clase 07 — CART · Guía del profesor

Documento de preparación para la tutorial. **Duración objetivo: 20-22 minutos** de exposición + lectura de outputs. Foco en **modelado y validación (métricas)**. Recorrido celda por celda con:

- **Qué se ve** — el output que aparece en pantalla.
- **Cómo leerlo** — interpretación correcta del output.
- **Para decir en clase** — puntos pedagógicos a remarcar.
- **Trampa pedagógica** (cuando aplica) — error conceptual más probable del alumno.

---

## Marco general — antes de empezar

CART (**C**lassification **A**nd **R**egression **T**rees) aplica la misma lógica de partición recursiva a dos tipos de problema:

- Target categórico → `DecisionTreeClassifier` (Parte A).
- Target continuo → `DecisionTreeRegressor` (Parte B).

En cada nodo, el árbol elige el corte que mejor separa los datos según una métrica de impureza:

- Clasificación: **Gini** (o entropía). Mide qué tan mezcladas están las clases dentro de un nodo.
- Regresión: **MSE**. Mide qué tan dispersos están los valores del target dentro de un nodo.

El árbol baja recursivamente hasta que se cumple un criterio de parada (`max_depth`, `min_samples_leaf`).

**Ventajas frente a algoritmos vistos antes:**

| Vs. | Ventaja de CART |
|---|---|
| Regresión lineal (Clase 04) | Captura no-linealidades sin transformar variables. Robusto a outliers. |
| Regresión logística (Clase 05) | No supone linealidad en el log-odds. Produce reglas explícitas. |
| KNN (Clase 05) | No requiere escalado. Predicción rápida. Salida interpretable. |

**Limitación:** un árbol individual tiende al overfitting cuando se permite que crezca mucho. La solución (Random Forest, Gradient Boosting) se aborda en clases siguientes.

**Justificación de los hiperparámetros elegidos** (validados antes de la clase):

- `max_depth=3` — testeado contra valores 2, 3, 4, 5, 6, 8, sin límite. En clasificación, depth=3 da el mejor **recall en test** (0.80) y train ≈ test. En regresión, depth=3 y 4 rinden parecido (R² 0.687 vs 0.712); preferimos 3 por legibilidad. Profundidades de 5+ empiezan a sobreajustar visiblemente.
- `min_samples_leaf=15` (clasificación) / `30` (regresión) — evita hojas chicas (reglas espurias).
- `class_weight="balanced"` (solo clasificador) — compensa el 12% de churners. Sin esto, recall cae al 5-10%.

---

## Celda 0 — Header del caso

**Qué se ve:** encuadre Netflix LATAM, **las dos preguntas** que la clase va a responder (churn + horas) y la nota de que la clase ocurre en la etapa de Modeling de CRISP-DM.

**Para decir:**

- Subrayar que el dataset **llega limpio** — la limpieza fue parte de las Clases 02 y 04.
- Hoy el foco está en **modelar y evaluar**, no en preparar datos.
- Las dos preguntas planteadas son las que un equipo de Retention real se hace cada semana.

---

## Celda 1 — Imports

**Qué se ve:** carga silenciosa de librerías.

**Para decir:** señalar el bloque de `sklearn.tree` — importamos los dos modelos (`DecisionTreeClassifier`, `DecisionTreeRegressor`) y dos utilidades clave (`plot_tree` para visualización, `export_text` para reglas en texto).

---

## Celdas 2-5 — Carga y vistazo

**Qué se ve:**

- Cel. 3: `shape (1500 × 11)` más primeras filas del dataset.
- Cel. 4: `df.info()` confirma que no hay nulos y los tipos son correctos.
- Cel. 5: tabla de referencia con las variables disponibles.

**Cómo leerlo:** 1500 filas son suficientes para un árbol con `max_depth=3`. 11 columnas, dos targets (`churn_30d` y `horas_proximo_mes`).

**Para decir:**

- No hay nulos → no toca imputar.
- Tener **dos targets en el mismo dataset** (uno binario, uno continuo) es lo que permite resolver clasificación y regresión sobre la misma base.

---

## Celdas 6-15 — EDA

**Qué se ve:**

- Cel. 7: balance del target — `churn_30d` se distribuye 88% / 12%.
- Cel. 8 (markdown): justifica `class_weight="balanced"` como consecuencia directa del desbalance.
- Cel. 9 (markdown): anuncia tres vistas — plan, consumo, recencia.
- Cel. 10: barplot de tasa de churn por plan.
- Cel. 11: boxplot horas vistas según churn.
- Cel. 12: boxplot recencia según churn.
- Cel. 13 (markdown): observaciones del EDA + tratamiento de outliers.
- Cel. 14 (markdown): intro al describe.
- Cel. 15: `df.describe(include="all")` como referencia.

**Cómo leerlo:**

- **88/12 es desbalanceado.** Un modelo trivial que prediga "se queda" para todos obtiene 88% de accuracy pero recall de churn = 0. Es lo opuesto al objetivo de negocio. `class_weight="balanced"` resuelve esto en el criterio de split.
- **Plan:** `estandar_con_anuncios` concentra el churn (más barato, menos comprometido).
- **Horas:** los churners venían viendo menos horas (mediana ~20h vs ~35h).
- **Recencia:** los churners venían con más días sin entrar (predictor más fuerte).

**Para decir en clase:**

- El balance es el único dato del EDA que justifica directamente una decisión de modelado (`class_weight`). Conviene anclar la pregunta del grupo acá: *"si el modelo predijera 'se queda' para todos, ¿le sirve al equipo de Retention?"*. La respuesta evidente fuerza el razonamiento sobre recall.
- Pasar **firme pero no apurado** por las 3 visualizaciones. Cada una refuerza una intuición que después aparece en el árbol.

**Trampa pedagógica importante — outliers en el boxplot de horas:**

> *"Profe, ¿no deberíamos remover esos outliers?"*

Respuesta:

1. **No son ruido.** Netflix efectivamente tiene usuarios que consumen 90-100h/mes (3+ h diarias). Son la cola larga del comportamiento real — son los usuarios de mayor LTV.
2. **CART es robusto a outliers por diseño.** El árbol divide por umbrales — si un usuario vio 95 o 200 horas, cae del mismo lado del corte. No afecta la decisión.
3. **Diferencia con clases anteriores:** en Clase 04 (regresión lineal) un outlier alto distorsionaba la pendiente; por eso aplicábamos `log` o removíamos casos extremos. En Clase 05 (KNN), los outliers afectaban las distancias. En CART nada de esto aplica.

Frase de cierre: *"CART es la primera familia de modelos del curso que no requiere preprocesamiento de outliers ni escalado de variables."*

---

## Celdas 16-18 — Data prep

**Qué se ve:**

- Cel. 17: `pd.get_dummies(..., drop_first=True)` convierte categóricas a binarias. El dataset pasa de 11 a ~20 columnas.
- Cel. 18: train/test split estratificado 70/30. Confirma `Train: 1050 filas | Test: 450 filas`.

**Cómo leerlo:**

- **One-hot encoding** porque sklearn no acepta categóricas directamente.
- **`drop_first=True`** evita la trampa de la dummy variable (multicolinealidad perfecta).
- **Estratificación por `churn_30d`** mantiene el 12% en ambas particiones.
- **`random_state=42`** asegura reproducibilidad.
- **Un único split reutilizado para los dos modelos** → resultados comparables.

**Para decir:**

- Estratificar es **crítico** con desbalance. Sin estratificación, el test set podría tener 5% o 18% de churn por azar.
- Mencionar al pasar que **CART no necesita escalado** (a diferencia de KNN de la Clase 05).

**Trampa:**

> *"¿El árbol no podría manejar categóricas directamente?"*

Otros frameworks (LightGBM, CatBoost) sí lo hacen de manera nativa. sklearn no — exige features numéricas. Mencionarlo porque va a aparecer en la documentación.

---

## Celda 19 — Markdown Parte A (intro)

Anuncia el modelo de clasificación. Anticipa los hiperparámetros principales (`max_depth=3` para legibilidad, `class_weight="balanced"` para el desbalance).

---

## Celda 20 — Entrenamiento del clasificador

**Qué se ve:** ejecución silenciosa de `fit`.

**Cómo leerlo:** se entrena el árbol con tres restricciones explícitas:

| Hiperparámetro | Valor | Justificación |
|---|---|---|
| `max_depth=3` | profundidad máxima 3 niveles | Validado contra otros valores; da el mejor recall en test sin overfittear. Mantiene el árbol **legible**. |
| `min_samples_leaf=15` | mínimo 15 observaciones por hoja | Evita hojas pequeñas (reglas espurias). |
| `class_weight="balanced"` | pondera la clase minoritaria | Sin este parámetro, el recall de churn cae por debajo del 10%. |

**Para decir en clase:**

- Los tres hiperparámetros responden a decisiones concretas: `max_depth` resuelve interpretabilidad + overfitting, `min_samples_leaf` resuelve robustez estadística, `class_weight` resuelve desbalance.
- **`class_weight="balanced"`** fue introducido en la Clase 05 con regresión logística. Misma lógica aquí.

---

## Celda 21 — Métricas de clasificación

**Qué se ve:**

```
Matriz de confusión:
[[277 118]
 [ 11  44]]

Reporte de clasificación:
              precision    recall  f1-score   support
    Se queda       0.96      0.70      0.81       395
       Churn       0.27      0.80      0.41        55
    accuracy                           0.71       450

Accuracy train: 0.702   |   Accuracy test: 0.713
```

**Cómo leerlo — punto central de la clase:**

- **Recall de Churn = 0.80:** de cada 100 churners reales, el modelo detecta 80. **Es la métrica que importa para Retention.**
- **Precision de Churn = 0.27:** de cada 100 usuarios marcados como riesgo, 27 son churners reales; el resto son falsos positivos.
- **F1 = 0.41:** la media armónica entre las dos.
- **Accuracy train ≈ Accuracy test (0.70 ≈ 0.71):** **el modelo NO está overfitteando.** Sanity check obligatorio en cualquier modelo de producción.

**El trade-off central:**

- Precision baja con recall alto significa que el modelo es **inclusivo** — captura casi todos los churners reales pero también marca usuarios que iban a permanecer.
- **¿Es un problema?** Depende del costo. Un cupón a un falso positivo cuesta poco. NO detectar a un churner real implica perder el LTV completo. En Retention **el recall pesa más que la precision**.

**Para decir en clase:**

- Este es el contenido de la Clase 06 (Métricas) aplicado en un caso real. Si los alumnos no internalizan esta sección, no comprenden CART aplicado.
- Pregunta para el grupo: *"si Retention tuviera presupuesto para contactar solo 50 usuarios por semana, ¿priorizarían precision o recall alto?"*. La respuesta cambia con la restricción.
- **No saltearse el sanity check de overfitting.** Que train ≈ test es lo que separa un modelo de producción de un modelo memorizador.

---

## Celdas 22-23 — Árbol de clasificación y su lectura

**Qué se ve:**

- Cel. 22: `plot_tree` del clasificador en figura 14×7 con `max_depth=3` → ~8 hojas como máximo. Cada caja muestra:
  - La regla del corte (ej: `dias_desde_ultima_sesion <= 12.5`).
  - El `gini` del nodo (impureza, 0 = puro).
  - `samples` (observaciones en ese nodo).
  - `value = [X, Y]` (distribución entre clases, **ponderada por `class_weight`**).
  - `class` (clase mayoritaria).
  - **Colores:** azul = "Se queda", rojo = "Churn". Intensidad = pureza.
- Cel. 23 (markdown): observación breve sobre la lectura.

**Cómo leerlo paso a paso:**

1. **Nodo raíz:** primer corte. Casi con certeza `dias_desde_ultima_sesion` — la recencia es el predictor más fuerte.
2. **Recorrer una rama:** cada nodo es una pregunta sí/no. La hoja final indica la predicción.
3. **Hojas oscuras de rojo:** segmentos de mayor riesgo — los que Retention contacta prioritariamente.
4. **Hojas azules:** clientes con riesgo bajo, no requieren intervención.

**Para decir en clase — sección de mayor impacto pedagógico:**

- *"Lo que se ve en pantalla resume la diferencia entre CART y otros modelos: la salida no es una probabilidad opaca, es un conjunto de reglas explícitas. El equipo de Retention puede leer el árbol y construir su workflow de contacto sin necesidad de comprender machine learning."*
- Dedicar 2-3 minutos a recorrer una hoja en voz alta:
  - *"Si los días sin entrar son mayores a X y las horas vistas son menores a Y, hay Z% de probabilidad de churn → llamar mañana."*

**Trampa pedagógica:**

Los valores `value=[X, Y]` están ponderados por `class_weight`. Al sumarlos no coinciden con `samples`. Aclarar: "los `samples` son las observaciones reales, los `value` son la representación ponderada que el árbol usa internamente para decidir los cortes".

---

## Celdas 24-25 — Importancia de variables

**Qué se ve:**

- Cel. 24 (markdown): intro.
- Cel. 25: barplot horizontal de `feature_importances_` filtrando las que tienen importancia > 0.

**Cómo leerlo:** la importancia mide cuánto pesa cada feature al armar los cortes del árbol. Es la versión cuantitativa de lo que se ve visualmente en el árbol.

**Para decir:**

- Confirma cuantitativamente lo que el árbol mostró visualmente.
- **Util para ejecutivos:** "estas son las 3 variables que explican el 90% del churn" — vista comprimida del árbol.
- Si una feature de la tabla de variables (celda 5) NO aparece acá, el árbol no la usó. Es señal de que esa columna **no agrega valor predictivo** en este modelo.

---

## Celdas 26-27 — Reglas del árbol en texto (`export_text`)

**Qué se ve:**

- Cel. 26 (markdown): intro.
- Cel. 27: representación textual del árbol completo, indentada por niveles. Cada línea es una regla `feature <= valor`.

**Cómo leerlo:** la misma información del árbol visual, pero en formato lineal. Útil para incluir en un documento operativo.

**Para decir:**

- *"Si el equipo de Retention te pide 'pasame las reglas para copiar al documento', esta es la herramienta."*
- Mostrar brevemente y derivar a la lectura del árbol visual (celda 22) como el formato principal.

---

## Celda 28 — Markdown Parte B (intro)

Anuncia el cambio a regresión. Aclarar:

- **Misma estructura**, mismo `max_depth=3`, mismo `random_state`.
- Solo cambian la clase del estimador (`DecisionTreeRegressor`) y el target.
- Métrica interna ahora es **MSE** en lugar de Gini.

Es el corazón conceptual de la clase: dos problemas distintos resueltos con el mismo algoritmo.

---

## Celdas 29-30 — Entrenamiento y métricas del regresor

**Qué se ve:**

- Cel. 29: `fit` silencioso. `min_samples_leaf=30` un poco más alto que en clasificación para promedios estables.
- Cel. 30:
  ```
  MSE:  125.77
  RMSE: 11.21 horas
  R2:   0.687

  R² train: 0.689   |   R² test: 0.687
  ```

**Cómo leerlo:**

- **RMSE ≈ 11 horas:** error típico de la predicción. Si el modelo predice 30h y el usuario consume 47h, el error es 17h (cerca del RMSE).
- **R² ≈ 0.69:** el modelo explica el 69% de la variabilidad de las horas. **Es un buen número** para predicción de comportamiento humano.
- **R² train ≈ R² test (0.689 ≈ 0.687):** **no overfittea.** El sanity check confirma la elección de `max_depth=3`.

**Para decir:**

- **R² no debe leerse como una calificación absoluta.** Lo razonable depende del dominio. En este caso 0.69 es excelente — vamos a ver en Random Forest si se puede subir más.
- **RMSE expresado en horas** es la métrica que el área de negocio comprende — más útil que un R² aislado.
- **Train ≈ test** confirma que el modelo generaliza. Vale la pena verbalizarlo: el modelo no memoriza el training set.

**Pregunta probable:**

> *"¿Qué pasaría si subimos `max_depth` a 10?"*

R² train sube; R² test probablemente cae o se mantiene. Hicimos esa búsqueda antes de la clase: a partir de `max_depth=5` el gap empieza a abrirse (~+0.02 a +0.03). Con `depth=3` el gap es prácticamente nulo.

---

## Celdas 31-33 — Árbol de regresión

**Qué se ve:**

- Cel. 31 (markdown): intro corta.
- Cel. 32: `plot_tree` del regresor en figura 14×7. Cada caja muestra:
  - Regla del corte.
  - `squared_error` del nodo (la versión continua de Gini).
  - `samples`.
  - `value` (el promedio del target en ese nodo — el valor que el modelo predice).
- Cel. 33 (markdown): cierre operativo (insumo para LTV / Contenido).

**Cómo leerlo:**

- Cada hoja contiene un **valor numérico** — horas esperadas para los suscriptores que caen ahí.
- El primer corte va a ser nuevamente `dias_desde_ultima_sesion` o `horas_vistas_mes_pasado` (las dos variables más correlacionadas con el target).
- Las hojas con valores altos son segmentos de alto consumo; las hojas con valores bajos son segmentos de bajo consumo.

**Para decir en clase:**

- *"Las hojas de este árbol son segmentos de consumo. Cada una es un perfil con un valor esperado de horas. Insumo directo para calcular **LTV por segmento** y para que Contenido sepa cuántas horas-vista empujar en cada cohorte."*
- Mostrar **la conexión con el árbol de clasificación**: las variables que cortan son básicamente las mismas. Recencia y consumo previo predicen tanto la probabilidad de churn como las horas futuras. Coherencia conceptual fuerte.

---

## Celda 34 — Cierre

**Qué se ve:** las dos preguntas del header respondidas explícitamente, acción operativa por área, justificación del modelo y gancho a la próxima clase.

**Para decir al cerrar:**

1. **Volver a las dos preguntas del principio.** Mostrar que respondimos ambas con métricas concretas.
2. **Acción operativa por área.** Retention contacta el 80% identificado aceptando 27% de precision; Pricing / Content / Finance usan las cohortes del árbol de regresión para sus propios cálculos.
3. **Interpretabilidad como ventaja competitiva.** El ejemplo del CFO ("¿por qué llamamos a Juan?") sirve para aterrizar el valor distintivo de CART.
4. **Enlace con la próxima clase.** Random Forest y Gradient Boosting suben performance combinando muchos árboles. Es lo que la industria usa.

---

## Preguntas frecuentes (anticipar)

### "¿Por qué Gini y no entropía?"

Ambos criterios producen árboles muy similares. Gini es el default de sklearn y se calcula más rápido.

### "¿El árbol está overfiteado?"

No, y queda demostrado en pantalla. Las celdas 21 y 30 imprimen explícitamente `train ≈ test` para ambos modelos. Si querés profundizar, mencioná que la validación previa probó `max_depth` de 2 a 8 — a partir de 5 empieza a abrirse el gap entre train y test.

### "¿Por qué no usar KNN aquí?"

KNN podría aplicarse, pero requiere escalado, predice lentamente en producción y **no produce reglas legibles**. Para un caso donde la interpretabilidad es prioritaria, CART es la elección correcta.

### "¿Cómo elegir `max_depth`?"

Búsqueda en grilla con `GridSearchCV` — herramienta de clases posteriores. Heurística práctica: 3-5 niveles para problemas con 10-20 features y miles de observaciones.

### "¿Qué pasa si el dataset cambia mes a mes?"

CART aprende del dataset que se le entrega. Cada nuevo mes requiere un reentrenamiento.

---

## Timing sugerido (clase de 20-22 minutos)

| Bloque | Celdas | Tiempo |
|---|---|---|
| Header + imports + carga + tabla variables | 0-5 | 2 min |
| EDA (balance + 3 viz + observaciones + describe) | 6-15 | 4 min |
| Data prep: one-hot + split estratificado | 16-18 | 2 min |
| **Parte A: clasificación** — fit + métricas + árbol + importancia + reglas en texto | 19-27 | **7 min** |
| **Parte B: regresión** — fit + métricas + árbol | 28-33 | **5 min** |
| Cierre — responder las dos preguntas + acción de negocio + gancho | 34 | 2 min |
| **Total** | | **22 min** |

Si la clase corre corta, `export_text` (celda 27) se puede saltar — el árbol visual ya cubre la información. Si corre larga, las 3 viz del EDA (celdas 10-12) se pueden mostrar más rápido sin perder pedagogía.
