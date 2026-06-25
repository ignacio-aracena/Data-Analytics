# RESPUESTAS — EXAMEN DE PRÁCTICA ANALÍTICA DE DATOS

> Cada respuesta incluye la(s) opción(es) correcta(s), una explicación breve y los pasos para llegar al resultado. En las preguntas con múltiples respuestas, marcar una opción incorrecta **descuenta 1 punto**, así que si no estás seguro de una opción, es mejor dejarla en blanco.

---

## PARTE 1: MÚLTIPLE CHOICE

---

### Pregunta 1 — Normalización y escalado

**Respuestas correctas: A, C, D**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | Min-Max por definición escala al rango [0, 1]: `(x - min) / (max - min)` |
| B | ✗ Incorrecta | Los árboles de decisión (CART) **no necesitan escalado**. Cortan por umbrales, no por distancias. Solo KNN, regresión logística y SVM lo requieren. |
| C | ✓ Correcta | La fórmula Z-score es `(x - media) / std`. Por construcción, la media del resultado es 0 y la std es 1. |
| D | ✓ Correcta | Si calculás la media/min/max sobre todo el dataset (incluyendo el test), le estás "filtrando" información del futuro al modelo. Esto se llama **data leakage**. Siempre calculá los parámetros solo sobre train y luego aplicalos al test. |

---

### Pregunta 2 — Tratamiento de valores faltantes

**Respuestas correctas: A, C, D**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | Eliminar filas con faltantes es válido (listwise deletion). Tiene costo: perdés datos, pero no introduce sesgo. |
| B | ✗ Incorrecta | Imputar con el valor **máximo** introduce sesgo severo hacia la cola superior de la distribución. No hay justificación estadística para esta estrategia. |
| C | ✓ Correcta | Media (cuando la distribución es simétrica) o mediana (cuando hay outliers o asimetría) son estrategias estándar para variables numéricas. |
| D | ✓ Correcta | Para variables categóricas, crear la categoría "Sin Dato" preserva la información de que el dato faltó (que puede ser una señal en sí misma, ej: en un formulario bancario, dejar vacío el campo de ingresos puede ser relevante). |

---

### Pregunta 3 — Cálculo de Recall

**Respuesta correcta: C) 0.875**

**Datos:** VP = 70 | FP = 30 | FN = 10 | VN = 90

**Pasos:**

$$\text{Recall} = \frac{VP}{VP + FN} = \frac{70}{70 + 10} = \frac{70}{80} = 0.875$$

> **Cómo recordarlo:** Recall mira la fila de los positivos reales. "De todos los enfermos reales, ¿cuántos detecté?" Denominador = todos los que eran positivos (VP + FN).

---

### Pregunta 4 — Selección de métrica según contexto

**Respuesta correcta: C) Recall (Sensibilidad)**

**Razonamiento:**

El costo de **no detectar** un efecto secundario (Falso Negativo) es extremadamente alto. En términos de la matriz de confusión, queremos minimizar los FN → maximizar el **Recall**.

| Métrica | Qué penaliza | ¿Aplica acá? |
|---------|--------------|--------------|
| Accuracy | Errores totales | No — clases desbalanceadas |
| Precisión | Falsos Positivos | No — el costo está en los FN |
| **Recall** | **Falsos Negativos** | **Sí — es el costo relevante** |
| Especificidad | Falsos Positivos sobre negativos reales | No |

> Regla general: **si el costo de no detectar es alto → priorizar Recall**. Si el costo de una alarma falsa es alto → priorizar Precisión.

---

### Pregunta 5 — Overfitting

**Respuestas correctas: B, C**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✗ Incorrecta | Aumentar la profundidad **empeora** el overfitting: el árbol memoriza más casos del training. |
| B | ✓ Correcta | La poda (pruning) elimina ramas que no generalizan bien, reduciendo la complejidad del modelo. |
| C | ✓ Correcta | K-fold cross-validation evalúa el modelo en múltiples subconjuntos, detectando si hay diferencia grande entre train y test (señal de overfitting). También permite elegir hiperparámetros más robustos. |
| D | ✗ Incorrecta | Agregar más variables sin criterio puede **aumentar** el overfitting: el modelo aprende ruido. El criterio de selección de variables es clave (importancia, correlación, dominio de negocio). |

---

### Pregunta 6 — Método del codo

**Respuestas correctas: A, B, D**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | El objetivo del método del codo es precisamente elegir K. |
| B | ✓ Correcta | El eje Y del gráfico es la **inercia** (suma de distancias cuadradas de cada punto a su centroide). A mayor K, menor inercia. |
| C | ✗ Incorrecta | El método del codo es una **heurística orientativa**, no garantiza el óptimo. En datasets con clusters muy superpuestos, el "codo" puede no ser visible o ambiguo. |
| D | ✓ Correcta | Esta es la lógica del método: buscás el punto donde la inercia deja de bajar rápido (el "codo"). Agregar más clusters después de ese K da rendimientos decrecientes. |

---

### Pregunta 7 — Clustering jerárquico aglomerativo

**Respuestas correctas: A, C, D**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | "Aglomerativo" = de abajo hacia arriba. Cada observación empieza como su propio cluster y se van fusionando de a pares según similitud. |
| B | ✗ Incorrecta | Esta es la diferencia clave con K-Means: **no necesitás definir K de antemano**. El dendrograma muestra todas las posibilidades de corte. |
| C | ✓ Correcta | El dendrograma es la visualización propia del clustering jerárquico. El eje Y muestra a qué distancia se fusionaron los clusters. |
| D | ✓ Correcta | Tiene complejidad O(n³) en implementaciones básicas, vs O(n·K·it) de K-Means. Para millones de registros, K-Means escala mucho mejor. |

---

### Pregunta 8 — Caso de negocio: clases desbalanceadas

**Respuestas correctas: A, B, D**

**Modelo que siempre predice "legítima":** VP = 0, FP = 0, FN = todos los fraudes (2%), VN = todas las legítimas (98%)

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | Accuracy = predicciones correctas / total = (0 + 0.98·n) / n = **0.98** (98%). Acertó en todas las legítimas. |
| B | ✓ Correcta | Recall (Fraude) = VP / (VP + FN) = 0 / (0 + todos los fraudes) = **0%**. No detectó ningún fraude. |
| C | ✗ Incorrecta | Un modelo que no detecta ningún fraude es completamente **inútil** para el negocio, a pesar de su accuracy del 98%. Este es el ejemplo clásico de por qué accuracy falla con clases desbalanceadas. |
| D | ✓ Correcta | Precisión (Fraude) = VP / (VP + FP) = 0 / 0 = **indefinida** (división por cero). En la práctica se suele reportar como 0. |

---

### Pregunta 9 — Índice de Gini

**Respuestas correctas: A, B, D**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | Gini = 0 significa que todas las instancias son de la misma clase. Fórmula: `1 - Σpᵢ²`. Si p₁=1 y p₂=0: `1 - (1 + 0) = 0`. |
| B | ✓ Correcta | El árbol elige la variable que, al dividir, produce el **menor** Gini ponderado (mayor reducción de impureza). |
| C | ✗ Incorrecta | Para clasificación **binaria**, el máximo del Gini es **0.5** (cuando las clases son 50/50): `1 - (0.5² + 0.5²) = 1 - 0.5 = 0.5`. El valor 1 solo sería posible con infinitas clases perfectamente equilibradas. |
| D | ✓ Correcta | Esta es la interpretación intuitiva del Gini: la probabilidad de clasificar mal una instancia elegida al azar si la asignás según la distribución de clases del nodo. |

---

### Pregunta 10 — Naive Bayes

**Respuestas correctas: A, C**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | El "naive" (ingenuo) de Naive Bayes es justamente este supuesto: asume que las variables son independientes entre sí, condicionadas a la clase. |
| B | ✗ Incorrecta | Naive Bayes funciona muy bien con **pocos datos**. Es una de sus ventajas frente a modelos más complejos como Random Forest. |
| C | ✓ Correcta | Naive Bayes es naturalmente multiclase. El Teorema de Bayes calcula P(Clase|Features) para cada clase y elige la de mayor probabilidad. |
| D | ✗ Incorrecta | Naive Bayes **no es sensible a la escala** porque trabaja con probabilidades, no con distancias euclidianas (a diferencia de KNN, que sí lo es). |

---

### Pregunta 11 — Random Forest

**Respuestas correctas: A, C, D**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | Random Forest es un ensemble: combina cientos de árboles entrenados de forma independiente y promedia sus predicciones. |
| B | ✗ Incorrecta | Cada árbol se entrena con una **muestra bootstrap** (muestreo con reemplazo, ~63% de los datos originales). Además, en cada split solo considera un subconjunto aleatorio de variables. Esta aleatoriedad es lo que genera diversidad entre árboles. |
| C | ✓ Correcta | La diversidad entre árboles (por el bootstrap y la selección aleatoria de variables) reduce la varianza del modelo, combatiendo el overfitting. Un árbol solo sin restricciones memoriza los datos; el ensemble generaliza. |
| D | ✓ Correcta | La importancia de cada variable se calcula sumando cuánto redujo el Gini (o MSE) en todos los nodos y árboles donde se usó. Es una de las herramientas más útiles de RF para análisis exploratorio. |

---

### Pregunta 12 — Cálculo de F1-Score

**Respuesta correcta: C) 0.667**

**Datos:** VP = 60 | FP = 40 | FN = 20 | VN = 80

**Pasos:**

**1. Calcular Precisión:**
$$\text{Precisión} = \frac{VP}{VP + FP} = \frac{60}{60 + 40} = \frac{60}{100} = 0.60$$

**2. Calcular Recall:**
$$\text{Recall} = \frac{VP}{VP + FN} = \frac{60}{60 + 20} = \frac{60}{80} = 0.75$$

**3. Calcular F1:**
$$\text{F1} = \frac{2 \times \text{Precisión} \times \text{Recall}}{\text{Precisión} + \text{Recall}} = \frac{2 \times 0.60 \times 0.75}{0.60 + 0.75} = \frac{0.90}{1.35} = 0.\overline{6} \approx 0.667$$

> F1 es el promedio armónico de precisión y recall. Penaliza más que el promedio aritmético cuando una de las dos es baja.

---

### Pregunta 13 — Caso de negocio: selección de métrica con restricción

**Respuesta correcta: C) Precisión (Precision)**

**Razonamiento:**

El equipo tiene un presupuesto fijo de **200 contactos** y quiere que esos contactos sean los más efectivos posible (que la mayoría de los contactados realmente fueran a cancelar).

Esto es exactamente la definición de **Precisión**: de todos los que el modelo predice como "va a cancelar", ¿qué porcentaje realmente cancela?

| Si usara... | Resultado |
|-------------|-----------|
| **Precisión alta** | De los 200 contactados, la mayoría son churners reales → eficiencia máxima del presupuesto |
| Recall alto | Capturo más churners totales, pero los 200 contactos incluyen muchos falsos positivos (no iban a cancelar) |
| Accuracy | No es relevante con listas acotadas |

> Clave: cuando tenés una **lista acotada** (presupuesto, cupos, capacidad operativa), la métrica a maximizar es **Precisión**.

---

### Pregunta 14 — Codificación de variables categóricas

**Respuestas correctas: A, B, D**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | Label Encoding asigna 0=Norte, 1=Sur, 2=Este, etc. El modelo puede interpretar que Sur > Norte y Este > Sur, una relación ordinal que no existe. |
| B | ✓ Correcta | One-Hot Encoding crea una columna binaria por cada categoría. Con 5 regiones → 5 columnas. |
| C | ✗ Incorrecta | No es la única. Existen Target Encoding, Frequency Encoding, Binary Encoding, y Label Encoding es válido cuando la variable **sí tiene orden** (ej: nivel educativo). |
| D | ✓ Correcta | Con 5 categorías el impacto es manejable, pero con variables que tienen 50 o 500 categorías (ej: código postal), One-Hot genera una explosión de dimensiones. |

---

### Pregunta 15 — Data leakage

**Respuestas correctas: A, B**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | Si normalizás con datos del test antes de dividir, el modelo "vio" indirectamente los datos de prueba durante el entrenamiento. Es data leakage clásico. |
| B | ✓ Correcta | Si incluís una variable que en producción no existirá al momento de predecir (ej: "resultado del tratamiento" para predecir si el paciente se va a recuperar), el modelo funciona en papel pero falla en producción. |
| C | ✗ Incorrecta | Dividir **antes** de transformar es la **práctica correcta**. Evita exactamente el leakage de la opción A. |
| D | ✗ Incorrecta | Entrenar con datos históricos y evaluar con datos posteriores es la **evaluación correcta** para series temporales. No hay leakage. |

---

### Pregunta 16 — Curva ROC y AUC

**Respuestas correctas: A, B, D**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | AUC = 0.5 es la diagonal del espacio ROC, que corresponde a clasificar al azar (sin capacidad de discriminación). |
| B | ✓ Correcta | La curva ROC tiene en el eje Y el TPR (= Recall = VP / (VP+FN)) y en el eje X el FPR (= FP / (FP+VN)). Al variar el umbral de clasificación se traza la curva. |
| C | ✗ Incorrecta | AUC más alto indica mejor capacidad de discriminación **en promedio sobre todos los umbrales**, pero no garantiza mejor rendimiento con un umbral específico. El umbral óptimo depende del costo de negocio de cada tipo de error. |
| D | ✓ Correcta | AUC = 1 significa que el modelo separa perfectamente las dos clases a todos los umbrales posibles. |

---

### Pregunta 17 — Árbol de decisión: profundidad y generalización

**Respuestas correctas: A, B, D**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | Sin restricciones, el árbol puede crecer hasta tener una hoja por cada instancia del training. Memoriza en vez de generalizar → overfitting. |
| B | ✓ Correcta | Si el árbol memoriza los datos de train, su accuracy en train es perfecta (o casi). Siempre mayor que la de un árbol podado que sacrifica training accuracy para ganar generalización. |
| C | ✗ Incorrecta | La palabra clave es "**siempre**". En realidad, el árbol profundo generalmente tiene **menor** accuracy en test (por overfitting), no mayor. Un árbol podado suele generalizar mejor. |
| D | ✓ Correcta | Limitar `max_depth`, `min_samples_leaf`, etc., son formas de regularización: fuerzan al modelo a aprender patrones más generales y no memorizar. |

---

### Pregunta 18 — K-Means: características y limitaciones

**Respuestas correctas: A, B, D**

| Opción | Veredicto | Por qué |
|--------|-----------|---------|
| A | ✓ Correcta | K-Means inicializa los centroides de forma aleatoria. Con distintas inicializaciones puede converger a soluciones diferentes. Por eso se usa `random_state` para reproducibilidad, o K-Means++ para una inicialización más inteligente. |
| B | ✓ Correcta | Definir K es un prerequisito de K-Means. Si no sabés cuántos clusters querés, usás el método del codo o clustering jerárquico. |
| C | ✗ Incorrecta | K-Means es **sensible** a outliers porque usa la **media** para calcular los centroides. Un outlier puede "arrastrar" el centroide hacia él. |
| D | ✓ Correcta | K-Means minimiza distancias euclidianas, lo que lo hace óptimo para clusters esféricos y de tamaño similar. Con clusters elongados, de densidad variable, o con formas irregulares, falla. |

---

---

## PARTE 2: EJERCICIOS PRÁCTICOS

---

### Ejercicio 1 — Árbol de Decisión: Índice de Gini

**Datos del dataset (12 clientes):**

| ID | Edad   | Nivel_Ingresos | Compra |
|----|--------|----------------|--------|
| 1  | Joven  | Alto           | No     |
| 2  | Joven  | Alto           | No     |
| 3  | Adulto | Alto           | Sí     |
| 4  | Senior | Medio          | Sí     |
| 5  | Senior | Bajo           | Sí     |
| 6  | Senior | Bajo           | No     |
| 7  | Adulto | Bajo           | Sí     |
| 8  | Joven  | Medio          | No     |
| 9  | Joven  | Bajo           | Sí     |
| 10 | Senior | Medio          | Sí     |
| 11 | Adulto | Medio          | Sí     |
| 12 | Adulto | Alto           | Sí     |

**Conteo total:** 12 instancias → **Compra Sí: 8** (IDs 3,4,5,7,9,10,11,12) | **Compra No: 4** (IDs 1,2,6,8)

---

#### a) Gini del nodo raíz *(4 puntos)*

**Fórmula:** `Gini = 1 - Σ(pᵢ²)` donde pᵢ es la proporción de cada clase.

$$p(\text{Sí}) = \frac{8}{12} = \frac{2}{3} \qquad p(\text{No}) = \frac{4}{12} = \frac{1}{3}$$

$$\text{Gini}_{\text{raíz}} = 1 - \left[\left(\frac{2}{3}\right)^2 + \left(\frac{1}{3}\right)^2\right] = 1 - \left[\frac{4}{9} + \frac{1}{9}\right] = 1 - \frac{5}{9} = \frac{4}{9} \approx \boxed{0.444}$$

---

#### b) Gini ponderado para la variable **Edad** *(9 puntos)*

**Paso 1 — Distribuir los clientes por categoría de Edad:**

| Categoría | IDs | n | Sí | No |
|-----------|-----|---|----|----|
| Joven | 1, 2, 8, 9 | 4 | 1 (ID 9) | 3 (IDs 1,2,8) |
| Adulto | 3, 7, 11, 12 | 4 | 4 (todos) | 0 |
| Senior | 4, 5, 6, 10 | 4 | 3 (IDs 4,5,10) | 1 (ID 6) |

**Paso 2 — Calcular Gini de cada categoría:**

$$\text{Gini(Joven)} = 1 - \left[\left(\frac{1}{4}\right)^2 + \left(\frac{3}{4}\right)^2\right] = 1 - \left[\frac{1}{16} + \frac{9}{16}\right] = 1 - \frac{10}{16} = \frac{6}{16} = 0.375$$

$$\text{Gini(Adulto)} = 1 - \left[\left(\frac{4}{4}\right)^2 + \left(\frac{0}{4}\right)^2\right] = 1 - [1 + 0] = \boxed{0} \quad \text{(nodo puro)}$$

$$\text{Gini(Senior)} = 1 - \left[\left(\frac{3}{4}\right)^2 + \left(\frac{1}{4}\right)^2\right] = 1 - \left[\frac{9}{16} + \frac{1}{16}\right] = 1 - \frac{10}{16} = \frac{6}{16} = 0.375$$

**Paso 3 — Calcular el Gini ponderado (cada categoría tiene 4/12 = 1/3 del total):**

$$\text{Gini ponderado(Edad)} = \frac{4}{12} \times 0.375 + \frac{4}{12} \times 0 + \frac{4}{12} \times 0.375$$

$$= \frac{1}{3}(0.375 + 0 + 0.375) = \frac{1}{3}(0.75) = \boxed{0.250}$$

---

#### c) Gini ponderado para la variable **Nivel_Ingresos** *(6 puntos)*

**Paso 1 — Distribuir los clientes por categoría de Nivel_Ingresos:**

| Categoría | IDs | n | Sí | No |
|-----------|-----|---|----|----|
| Alto | 1, 2, 3, 12 | 4 | 2 (IDs 3,12) | 2 (IDs 1,2) |
| Medio | 4, 8, 10, 11 | 4 | 3 (IDs 4,10,11) | 1 (ID 8) |
| Bajo | 5, 6, 7, 9 | 4 | 3 (IDs 5,7,9) | 1 (ID 6) |

**Paso 2 — Calcular Gini de cada categoría:**

$$\text{Gini(Alto)} = 1 - \left[\left(\frac{2}{4}\right)^2 + \left(\frac{2}{4}\right)^2\right] = 1 - \left[\frac{1}{4} + \frac{1}{4}\right] = 1 - \frac{1}{2} = 0.500$$

$$\text{Gini(Medio)} = 1 - \left[\left(\frac{3}{4}\right)^2 + \left(\frac{1}{4}\right)^2\right] = 1 - \frac{10}{16} = \frac{6}{16} = 0.375$$

$$\text{Gini(Bajo)} = 1 - \left[\left(\frac{3}{4}\right)^2 + \left(\frac{1}{4}\right)^2\right] = 1 - \frac{10}{16} = \frac{6}{16} = 0.375$$

**Paso 3 — Calcular el Gini ponderado:**

$$\text{Gini ponderado(Nivel\_Ingresos)} = \frac{4}{12} \times 0.500 + \frac{4}{12} \times 0.375 + \frac{4}{12} \times 0.375$$

$$= \frac{1}{3}(0.500 + 0.375 + 0.375) = \frac{1}{3}(1.250) = \boxed{0.417}$$

---

#### d) Decisión: ¿con qué variable dividir el nodo raíz? *(3 puntos)*

| Variable | Gini ponderado |
|----------|---------------|
| Edad | **0.250** ← menor |
| Nivel_Ingresos | 0.417 |

**Se divide por Edad**, porque produce el **menor Gini ponderado (0.250)**, lo que implica la mayor reducción de impureza respecto al nodo raíz (0.444 → 0.250).

> La lógica es: menor Gini ponderado = splits más "puros" = el árbol aprende mejor con esa variable. Notar que el nodo "Adulto" tiene Gini = 0 (puro), lo que hace que Edad sea especialmente buena para este dataset.

---

### Ejercicio 2 — Clasificador Naive Bayes

**Datos del dataset (16 clientes):**

**Conteo total:** 16 instancias → **Mora Sí: 8** (IDs 4,5,8,9,11,13,15,16) | **Mora No: 8** (IDs 1,2,3,6,7,10,12,14)

---

#### a) Probabilidades a priori y tabla de probabilidades condicionales *(9 puntos)*

**Probabilidades a priori:**

$$P(\text{Mora} = \text{Sí}) = \frac{8}{16} = 0.50 \qquad P(\text{Mora} = \text{No}) = \frac{8}{16} = 0.50$$

**Paso 1 — Identificar los clientes por clase:**

| Mora = Sí (8 clientes) | Historial | Nivel_Deuda |
|------------------------|-----------|-------------|
| ID 4 | Malo | Alto |
| ID 5 | Malo | Alto |
| ID 8 | Bueno | Bajo |
| ID 9 | Malo | Alto |
| ID 11 | Malo | Alto |
| ID 13 | Malo | Bajo |
| ID 15 | Malo | Alto |
| ID 16 | Bueno | Bajo |

| Mora = No (8 clientes) | Historial | Nivel_Deuda |
|------------------------|-----------|-------------|
| ID 1 | Bueno | Bajo |
| ID 2 | Bueno | Bajo |
| ID 3 | Bueno | Alto |
| ID 6 | Bueno | Bajo |
| ID 7 | Malo | Bajo |
| ID 10 | Bueno | Alto |
| ID 12 | Malo | Bajo |
| ID 14 | Bueno | Alto |

**Paso 2 — Tabla de probabilidades condicionales:**

**Variable: Historial_Crediticio**

| | Dado Mora = Sí | Dado Mora = No |
|---|---|---|
| **Bueno** | IDs 8,16 → 2/8 = **0.25** | IDs 1,2,3,6,10,14 → 6/8 = **0.75** |
| **Malo** | IDs 4,5,9,11,13,15 → 6/8 = **0.75** | IDs 7,12 → 2/8 = **0.25** |

**Variable: Nivel_Deuda**

| | Dado Mora = Sí | Dado Mora = No |
|---|---|---|
| **Alto** | IDs 4,5,9,11,15 → 5/8 = **0.625** | IDs 3,10,14 → 3/8 = **0.375** |
| **Bajo** | IDs 8,13,16 → 3/8 = **0.375** | IDs 1,2,6,7,12 → 5/8 = **0.625** |

---

#### b) Nuevo cliente: Historial = Malo, Nivel_Deuda = Alto *(8 puntos)*

**Fórmula Naive Bayes:**

$$\text{Score}(\text{Clase}) = P(\text{Clase}) \times P(\text{Historial} \mid \text{Clase}) \times P(\text{Deuda} \mid \text{Clase})$$

**Paso 1 — Calcular scores proporcionales:**

$$\text{Score(Sí)} = P(\text{Sí}) \times P(\text{Malo} \mid \text{Sí}) \times P(\text{Alto} \mid \text{Sí})$$
$$= 0.50 \times 0.75 \times 0.625 = \mathbf{0.234375}$$

$$\text{Score(No)} = P(\text{No}) \times P(\text{Malo} \mid \text{No}) \times P(\text{Alto} \mid \text{No})$$
$$= 0.50 \times 0.25 \times 0.375 = \mathbf{0.046875}$$

**Paso 2 — Normalizar (dividir por la suma total):**

$$\text{Total} = 0.234375 + 0.046875 = 0.28125$$

$$P(\text{Sí} \mid \text{Malo, Alto}) = \frac{0.234375}{0.28125} \approx \mathbf{83.3\%}$$

$$P(\text{No} \mid \text{Malo, Alto}) = \frac{0.046875}{0.28125} \approx \mathbf{16.7\%}$$

**Predicción: Mora = Sí** (83.3% > 50%)

> Tiene sentido intuitivo: historial malo + deuda alta es el perfil de mayor riesgo en el dataset.

---

#### c) Segundo cliente: Historial = Bueno, Nivel_Deuda = Alto *(5 puntos)*

**Paso 1 — Calcular scores proporcionales:**

$$\text{Score(Sí)} = P(\text{Sí}) \times P(\text{Bueno} \mid \text{Sí}) \times P(\text{Alto} \mid \text{Sí})$$
$$= 0.50 \times 0.25 \times 0.625 = \mathbf{0.078125}$$

$$\text{Score(No)} = P(\text{No}) \times P(\text{Bueno} \mid \text{No}) \times P(\text{Alto} \mid \text{No})$$
$$= 0.50 \times 0.75 \times 0.375 = \mathbf{0.140625}$$

**Paso 2 — Normalizar:**

$$\text{Total} = 0.078125 + 0.140625 = 0.21875$$

$$P(\text{Sí} \mid \text{Bueno, Alto}) = \frac{0.078125}{0.21875} \approx \mathbf{35.7\%}$$

$$P(\text{No} \mid \text{Bueno, Alto}) = \frac{0.140625}{0.21875} \approx \mathbf{64.3\%}$$

**Predicción: Mora = No** (64.3% > 50%)

> Aunque la deuda es alta, el buen historial crediticio pesa más. El modelo captura que el historial es el predictor más fuerte (P(Malo|Sí)=0.75 vs P(Bueno|Sí)=0.25).

---

### Ejercicio 3 — Matrices de Confusión y Costos

**Lectura de las matrices:**

**Modelo A:** VP=60, FP=50, FN=40, VN=350 → Total = 500

**Modelo B:** VP=80, FP=120, FN=20, VN=280 → Total = 500

**Estructura de costos:** VP=+$300 | FP=−$80 | FN=−$600 | VN=$0

---

#### a) Métricas para cada modelo *(8 puntos)*

**Fórmulas:**

$$\text{Accuracy} = \frac{VP + VN}{Total} \qquad \text{Recall} = \frac{VP}{VP + FN} \qquad \text{Precisión} = \frac{VP}{VP + FP}$$

**Modelo A:**

$$\text{Accuracy}_A = \frac{60 + 350}{500} = \frac{410}{500} = \mathbf{0.82}$$

$$\text{Recall}_A = \frac{60}{60 + 40} = \frac{60}{100} = \mathbf{0.60}$$

$$\text{Precisión}_A = \frac{60}{60 + 50} = \frac{60}{110} \approx \mathbf{0.545}$$

**Modelo B:**

$$\text{Accuracy}_B = \frac{80 + 280}{500} = \frac{360}{500} = \mathbf{0.72}$$

$$\text{Recall}_B = \frac{80}{80 + 20} = \frac{80}{100} = \mathbf{0.80}$$

$$\text{Precisión}_B = \frac{80}{80 + 120} = \frac{80}{200} = \mathbf{0.40}$$

**Resumen:**

| Modelo | Accuracy | Recall | Precisión |
|--------|----------|--------|-----------|
| A | **0.82** | 0.60 | 0.545 |
| B | 0.72 | **0.80** | 0.40 |

---

#### b) Resultado económico neto de cada modelo *(8 puntos)*

**Cálculo para Modelo A:**

| Tipo | Cantidad | Costo unitario | Subtotal |
|------|----------|---------------|---------|
| VP | 60 | +$300 | +$18,000 |
| FP | 50 | −$80 | −$4,000 |
| FN | 40 | −$600 | −$24,000 |
| VN | 350 | $0 | $0 |
| **Total** | | | **−$10,000** |

**Cálculo para Modelo B:**

| Tipo | Cantidad | Costo unitario | Subtotal |
|------|----------|---------------|---------|
| VP | 80 | +$300 | +$24,000 |
| FP | 120 | −$80 | −$9,600 |
| FN | 20 | −$600 | −$12,000 |
| VN | 280 | $0 | $0 |
| **Total** | | | **+$2,400** |

---

#### c) Recomendación *(4 puntos)*

**Recomendación: Modelo B**

**Justificación:**

| Criterio | Modelo A | Modelo B | Ganador |
|----------|----------|----------|---------|
| Accuracy | 0.82 | 0.72 | A |
| Recall | 0.60 | **0.80** | **B** |
| Resultado económico | **−$10,000** | **+$2,400** | **B** |

El Modelo A tiene mayor accuracy (82% vs 72%), pero **genera una pérdida neta de $10,000**. El Modelo B, con menor accuracy, genera una **ganancia de $2,400**.

La clave está en la estructura de costos: el **FN cuesta $600** (cliente de alto riesgo no detectado → siniestro sin prevención) mientras que el **FP solo cuesta $80** (monitoreo innecesario). El Modelo B tiene el doble de FP que el A (120 vs 50), pero tiene la mitad de FN (20 vs 40). Evitar esos 20 FN adicionales ahorra $12,000, que supera ampliamente el costo extra de los 70 FP adicionales ($5,600).

**Moraleja:** accuracy más alta no implica mayor valor económico. Cuando los errores tienen costos asimétricos (FN $600 >> FP $80), hay que priorizar recall y evaluar el impacto en pesos.

---

*Fin de las respuestas*
