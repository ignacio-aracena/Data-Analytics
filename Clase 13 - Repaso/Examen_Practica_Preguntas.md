# EXAMEN DE PRÁCTICA — ANALÍTICA DE DATOS

**Puntaje total:** 100 puntos | **Mínimo para aprobar:** 60 puntos
**Parte 1:** 36 puntos | **Parte 2:** 64 puntos

> **Nota para el estudiante:** Esta práctica incluye 18 preguntas de opción múltiple como banco de ejercitación. El examen real contará con entre 10 y 15 preguntas de esta selección.

---

## PARTE 1: MÚLTIPLE CHOICE (36 puntos — 18 preguntas × 2 puntos)

**Instrucciones:** Cada pregunta vale 2 puntos. Puede haber **una o más** respuestas correctas (se indica en cada pregunta). Marcar una opción incorrecta descuenta **1 punto**. Dejar en blanco = 0 puntos.

---

**Pregunta 1** *(Múltiples respuestas)* — Normalización y escalado de variables

¿Cuál(es) de las siguientes afirmaciones es/son **correcta(s)**?

- A) La normalización Min-Max escala los valores al rango [0, 1]
- B) La estandarización Z-score es necesaria antes de aplicar un árbol de decisión para mejorar su rendimiento
- C) La estandarización Z-score produce una distribución con media 0 y desviación estándar 1
- D) Los parámetros de normalización (media, mín, máx) deben calcularse **solo** sobre el conjunto de entrenamiento y luego aplicarse al de prueba

---

**Pregunta 2** *(Múltiples respuestas)* — Tratamiento de valores faltantes

¿Cuál(es) de las siguientes es/son estrategias **válidas** para tratar valores faltantes?

- A) Eliminar las filas que contengan al menos un valor faltante
- B) Imputar con el valor máximo de la variable para no perder información
- C) Imputar con la media o mediana (para variables numéricas)
- D) Crear una categoría adicional "Sin Dato" para variables categóricas

---

**Pregunta 3** *(Respuesta única)* — Cálculo de métricas

Un modelo de clasificación para detección de enfermedades arroja los siguientes resultados sobre 200 pacientes:

**VP = 70 | FP = 30 | FN = 10 | VN = 90**

¿Cuál es el valor del **Recall (Sensibilidad)** del modelo?

- A) 0.70
- B) 0.80
- C) 0.875
- D) 0.78

---

**Pregunta 4** *(Respuesta única)* — Selección de métrica según contexto

Una empresa farmacéutica desarrolla un modelo para detectar efectos secundarios graves en pacientes. El costo de **no detectar** un efecto secundario es extremadamente alto. ¿Qué métrica debería priorizarse al evaluar el modelo?

- A) Exactitud (Accuracy)
- B) Precisión (Precision)
- C) Recall (Sensibilidad)
- D) Especificidad

---

**Pregunta 5** *(Múltiples respuestas)* — Overfitting

¿Cuál(es) de las siguientes técnicas ayuda(n) a **reducir el overfitting**?

- A) Aumentar la profundidad máxima del árbol de decisión
- B) Aplicar poda (pruning) al árbol de decisión
- C) Usar validación cruzada (k-fold cross-validation)
- D) Agregar más variables al modelo sin criterio de selección previa

---

**Pregunta 6** *(Múltiples respuestas)* — Método del codo

Respecto al **método del codo (Elbow Method)** en K-Means, ¿cuál(es) de las siguientes afirmaciones es/son correcta(s)?

- A) Se utiliza para seleccionar el número óptimo de clusters K
- B) Evalúa la inercia (suma de distancias cuadradas intra-cluster) para diferentes valores de K
- C) Garantiza siempre encontrar el número óptimo de clusters en cualquier dataset
- D) El punto "codo" indica el K a partir del cual agregar más clusters no reduce significativamente la inercia

---

**Pregunta 7** *(Múltiples respuestas)* — Clustering aglomerativo

¿Cuál(es) es/son características del **clustering jerárquico aglomerativo**?

- A) Comienza con cada observación en su propio cluster y los va fusionando de a pares
- B) Requiere definir el número de clusters K antes de construir el dendrograma
- C) El dendrograma permite visualizar las jerarquías de fusión entre clusters
- D) Es generalmente más costoso computacionalmente que K-Means para datasets de gran escala

---

**Pregunta 8** *(Múltiples respuestas)* — Caso de negocio: clases desbalanceadas

Un modelo de detección de fraude fue entrenado con datos donde el **98% son transacciones legítimas** y el **2% son fraudulentas**. Si el modelo predice **siempre "legítima"**, ¿cuál(es) de las siguientes afirmaciones es/son verdadera(s)?

- A) La exactitud (Accuracy) del modelo es del 98%
- B) El Recall para la clase "fraude" es del 0%
- C) Este modelo es útil para la empresa en términos prácticos
- D) La Precisión para la clase "fraude" es indefinida o 0%

---

**Pregunta 9** *(Múltiples respuestas)* — Índice de Gini

Respecto al **índice de Gini** en árboles de decisión, ¿cuál(es) es/son correcta(s)?

- A) Un nodo con Gini = 0 indica que todas las instancias pertenecen a la misma clase (nodo puro)
- B) Se elige la variable que produce el **menor** Gini ponderado al dividir el nodo
- C) El valor máximo del Gini para una clasificación binaria es 1
- D) Conceptualmente, el Gini mide la probabilidad de clasificar incorrectamente una instancia elegida al azar

---

**Pregunta 10** *(Múltiples respuestas)* — Naive Bayes

¿Cuál(es) de las siguientes es/son características del clasificador **Naive Bayes**?

- A) Asume independencia condicional entre las variables predictoras dada la clase
- B) Requiere grandes volúmenes de datos para funcionar correctamente
- C) Puede usarse para problemas de clasificación multiclase
- D) Es sensible a la escala de las variables numéricas

---

**Pregunta 11** *(Múltiples respuestas)* — Random Forest

¿Cuál(es) de las siguientes afirmaciones sobre **Random Forest** es/son correcta(s)?

- A) Es un conjunto (ensemble) de múltiples árboles de decisión entrenados de forma independiente
- B) Cada árbol se entrena con exactamente los mismos datos del conjunto de entrenamiento
- C) Reduce el overfitting en comparación con un único árbol de decisión sin restricciones
- D) Permite estimar la importancia de cada variable predictora en el modelo

---

**Pregunta 12** *(Respuesta única)* — Cálculo de F1-Score

Un modelo de clasificación binaria arroja los siguientes resultados sobre 200 instancias:

**VP = 60 | FP = 40 | FN = 20 | VN = 80**

¿Cuál es el **F1-Score** del modelo?

- A) 0.60
- B) 0.75
- C) 0.667
- D) 0.68

---

**Pregunta 13** *(Respuesta única)* — Caso de negocio: selección de métrica con restricción

Una plataforma de streaming quiere predecir qué usuarios cancelarán su suscripción el próximo mes. El equipo de retención tiene presupuesto para contactar como máximo a **200 clientes** con una oferta especial y quiere que esos contactos sean lo más efectivos posible (es decir, que la mayoría de los contactados realmente fueran a cancelar). ¿Qué métrica es más relevante para seleccionar el modelo?

- A) Recall, para maximizar la cantidad de churners detectados
- B) Accuracy general del modelo
- C) Precisión (Precision), para asegurar que los contactos estén bien dirigidos
- D) Especificidad (True Negative Rate)

---

**Pregunta 14** *(Múltiples respuestas)* — Codificación de variables categóricas

Una variable categórica **nominal** llamada "Región" tiene 5 valores posibles: Norte, Sur, Este, Oeste, Centro. ¿Cuál(es) de las siguientes afirmaciones es/son correcta(s)?

- A) Aplicar Label Encoding (0, 1, 2, 3, 4) puede introducir relaciones de orden artificiales entre las categorías
- B) One-Hot Encoding generará 5 nuevas columnas binarias para representar esta variable
- C) One-Hot Encoding es la única técnica válida para variables categóricas nominales
- D) Cuando la variable tiene muchas categorías, One-Hot Encoding puede generar alta dimensionalidad en el dataset

---

**Pregunta 15** *(Múltiples respuestas)* — Data leakage

¿Cuál(es) de las siguientes situaciones representa(n) un caso de **data leakage** (fuga de datos)?

- A) Calcular los parámetros de normalización usando todo el dataset (incluyendo el conjunto de prueba) antes de dividirlo
- B) Incluir en el modelo una variable que, en producción, solo estará disponible *después* de que ocurra el evento que se quiere predecir
- C) Dividir el dataset en train/test *antes* de aplicar cualquier transformación
- D) Entrenar con datos históricos y evaluar el modelo con datos de un período posterior

---

**Pregunta 16** *(Múltiples respuestas)* — Curva ROC y AUC

Respecto a la **curva ROC** y el área bajo la curva (**AUC-ROC**), ¿cuál(es) de las siguientes afirmaciones es/son correcta(s)?

- A) Un modelo con AUC = 0.5 tiene un desempeño equivalente al de un clasificador aleatorio
- B) La curva ROC representa el trade-off entre la tasa de verdaderos positivos (Recall) y la tasa de falsos positivos (FPR)
- C) Un AUC más alto garantiza siempre un mejor desempeño práctico, independientemente del umbral de decisión elegido
- D) Un AUC = 1 corresponde a un clasificador perfecto que separa completamente las dos clases

---

**Pregunta 17** *(Múltiples respuestas)* — Árbol de decisión: profundidad y generalización

Un árbol de decisión se entrena **sin ninguna restricción de profundidad** sobre el conjunto de entrenamiento. ¿Cuál(es) de las siguientes afirmaciones es/son correcta(s)?

- A) Tenderá a memorizar los datos de entrenamiento (overfitting)
- B) Su accuracy sobre el conjunto de entrenamiento será generalmente mayor que la de un árbol con profundidad limitada
- C) Su accuracy sobre el conjunto de prueba siempre será mayor que la de un árbol podado
- D) Limitar la profundidad máxima del árbol es una técnica de regularización que puede mejorar la generalización

---

**Pregunta 18** *(Múltiples respuestas)* — K-Means: características y limitaciones

¿Cuál(es) de las siguientes es/son **limitaciones o características del algoritmo K-Means** que el analista debe considerar?

- A) Los resultados pueden variar según la inicialización aleatoria de los centroides
- B) Requiere que el número de clusters K sea especificado antes de ejecutar el algoritmo
- C) Es robusto frente a la presencia de outliers en los datos
- D) Asume implícitamente que los clusters tienen forma aproximadamente esférica y tamaño similar

---
---

## PARTE 2: EJERCICIOS PRÁCTICOS (64 puntos)

**Instrucciones:** Resuelva en papel con calculadora. Muestre **todos los pasos intermedios**. Las respuestas sin desarrollo no serán calificadas.

---

### Ejercicio 1 — Árbol de Decisión: Índice de Gini (22 puntos)

Una empresa de retail desea predecir si un cliente realizará una compra online (Compra = Sí / No). Se dispone del siguiente dataset de entrenamiento con 12 clientes:

| ID | Edad    | Nivel_Ingresos | Compra |
|----|---------|----------------|--------|
| 1  | Joven   | Alto           | No     |
| 2  | Joven   | Alto           | No     |
| 3  | Adulto  | Alto           | Sí     |
| 4  | Senior  | Medio          | Sí     |
| 5  | Senior  | Bajo           | Sí     |
| 6  | Senior  | Bajo           | No     |
| 7  | Adulto  | Bajo           | Sí     |
| 8  | Joven   | Medio          | No     |
| 9  | Joven   | Bajo           | Sí     |
| 10 | Senior  | Medio          | Sí     |
| 11 | Adulto  | Medio          | Sí     |
| 12 | Adulto  | Alto           | Sí     |

**a)** Calcule el índice de Gini del **nodo raíz**. *(4 puntos)*

**b)** Calcule el índice de Gini para cada categoría de la variable **Edad** (Joven, Adulto, Senior) y luego obtenga el **Gini ponderado** de esa variable. *(9 puntos)*

**c)** Calcule el índice de Gini para cada categoría de la variable **Nivel_Ingresos** (Alto, Medio, Bajo) y luego obtenga el **Gini ponderado** de esa variable. *(6 puntos)*

**d)** ¿Con qué variable dividiría el nodo raíz? Justifique su respuesta con los valores calculados. *(3 puntos)*

---

### Ejercicio 2 — Clasificador Naive Bayes (22 puntos)

Un banco desea predecir si un cliente incurrirá en **mora** (impago) a partir de dos variables: su historial crediticio y su nivel de deuda. Se dispone del siguiente dataset con 16 clientes:

| ID | Historial_Crediticio | Nivel_Deuda | Mora |
|----|---------------------|-------------|------|
| 1  | Bueno               | Bajo        | No   |
| 2  | Bueno               | Bajo        | No   |
| 3  | Bueno               | Alto        | No   |
| 4  | Malo                | Alto        | Sí   |
| 5  | Malo                | Alto        | Sí   |
| 6  | Bueno               | Bajo        | No   |
| 7  | Malo                | Bajo        | No   |
| 8  | Bueno               | Bajo        | Sí   |
| 9  | Malo                | Alto        | Sí   |
| 10 | Bueno               | Alto        | No   |
| 11 | Malo                | Alto        | Sí   |
| 12 | Malo                | Bajo        | No   |
| 13 | Malo                | Bajo        | Sí   |
| 14 | Bueno               | Alto        | No   |
| 15 | Malo                | Alto        | Sí   |
| 16 | Bueno               | Bajo        | Sí   |

**a)** Calcule las probabilidades a priori P(Mora = Sí) y P(Mora = No). Luego construya la tabla completa de **probabilidades condicionales** para cada valor de cada variable. *(9 puntos)*

**b)** Un nuevo cliente tiene **Historial = Malo** y **Nivel_Deuda = Alto**. Calcule las probabilidades proporcionales para cada clase, normalícelas y determine la predicción del modelo. *(8 puntos)*

**c)** Un segundo cliente tiene **Historial = Bueno** y **Nivel_Deuda = Alto**. ¿Cuál es la predicción? Muestre el cálculo completo. *(5 puntos)*

---

### Ejercicio 3 — Caso de Negocio: Matrices de Confusión y Costos (20 puntos)

Una compañía de seguros desarrolló dos modelos para identificar clientes con **alto riesgo de siniestro**. Ambos modelos fueron evaluados sobre un conjunto de prueba de **500 clientes**:

**Modelo A**

|                        | Predicho: Alto Riesgo | Predicho: Bajo Riesgo |
|------------------------|:---------------------:|:---------------------:|
| **Real: Alto Riesgo**  |          60           |          40           |
| **Real: Bajo Riesgo**  |          50           |         350           |

**Modelo B**

|                        | Predicho: Alto Riesgo | Predicho: Bajo Riesgo |
|------------------------|:---------------------:|:---------------------:|
| **Real: Alto Riesgo**  |          80           |          20           |
| **Real: Bajo Riesgo**  |         120           |         280           |

**Estructura de costos y beneficios (por cliente):**

| Caso                    | Descripción                                                              | Impacto      |
|-------------------------|--------------------------------------------------------------------------|:------------:|
| Verdadero Positivo (VP) | Cliente de alto riesgo detectado → medidas preventivas exitosas          | **+$300**    |
| Falso Positivo (FP)     | Cliente de bajo riesgo monitoreado innecesariamente                      | **−$80**     |
| Falso Negativo (FN)     | Cliente de alto riesgo no detectado → siniestro ocurre sin prevención    | **−$600**    |
| Verdadero Negativo (VN) | Cliente de bajo riesgo clasificado correctamente                         | **$0**       |

**a)** Para cada modelo calcule: **Exactitud (Accuracy)**, **Recall** y **Precisión**. Muestre las fórmulas utilizadas. *(8 puntos)*

**b)** Calcule el **resultado económico neto** (costo/beneficio total) de cada modelo sobre el conjunto de prueba. *(8 puntos)*

**c)** ¿Qué modelo recomendaría implementar? Justifique considerando tanto las métricas de clasificación como el análisis económico. *(4 puntos)*

---

*Fin del examen*
