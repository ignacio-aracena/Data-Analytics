# Clase 07 — CART · Guía del profesor

Guía de preparación para la tutorial. Material **no se distribuye a los alumnos**.

**Duración objetivo:** 20-22 minutos. Foco: **modelado + validación con métricas**.

Recorrido por sección con: qué se ve, cómo leerlo, qué decir, trampas pedagógicas.

---

## Marco general

CART aplica la misma lógica de partición recursiva a dos problemas:

- Target categórico → `DecisionTreeClassifier` (Parte A).
- Target continuo → `DecisionTreeRegressor` (Parte B).

En cada nodo el árbol elige el corte que más reduce la impureza:

- Clasificación: **Gini** (o entropía).
- Regresión: **MSE**.

**Por qué CART importa pedagógicamente:**

| Vs. | Ventaja |
|---|---|
| Regresión lineal (Clase 04) | Captura no-linealidades. Robusto a outliers. |
| Logística (Clase 05) | No supone linealidad. Reglas explícitas. |
| KNN (Clase 05) | No requiere escalado. Predicción rápida. |

**Limitación:** un árbol único tiende al overfitting cuando crece. La solución (Random Forest, Gradient Boosting) viene en clases siguientes.

**Hiperparámetros — justificación validada:**

- `max_depth=3` — probé valores 2-8 y sin tope. En clasificación da el mejor recall en test (0.80) sin overfit; en regresión rinde casi igual que `depth=4` con árbol más legible. A partir de `depth=5` el gap train-test se abre.
- `min_samples_leaf=15` (clasif) / `30` (reg) — evita hojas con pocas observaciones (reglas espurias).
- `class_weight="balanced"` (solo clasif) — compensa el 12% de churners. Sin esto recall cae al 5-10%.

---

## Celda 0 — Header

Encuadre Netflix LATAM, las **dos preguntas** de la clase, mención a CRISP-DM Modeling.

**Para decir:**
- El dataset llega limpio (la limpieza fue de Clases 02 y 04).
- Hoy el foco es modelar y evaluar.
- Las dos preguntas son las que un equipo de Retention real se hace cada semana.

## Celda 1 — Imports

Señalar el bloque de `sklearn.tree` — los dos modelos (`DecisionTreeClassifier`, `DecisionTreeRegressor`) + `plot_tree` (visualización) + `export_text` (reglas en texto).

## Celdas 2-5 — Carga y vistazo

- Cel. 3: shape `(1500, 11)` + head.
- Cel. 4: `df.info()` confirma 0 nulos.
- Cel. 5: tabla de variables (referencia).

**Para decir:** sin nulos, no toca imputar. Dos targets en el mismo dataset (binario + continuo) → modelamos los dos con la misma base.

---

## Celdas 6-15 — EDA

- Cel. 7: balance del target → **88% / 12%** desbalanceado.
- Cel. 8 (md): justifica `class_weight="balanced"` como consecuencia del desbalance.
- Cel. 9 (md): intro a tres vistas.
- Cel. 10: barplot tasa de churn por plan.
- Cel. 11: boxplot horas vistas según churn.
- Cel. 12: boxplot recencia según churn.
- Cel. 13 (md): observaciones + **outliers**.
- Cel. 14-15: `describe(include="all")` como referencia.

**Cómo leerlo:**
- 12% es churn → un modelo que prediga "todos se quedan" obtiene 88% accuracy pero recall = 0. Por eso usamos `class_weight="balanced"`.
- `estandar_con_anuncios` concentra el churn (plan barato, menos compromiso).
- Churners venían con menos horas vistas y mayor recencia.

**Para decir:**
- Anclar la pregunta del grupo en el balance: *"si predijéramos 'se queda' para todos, ¿le sirve a Retention?"*. La respuesta evidente fuerza el razonamiento sobre recall.
- Pasar firme pero no apurado por las 3 visualizaciones — cada una refuerza una intuición que va a aparecer en el árbol.

**Trampa pedagógica — outliers en el boxplot de horas:**

> *"Profe, ¿no deberíamos remover esos outliers?"*

Respuesta corta para clase:

1. **No son ruido.** Netflix tiene usuarios reales que ven 90-100 h/mes (3+ h por día). Son la cola larga del comportamiento — los usuarios de mayor LTV.
2. **CART es robusto a outliers por diseño.** Corta por umbrales — si un usuario vio 95 o 200 horas, cae del mismo lado del corte.
3. **Diferencia con clases anteriores:** Clase 04 (regresión lineal) sí los sacaba. Clase 05 (KNN) también era sensible. CART no.

Frase de cierre: *"CART es la primera familia del curso que no requiere preprocesamiento de outliers ni escalado."*

---

## Celdas 16-18 — Data prep

- Cel. 17: `pd.get_dummies(..., drop_first=True)` → de 11 a ~20 columnas.
- Cel. 18: split estratificado 70/30 → `Train: 1050 | Test: 450`.

**Para decir:**
- One-hot porque sklearn no acepta categóricas directamente.
- `drop_first=True` evita multicolinealidad perfecta.
- Estratificar es **crítico** con desbalance — sin esto el test podría tener 5% o 18% de churn por azar.
- Un único split reutilizado en ambos modelos → resultados comparables.
- Mencionar al pasar: **CART no necesita escalado** (a diferencia de KNN).

**Trampa:** *"¿El árbol no podría manejar categóricas directo?"* — LightGBM/CatBoost sí, sklearn no. Mencionarlo porque va a aparecer en la documentación.

---

## Celdas 19-28 — Parte A · Clasificación

### 19-20 · Entrenamiento

Tres hiperparámetros:

| | Valor | Por qué |
|---|---|---|
| `max_depth=3` | 3 niveles | Legibilidad + mejor recall en test (validado) |
| `min_samples_leaf=15` | mínimo 15 obs/hoja | Evita reglas espurias |
| `class_weight="balanced"` | pondera 12% churners | Sin esto recall ~5% |

### 21 · Métricas

Esperás ver algo cercano a:

```
Matriz:
[[277 118]
 [ 11  44]]

Reporte:
              precision  recall  f1
    Se queda     0.96     0.70   0.81
       Churn     0.27     0.80   0.41

Accuracy train: 0.702 | Accuracy test: 0.713
```

**Cómo leerlo — corazón de la clase:**
- **Recall Churn 0.80** → captamos 8 de cada 10 churners reales.
- **Precision Churn 0.27** → de 100 marcados, 27 son churners; el resto, falsos positivos.
- **Train ≈ Test → no overfit.**

**Trade-off para verbalizar:**
- Modelo **inclusivo**: tira la red ancha. Captura casi todos los churners pero también marca usuarios que iban a quedarse.
- En Retention el costo de un falso positivo (cupón) es bajo; el costo de no detectar un churner real es el LTV completo. **Por eso priorizamos recall.**

**Pregunta para el grupo:** *"si Retention solo pudiera contactar 50 usuarios por semana, ¿priorizarían precision o recall?"*. La respuesta cambia con la restricción.

### 22-23 · Cómo se lee + Árbol visual

Cel. 22 (md) explica cada componente de las cajas. **Es la celda que salva la clase** — sin esto, "interpretabilidad" es palabra vacía.

Cel. 23: `plot_tree` (14×7, fontsize 10). Con `max_depth=3` hay ~8 hojas → cajas grandes y legibles.

**Para decir cuando aparece el árbol:**
- *"Lo que se ve en pantalla resume por qué CART le gana a otros modelos: la salida no es una probabilidad opaca, es un conjunto de reglas explícitas."*
- Dedicar 2-3 minutos a recorrer una hoja en voz alta:
  - *"Si los días sin entrar > X y las horas vistas < Y → Z% probabilidad de churn → llamar mañana."*
- El primer corte casi seguro va a ser `dias_desde_ultima_sesion` — recencia es el predictor #1.

**Trampa:** los `value=[X, Y]` están **ponderados por `class_weight`**, no son observaciones crudas. Al sumarlos no coinciden con `samples`. Aclararlo si alguien pregunta.

### 24 · Lectura del árbol (md)

Recencia es predictor #1. Hojas oscuras → segmentos prioritarios para Retention.

### 25-26 · Importancia de variables

Barplot horizontal de `feature_importances_`. **Versión cuantitativa** de lo que se ve en el árbol.

**Para decir:** útil para presentaciones ejecutivas — "estas 3 variables explican el 90% del churn". Si una feature de la tabla de variables (cel. 5) no aparece, el árbol no la usó.

### 27-28 · Reglas en texto (`export_text`)

Misma información del árbol visual, formato lineal. *"Si Retention te pide pasame las reglas para copiar al documento, es esto."*

Mostrar brevemente y pasar — el árbol visual ya es el formato principal.

---

## Celdas 29-34 — Parte B · Regresión

### 29-30 · Entrenamiento + métricas

Mismo árbol, target continuo. `min_samples_leaf=30` más alto para promedios estables.

Esperás:

```
MSE:  125.77
RMSE: 11.21 horas
R2:   0.687

R² train: 0.689 | R² test: 0.687
```

**Cómo leerlo:**
- **RMSE = 11 horas** → error típico de la predicción. *"Si predice 30 h y el usuario consume 41, el error es 11 — cerca del RMSE."* RMSE está en horas porque el target está en horas.
- **R² = 0.69** → el modelo explica el 69% de la variabilidad. Es un buen número para comportamiento humano.
- **Train ≈ Test** → tampoco overfit.

**Para decir:**
- R² no es una nota absoluta. Lo razonable depende del dominio. Acá es lo que los datos permiten.
- RMSE expresado en horas es la métrica que el negocio entiende — más útil que un R² aislado.

**Pregunta probable:** *"¿Y si subimos `max_depth`?"* — R² train sube, R² test queda igual o cae. A partir de `depth=5` el gap se abre. Lo validamos antes de la clase.

### 31-33 · Árbol de regresión

Mismo formato visual, pero ahora cada hoja contiene un **valor numérico** = horas esperadas para esa cohorte.

**Para decir:**
- Cada hoja es un **segmento de consumo**. Insumo directo para LTV por segmento y para que Contenido sepa cuántas horas-vista empujar por cohorte.
- **Conexión con el árbol de clasificación:** las variables que cortan son las mismas (recencia + consumo previo). Recencia y horas predicen tanto la probabilidad de churn como las horas futuras → coherencia conceptual.

### 34 · Cierre del bloque regresión

Markdown breve sobre LTV y Pricing.

---

## Celda 35 — Cierre

Responde explícitamente las dos preguntas del header, da la acción operativa por área de negocio, justifica por qué CART y deja el gancho a la próxima clase.

**Para cerrar en clase:**

1. **Volver a las dos preguntas del principio.** Mostrar que las respondimos con métricas concretas.
2. **Acción de negocio:** Retention contacta el 80% identificado aceptando precision 27%; Pricing/Content/Finance usan las cohortes del árbol de regresión para sus cálculos.
3. **Interpretabilidad como ventaja.** *"Cuando el CFO pregunta por qué llamamos a Juan, la respuesta es: hace 22 días que no entra y tiene el plan más barato."*
4. **Gancho a la próxima:** ensembles (Random Forest, Gradient Boosting).

---

## Preguntas frecuentes (anticipar)

**"¿Por qué Gini y no entropía?"** — Producen árboles muy similares. Gini es el default y se calcula más rápido.

**"¿El árbol está overfiteado?"** — No, y queda demostrado en pantalla: celdas 21 y 31 imprimen `train ≈ test`. La validación previa probó depth 2-8; a partir de 5 el gap empieza a abrirse.

**"¿Por qué no usar KNN?"** — Requiere escalado, predice lento, no produce reglas legibles. Para un caso con interpretabilidad como prioridad, CART gana.

**"¿Cómo elegir `max_depth`?"** — GridSearchCV (viene en clases siguientes). Heurística: 3-5 niveles para problemas con 10-20 features y miles de filas.

**"¿Y si el dataset cambia?"** — CART es estático. Cada mes nuevo → reentrenar.

---

## Timing sugerido (clase de 20-22 minutos)

| Bloque | Celdas | Tiempo |
|---|---|---|
| Header + carga + tabla variables | 0-5 | 2 min |
| EDA: balance + 3 viz + observaciones + describe | 6-15 | 4 min |
| Data prep | 16-18 | 2 min |
| **Parte A — Clasificación** (fit + métricas + árbol + importancia + reglas) | 19-28 | **7 min** |
| **Parte B — Regresión** (fit + métricas + árbol) | 29-34 | **5 min** |
| Cierre — responder las dos preguntas | 35 | 1-2 min |
| **Total** | 36 | **~21 min** |

**Cortes si vas corto de tiempo:** `export_text` (celda 28) se puede saltar — el árbol visual ya tiene la info. Si necesitás recortar más, las 3 viz del EDA (10-12) se pueden pasar más rápido sin perder pedagogía.
