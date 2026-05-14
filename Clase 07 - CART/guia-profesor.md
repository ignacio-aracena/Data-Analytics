# Clase 07 — CART · Guía del profesor

Documento de preparación para la tutorial. **Duración objetivo: 20 minutos** en exposición + lectura de outputs. Foco en **modelado y validación (métricas)**. El EDA extendido, las visualizaciones complementarias y la inspección detallada del árbol se trabajan en "Para casa".

Recorrido celda por celda con:

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

**Limitación:** un árbol individual tiende al overfitting. La solución (Random Forest, Gradient Boosting) se aborda en clases siguientes.

---

## Celda 0 — Header del caso

**Qué se ve:** encuadre Netflix LATAM, las dos preguntas (churn + horas) y la nota de que la clase ocurre en la etapa de Modeling de CRISP-DM.

**Para decir:**

- Subrayar que el dataset **llega limpio** — la limpieza fue parte de las Clases 02 y 04.
- Hoy el foco está en **modelar y evaluar**, no en preparar datos.
- Las dos preguntas planteadas son las que un equipo de Retention real se hace cada semana.

---

## Celda 1 — Imports

**Qué se ve:** carga silenciosa de librerías.

**Para decir:** señalar el bloque de `sklearn.tree` — importamos los dos modelos (`DecisionTreeClassifier`, `DecisionTreeRegressor`) y dos utilidades clave (`plot_tree` para visualización, `export_text` para reglas en texto).

---

## Celdas 2-5 — Carga y vistazo (5 celdas)

**Qué se ve:**

- Cel. 3: shape (1500 × 11) más primeras filas.
- Cel. 4: `df.info()` confirma que no hay nulos y los tipos son correctos.
- Cel. 5: tabla de referencia con las variables disponibles.

**Cómo leerlo:** 1500 filas son suficientes para un árbol con `max_depth` acotado. 11 columnas, dos targets (`churn_30d` y `horas_proximo_mes`).

**Para decir:**

- No hay nulos → no toca imputar.
- Tener **dos targets en el mismo dataset** (uno binario, uno continuo) es lo que permite resolver clasificación y regresión sobre la misma base.

---

## Celdas 6-8 — EDA mínimo: balance del target

**Qué se ve:**

- Cel. 7 (código): conteo y proporción del target `churn_30d`.
  ```
  0    ~1320  (88%)
  1    ~180   (12%)
  ```
- Cel. 8 (markdown): la observación operativa — 12% es churn → desbalanceado → vamos a usar `class_weight="balanced"`.

**Cómo leerlo:** 12% es churn — **dataset desbalanceado**. Sin compensación, un clasificador predeciría "todos se quedan" y obtendría 88% de accuracy con recall de churn igual a cero. Es lo opuesto al objetivo de negocio.

**Para decir en clase:**

- Este es el único output del EDA que llevamos al core. **Por qué importa:** justifica directamente el `class_weight="balanced"` que va a aparecer en la celda 13.
- Pregunta para el grupo: *"si un modelo acierta 88% pero no detecta a ningún churner, ¿le sirve al equipo de Retention?"*. La respuesta es evidente, pero conviene que la formulen ellos.

**Conexión con la Clase 06 (Métricas):** accuracy es engañosa cuando hay desbalance. La métrica que importa en este caso es el **recall de la clase minoritaria** (Churn).

**Nota sobre el resto del EDA:** las visualizaciones de tasa de churn por plan, boxplot de horas vistas (con la discusión de outliers) y boxplot de recencia están en **"Para casa"**. Si algún alumno pregunta por más exploración, derivalo allí — es material que pueden trabajar entre clases.

---

## Celdas 9-11 — Data prep

**Qué se ve:**

- Cel. 10: `df_modelo` con más columnas tras `pd.get_dummies(..., drop_first=True)`. Pasa de 11 a aproximadamente 20.
- Cel. 11: `X_train: 1050 filas | X_test: 450 filas`. Split 70/30 estratificado.

**Cómo leerlo:**

- **One-hot encoding** convierte categóricas en binarias. `drop_first=True` evita multicolinealidad perfecta entre las dummies.
- **Train/test split** estratificado por `churn_30d` mantiene el 12% de churn en ambas particiones.
- `random_state=42` para reproducibilidad.
- **Decisión metodológica:** un único split, reutilizado para los dos modelos. Hace los resultados comparables.

**Para decir:**

- sklearn requiere features numéricas — por eso el one-hot.
- Estratificar es **crítico** con desbalance: sin estratificación, el test set podría tener 5% de churn por azar.
- Reusar el mismo split en clasificación y regresión no es opcional, es la práctica correcta.

**Trampa pedagógica:**

> *"¿El árbol no podría manejar categóricas directamente?"*

Otros frameworks como LightGBM o CatBoost sí lo hacen de manera nativa. sklearn no — exige features numéricas. Mencionarlo porque va a aparecer en la documentación que consulten.

---

## Celda 12 — Markdown Parte A (intro)

Anticipa el modelo de clasificación con sus hiperparámetros clave.

---

## Celda 13 — Entrenamiento del clasificador

**Qué se ve:** ejecución silenciosa de `fit`.

**Cómo leerlo:** se entrena el árbol con tres restricciones explícitas:

| Hiperparámetro | Valor | Justificación |
|---|---|---|
| `max_depth=4` | profundidad máxima 4 niveles | Mantiene el árbol **legible**. Mayor profundidad significa más nodos y un árbol imposible de explicar al área de negocio. |
| `min_samples_leaf=15` | mínimo 15 observaciones por hoja | Evita hojas pequeñas (reglas espurias que no generalizan). |
| `class_weight="balanced"` | pondera la clase minoritaria | Sin este parámetro, el recall de churn cae por debajo del 5% (consecuencia directa del 12% de la celda 7). |

**Para decir en clase (sección importante, dedicale tiempo):**

- **`max_depth` es el control principal contra el overfitting.** Profundidad chica subajusta, profundidad grande sobreajusta. 4 es razonable para este problema.
- **`class_weight="balanced"`** fue introducido en la Clase 05 con regresión logística. Misma lógica aquí.
- Los tres hiperparámetros responden a decisiones concretas: `max_depth` resuelve interpretabilidad, `min_samples_leaf` resuelve robustez, `class_weight` resuelve desbalance.

**Pregunta probable:**

> *"¿Por qué `max_depth=4` y no `max_depth=10`?"*

Trade-off entre ajuste en training, generalización en test e interpretabilidad. En esta clase se prioriza interpretabilidad porque el caso lo requiere. Si la explicabilidad no fuera prioritaria, se podría aumentar la profundidad y compensar el overfitting con un ensemble.

---

## Celdas 14-15 — Métricas de clasificación

**Qué se ve:**

- Cel. 14: matriz de confusión + reporte de clasificación (precision, recall, F1) impresos.
  ```
  Matriz:
  [[~340  ~55]
   [ ~12  ~43]]

  Reporte:
                  precision  recall  f1-score
  Se queda        0.97       0.86    0.91
  Churn           0.44       0.78    0.56
  ```
- Cel. 15: heatmap rojo de la matriz de confusión.

**Cómo leerlo — punto central de la clase:**

- **Precision de Churn ≈ 0.44:** de cada 100 usuarios marcados como churners, 44 lo serán realmente.
- **Recall de Churn ≈ 0.78:** de cada 100 churners reales, el modelo detecta 78.
- **F1 ≈ 0.56:** media armónica entre precision y recall.

**El trade-off a explicar:**

- Precision baja con recall alto indica que el modelo es **más inclusivo que selectivo**: marca muchos usuarios como riesgo y captura la mayoría de los churners reales, pero incluye también usuarios que iban a permanecer.
- **¿Es un problema?** Depende del costo de cada error. Enviar un cupón a un falso positivo tiene un costo bajo. NO detectar a un churner real implica perder el LTV completo del cliente. En Retention **el recall pesa más que la precision**.

**Para decir en clase:**

- Este es el contenido de la Clase 06 aplicado en un caso real. Si los alumnos no internalizan esta sección, no comprenden CART aplicado.
- Pregunta para el grupo: *"si Retention solo tuviera presupuesto para contactar 50 usuarios por semana, ¿priorizarían precision alta o recall alto?"*. La respuesta cambia con la restricción.

---

## Celda 16 — Visualización del árbol de clasificación

**Qué se ve:** **el árbol completo** con cajas de colores. Cada caja muestra:

- La regla del corte (por ejemplo, `dias_desde_ultima_sesion <= 12.5`).
- El `gini` del nodo (impureza, 0 = nodo puro).
- `samples` (observaciones en ese nodo).
- `value` (distribución de clases — al usar `class_weight="balanced"`, los valores están **ponderados**, no son crudos).
- `class` (la clase mayoritaria).

Código de colores: azul = "Se queda", rojo/naranja = "Churn". La intensidad refleja la pureza del nodo.

**Cómo leerlo paso a paso:**

1. **Nodo raíz:** la primera variable elegida como corte. En este caso, casi con certeza es `dias_desde_ultima_sesion` — la recencia es el predictor más fuerte.
2. **Recorrer una rama:** cada nodo es una pregunta sí/no. La hoja final indica que esa combinación de reglas predice una clase específica.
3. **Hojas oscuras de rojo:** segmentos de mayor riesgo. Son los usuarios que Retention debe contactar prioritariamente.
4. **Hojas azules:** clientes con riesgo bajo, no requieren intervención.

**Para decir en clase — sección de mayor impacto pedagógico:**

- *"Lo que se ve en pantalla resume la diferencia entre CART y regresión logística: la salida no es una probabilidad opaca, es un conjunto de reglas explícitas. El equipo de Retention puede leer el árbol y construir su workflow de contacto sin necesidad de comprender machine learning."*
- Dedicar 2-3 minutos a recorrer una hoja en voz alta:
  - *"Si los días sin entrar son mayores a 14 y las horas vistas son menores a 5, hay 80% de probabilidad de churn → llamar mañana."*

**Trampa pedagógica:**

Los `value=[X, Y]` están ponderados por `class_weight`. Al sumarlos no coinciden con `samples`. Aclarar: "los `samples` son las observaciones reales, los `value` son la representación ponderada que el árbol usa internamente para decidir los cortes".

---

## Celda 17 — Lectura del árbol (markdown)

**Qué se ve:** observación breve sobre la lectura del árbol.

**Para decir:** permitir que el grupo extraiga la conclusión central — la recencia es el predictor #1, el plan queda en segundo plano. Este resultado **invierte la intuición inicial**: uno esperaría que el plan tuviera más peso predictivo.

---

## Celda 18 — Markdown Parte B (intro)

Anuncia el cambio de target a continuo. Aclarar:

- **Misma estructura**, mismo `max_depth`, mismo `random_state`.
- Solo cambian la clase del estimador (`DecisionTreeRegressor`) y el target.
- La métrica interna que minimiza ahora es **MSE** en lugar de Gini.

Es el corazón conceptual de la clase: dos problemas distintos resueltos con el mismo algoritmo.

---

## Celdas 19-20 — Entrenamiento y métricas del regresor

**Qué se ve:**

- Cel. 19: `fit` silencioso. `min_samples_leaf=30` es ligeramente más alto que en clasificación para que el promedio de cada hoja sea estable.
- Cel. 20:
  ```
  MSE:  ~280
  RMSE: ~17 horas
  R2:   ~0.27
  ```

**Cómo leerlo:**

- **RMSE ≈ 17 horas:** error típico de la predicción. Si el modelo predice 30h y el usuario consume 47h, el error es 17h.
- **R² ≈ 0.27:** el modelo explica el 27% de la variabilidad de las horas consumidas. **Es un valor moderado** — el consumo de horas es volátil. Conviene ser transparente con el grupo: un árbol único no produce predicciones muy precisas en esta tarea.

**Para decir:**

- **R² no debe leerse como una calificación absoluta.** Lo razonable depende del dominio. Acá es lo que los datos permiten.
- **RMSE expresado en unidades del target** (horas) es la métrica que el área de negocio comprende — más útil que un R² aislado.

**Pregunta probable:**

> *"¿Qué pasaría si subimos `max_depth` a 10?"*

R² en training sube; R² en test probablemente se mantiene o cae. Es el patrón clásico de overfitting. Si hay tiempo se puede demostrar en vivo, si no queda como ejercicio del TP.

---

## Celdas 21-23 — Visualización del árbol de regresión

**Qué se ve:**

- Cel. 21 (markdown): intro corta.
- Cel. 22 (código): `plot_tree` del regresor. Cada caja muestra:
  - Regla del corte.
  - `squared_error` del nodo (la versión continua de Gini).
  - `samples`.
  - `value` (el promedio del target en ese nodo — el valor que el modelo predice si una observación cae allí).
- Cel. 23 (markdown): cierre operativo (insumo para LTV / Contenido).

**Cómo leerlo:**

- Cada hoja contiene un valor numérico — **horas esperadas para los suscriptores que caen en esa hoja**.
- El primer corte va a ser otra vez `dias_desde_ultima_sesion` (consistente con el árbol de clasificación).
- Las hojas con valores altos son segmentos de alto consumo; las hojas con valores bajos son segmentos de bajo consumo.

**Para decir en clase:**

- *"Las hojas de este árbol son segmentos de consumo. Cada una es un perfil con un valor esperado de horas. Este es el insumo directo para calcular **LTV por segmento** (cuánto vale económicamente cada cohorte) y para que el equipo de Contenido sepa cuántas horas-vista empujar en cada grupo."*
- Mostrar **la conexión con el árbol de clasificación**: las variables que cortan son básicamente las mismas. Recencia y consumo previo predicen tanto la probabilidad de churn como la cantidad de horas que va a ver. Coherencia conceptual.

---

## Celdas 24-26 — Predicción operativa sobre 5 nuevos suscriptores

**Qué se ve:**

- Cel. 25: tabla con cinco perfiles representativos:
  1. **Nuevo + plan barato + recencia alta** → candidato fuerte a churn.
  2. **Veterano + premium + alto consumo + sesión reciente** → cliente saludable.
  3. **Medio + estándar + consumo medio** → cliente promedio.
  4. **Nuevo + básico + recencia alta + dos cambios de plan** → riesgo.
  5. **Veterano + premium + consumo muy alto + sesión actual** → cliente top.

- Cel. 26: la misma tabla con tres columnas adicionales: `prob_churn`, `horas_proximo_mes`, `accion_retention`. La acción se determina con reglas simples:
  - Probabilidad ≥ 0.50 → "Contactar urgente"
  - 0.25 ≤ probabilidad < 0.50 → "Mandar promo"
  - Probabilidad < 0.25 → "No tocar"

**Cómo leerlo:** este es el output que se entrega al negocio. Convierte probabilidades en **acciones operativas concretas**.

**Para decir en clase — punto de cierre del modelo:**

- *"Los modelos no le aportan valor al negocio hasta que se traducen en acción. Una probabilidad por sí sola no es accionable."*
- Los thresholds (0.50, 0.25) son decisiones de negocio, no del modelo. Modificarlos cambia el volumen de usuarios contactados — son palancas operativas.
- En producción, esto se implementa como un proceso diario que corre sobre toda la base de usuarios y entrega un archivo al equipo de Retention. **Así se opera ML en negocios.**

---

## Celdas 27-41 — "Para casa"

Bloque optativo (que entra al parcial). Se muestra por arriba, **sin profundizar en clase**.

Contenido:

1. **EDA — ¿quiénes churnean?** (tasa por plan + boxplot horas + observaciones con outliers).
2. **Recencia** (boxplot adicional).
3. **Describe completo**.
4. **Reglas del árbol en texto** (`export_text`).
5. **Importancia de variables** (`feature_importances_`).
6. **Predicho vs real** (scatter del regresor).

**Tres puntos breves a mencionar al pasar por estas celdas en clase:**

- **Outliers:** cuando los alumnos vean el boxplot de horas con puntos sueltos arriba, el reflejo de la Clase 04 va a ser "removerlos". Aclarar: **CART es robusto a outliers** porque corta por umbrales — un usuario que vio 95 o 200 horas cae del mismo lado del corte. No se remueven. Esto es lo que diferencia a CART de regresión lineal (Clase 04) y de KNN (Clase 05), ambos sensibles a outliers.
- **`export_text`:** si el negocio pide las reglas "para copiar en un documento", esta es la herramienta. Misma información del árbol visual en formato texto plano.
- **Importancia de variables:** confirma cuantitativamente lo que el árbol mostró visualmente. Más concisa para presentaciones ejecutivas.

---

## Celda 42 — Cierre

**Qué se ve:** tabla resumen y tres ideas finales.

**Para decir al cerrar:**

1. **Recapitular la tabla.** Misma técnica aplicada a dos problemas distintos.
2. **Interpretabilidad como ventaja competitiva.** Cada predicción de un árbol viene con la secuencia de reglas que la generó. Es lo que el área de negocio valora especialmente.
3. **Enlace con la próxima clase.** Un árbol individual tiene tendencia al overfitting. La solución industrial es combinar muchos árboles: Random Forest y Gradient Boosting.

---

## Preguntas frecuentes (anticipar)

### "¿Por qué Gini y no entropía?"

Ambos criterios producen árboles muy similares. Gini es el default de sklearn y se calcula más rápido. Si se quiere comparar, basta con cambiar `criterion="entropy"` y reentrenar — la diferencia es mínima.

### "¿El árbol está overfiteado?"

Con `max_depth=4` y `min_samples_leaf=15` es poco probable. Para verificarlo:

```python
print(f"Accuracy train: {arbol_clf.score(X_train, yclf_train):.3f}")
print(f"Accuracy test:  {arbol_clf.score(X_test, yclf_test):.3f}")
```

Diferencia menor a 0.05 → no hay overfitting significativo.

### "¿Por qué no usar KNN aquí?"

KNN podría aplicarse, pero requiere escalado, predice lentamente en producción y **no produce reglas legibles**. Para un caso donde la interpretabilidad es prioritaria, CART es la elección correcta.

### "¿Cómo elegir `max_depth`?"

Búsqueda en grilla con `GridSearchCV` — herramienta que se introduce en clases posteriores. Heurística práctica: 3-5 niveles para problemas con 10-20 features y miles de observaciones.

### "¿Qué pasa si el dataset cambia mes a mes?"

CART aprende del dataset que se le entrega. Cada nuevo mes requiere un reentrenamiento que reemplaza el árbol en producción.

---

## Timing sugerido (clase de 20 minutos)

| Bloque | Celdas | Tiempo |
|---|---|---|
| Header + imports + carga + tabla variables | 0-5 | 2 min |
| EDA mínimo: balance del target → justificación de `class_weight` | 6-8 | 2 min |
| Data prep: one-hot + split estratificado | 9-11 | 2 min |
| **Parte A: clasificación** — fit + métricas + matriz + árbol + lectura | 12-17 | **6 min** |
| **Parte B: regresión** — fit + métricas + árbol + lectura | 18-23 | **5 min** |
| Predicción operativa sobre 5 nuevos suscriptores | 24-26 | 2 min |
| Cierre + repaso de "Para casa" | 27-42 | 1 min |
| **Total** | | **20 min** |

Si la clase corre corta, "Para casa" se muestra solo de nombre (30 segundos). Si corre larga, la matriz de confusión visual (celda 15) puede saltarse — el reporte numérico (celda 14) ya cubre la información.
