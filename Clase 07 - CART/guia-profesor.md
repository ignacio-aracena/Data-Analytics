# Clase 08 — Random Forest · Guía del profesor

Material **no se distribuye a los alumnos**. Es una guía narrativa celda por celda que te permite explicar el notebook sin necesidad de prepararlo aparte.

**Duración objetivo:** 25-28 minutos para el notebook completo (+ 5 minutos de Kahoot al cierre).

---

## La historia que cuenta el notebook

**Pregunta de negocio inicial (celda 0):** *"¿qué transacciones detener antes de que se cierren para minimizar el fraude no detectado?"*. El alumno se la lleva durante toda la clase y la respondemos en la celda de conclusión.

El recorrido pedagógico arma una secuencia en tres tiempos:

1. **CART solo se queda corto.** Aplicamos el árbol único de la Clase 07 al problema de detectar fraude en Mercado Pago. Captura casi todos los fraudes (recall 0.87) pero marca demasiadas transacciones legítimas como sospechosas (precision 0.15). En producción tal cual, sería inviable.

2. **Random Forest con valores por defecto sorprende.** Esperamos que el bosque mejore al árbol, y en cierto sentido lo hace (separa mejor las clases). Pero usando el umbral de probabilidad 0.50 del default, el recall se cae a 0.33: nos quedan sin detectar dos de cada tres fraudes. Esta es la sorpresa pedagógica de la clase: el default de sklearn no es óptimo para todo problema.

3. **GridSearchCV + StratifiedKFold permiten tunear sin filtrar el test.** Probamos 12 combinaciones de hiperparámetros sobre el train (5 folds estratificados, scoring por recall) y elegimos la mejor. El bosque tuneado llega a recall 0.73 con precision 0.69 — un balance operativo aceptable.

**Conclusión (celda 24):** Risk lleva a producción el Random Forest tuneado. La diferencia entre los tres modelos no estuvo en el algoritmo sino en cómo elegimos los hiperparámetros. Anticipamos Clase 09: la familia de Boosting, que entrena los árboles en secuencia en lugar de en paralelo.

---

## Métricas clave (resumen para tener a mano)

| Modelo | Accuracy | Precision Fraude | Recall Fraude |
|---|---|---|---|
| CART (max_depth=3, balanced) | 0.851 | 0.152 | 0.867 |
| RF default (300 árboles, balanced_subsample) | 0.979 | 0.938 | 0.333 |
| RF tuneado (GridSearchCV scoring="recall") | 0.982 | 0.688 | 0.733 |

**Mejor combo del GridSearch:** `n_estimators=100`, `max_depth=10`, `min_samples_leaf=5`. Mejor recall en CV: **0.657**.

**Top 4 features (Gini):** `monto_vs_promedio_cliente` (0.29), `n_tx_ultimas_24h` (0.16), `hora_del_dia` (0.12), `antiguedad_cuenta_dias` (0.10).

**Primer corte del árbol CART:** `monto_vs_promedio_cliente <= 1.71`. La misma variable que será la #1 del RF — buena coherencia para mencionar en clase.

---

## Recorrido celda por celda

### Celda 0 — Header del caso (markdown)

**Qué dice:** plantea el escenario en tres bloques:

1. **Quiénes somos:** "Somos el equipo de Risk de Mercado Pago". Contexto del problema: 3% de fraude, costo asimétrico (no detectar fraude > frenar legítima).
2. **Pregunta de negocio:** *"¿qué transacciones detener antes de que se cierren para minimizar el fraude no detectado?"*
3. **Cómo lo vamos a resolver:** comparamos CART vs Random Forest y tuneamos con cross-validation.

**Qué decir en clase:**
- "Esto es la misma situación de Clase 06: con clases muy desbalanceadas, accuracy no es la métrica adecuada — tenemos que mirar precision, recall y entender qué error cuesta más".
- Anclar al caso del PPT: "el equipo de María Rosa en CAPS también prioriza recall por la misma razón — el costo de no anticipar pesa más que el costo del contacto innecesario".
- Recordar la pregunta antes de pasar al código: "tenemos que volver a esta pregunta al final".

### Celda 1 — Imports (código)

**Qué hace:** carga numpy, pandas, matplotlib, seaborn, los modelos (DecisionTreeClassifier, RandomForestClassifier), la utilidad de GridSearchCV + StratifiedKFold, y las métricas. Define dos colores (verde Mercado Pago, coral) que se van a reusar en los plots.

**Qué decir:** "Cargamos el stack estándar. Pasamos al dato". No detenerse acá.

---

### Sección 1 — Carga (celdas 2-4)

#### Celda 2 — Markdown "## 1. Carga"

Solo un título de sección.

#### Celda 3 — Leer CSV y mostrar primeras filas

**Qué hace:** lee `transacciones_mercadopago.csv` e imprime el shape `(5000, 12)` y las primeras 5 filas.

**Qué se ve:** 12 columnas: monto, hora_del_dia, dispositivo, antiguedad_cuenta_dias, ubicacion_nueva, n_tx_ultimas_24h, n_tx_ultimos_7d, intentos_pin_fallidos_24h, categoria_comercio, dia_de_la_semana, monto_vs_promedio_cliente y el target `es_fraude`.

**Qué decir:** "5000 transacciones, 12 columnas. La última es el target — fraude o legítima. Las otras son señales típicas de Risk: monto, horario, dispositivo, antigüedad del cliente, comportamiento reciente".

#### Celda 4 — df.info()

**Qué hace:** muestra los tipos de columna y confirma 0 nulos en las 5000 filas.

**Qué decir:** "Sin nulos, no toca imputar. La limpieza ya pasó en clases previas. Hoy el foco es modelado".

---

### Sección 2 — EDA (celdas 5-7)

#### Celda 5 — Markdown "## 2. EDA"

Título.

#### Celda 6 — Balance del target (plot de barras)

**Qué hace:** muestra el porcentaje de legítimas vs fraude.

**Qué se ve:** 97% legítimas (verde), 3% fraude (coral).

**Qué decir:**
- "3% es fraude. Si predecimos siempre 'legítima', acertamos 97% y no sirve para nada".
- "Es exactamente la lógica del PPT teórico — accuracy no es la métrica cuando hay desbalance".
- **Pregunta para el grupo:** "¿qué tiene que hacer un modelo útil acá?".

#### Celda 7 — Tasa de fraude por categoría de comercio (barplot horizontal)

**Qué hace:** agrupa por categoría de comercio y calcula la tasa de fraude.

**Qué se ve:** `transferencia_p2p`, `supermercado` y `cripto` por encima del promedio del 3%. `gastronomia`, `vestimenta` por debajo.

**Qué decir:** "Algunas categorías concentran más fraude. Esto le sirve a Risk para reglas heurísticas — y también al modelo, que va a usar la categoría como feature de partición".

---

### Sección 3 — Preparación (celdas 8-9)

#### Celda 8 — Markdown "## 3. Preparación"

Anuncia one-hot encoding de las tres categóricas y split estratificado 70/30.

#### Celda 9 — One-hot + split estratificado

**Qué hace:** `pd.get_dummies(drop_first=True)` expande las 3 categóricas a binarias. La booleana `ubicacion_nueva` la pasa a int. Después hace train/test split 70/30 con `stratify=y` y `random_state=42`.

**Qué se ve:** Train 3500 filas, Test 1500. % fraude en ambos: 3.00%.

**Qué decir:**
- "CART y RF no necesitan escalado — a diferencia de KNN de Clase 05, que sí lo pedía. Los árboles parten por umbrales, no por distancias".
- "Estratificar es crítico con 3% de positivos. Sin esto, el test podía quedar con 1% o 5% por azar".

---

### Sección 4 — CART como baseline (celdas 10-12)

#### Celda 10 — Markdown "## 4. CART (baseline)"

Título.

#### Celda 11 — Entrenar CART e imprimir métricas

**Qué hace:** entrena un árbol con `max_depth=3`, `min_samples_leaf=20`, `class_weight="balanced"`, `random_state=42`. Predice sobre test y muestra el classification_report.

**Qué se ve:**
- Recall fraude: **0.87** → captura 39 de los 45 fraudes reales del test.
- Precision fraude: **0.15** → de 100 transacciones marcadas como fraude, solo 15 lo son realmente.
- F1 fraude: 0.26. Accuracy: 0.85.

**Qué decir:**
- "Recall alto: agarra casi todos los fraudes. Buena noticia para Risk".
- "Pero precision 0.15: de cada 100 transacciones que el modelo frena, 85 eran clientes legítimos. Inaceptable operativamente".
- "CART está siendo demasiado inclusivo. Tiene una sola partición global por nivel — para capturar fraude tiene que hacer cortes amplios que también caen sobre legítimas con perfil parecido".

#### Celda 12 — plot_tree

**Qué hace:** dibuja el árbol completo (max_depth=3, 8 hojas).

**Qué se ve:** el primer corte está en `monto_vs_promedio_cliente <= 1.71`. Las hojas naranjas son las que clasifican como fraude.

**Qué decir:**
- "Primer corte: el ratio del monto contra el promedio histórico del cliente. Tiene sentido para Risk — una transacción 2x sobre el promedio del cliente es alerta inmediata".
- "Esta misma variable va a aparecer #1 en feature importance del RF más adelante. Coincidencia útil para mencionar — el árbol y el bosque están de acuerdo en cuál es la señal más fuerte".
- Recorrer 1-2 hojas en voz alta: "si el ratio es alto Y hay muchas tx en 24h Y la cuenta es nueva → fraude probable".

---

### Sección 5 — Random Forest (celdas 13-15)

**Acá está el corazón pedagógico de la clase.**

#### Celda 13 — Markdown "## 5. Random Forest"

Recuerda la definición: RF = Bagging (Bootstrap Aggregating), con muestras bootstrap + selección aleatoria de features en cada split.

**Qué decir antes del output:**
- "Recordamos del PPT: Random Forest = Bootstrapping + selección aleatoria de variables = Bagging".
- "5 pasos: muestra bootstrap → entrenar árbol → en cada división, subset aleatorio de features → repetir 300 veces → voto mayoritario".
- "El subset de features lo controla `max_features='sqrt'` (default de sklearn). Con 23 features post-encoding, cada split ve √23 ≈ 5 features candidatas".

#### Celda 14 — Entrenar RF default e imprimir métricas

**Qué hace:** entrena un `RandomForestClassifier` con `n_estimators=300`, `class_weight="balanced_subsample"`, `random_state=42`. Predice sobre test.

**Qué se ve (la sorpresa):**
- Recall fraude: **0.33** ← cayó respecto a CART (que era 0.87).
- Precision fraude: **0.94** ← subió a casi perfecta.
- Accuracy: 0.98.

**Qué decir — la conversación clave de la clase:**
- "Sorpresa: el RF separa mejor las clases por probabilidad, pero el recall se cae a 33%. ¿Por qué?".
- Explicación: "el RF promedia 300 árboles → las probabilidades se suavizan. El umbral default de 0.50 exige consenso mayoritario para marcar fraude. Solo se marca fraude cuando la mayoría de los árboles coincide. Resultado: precision casi perfecta pero recall inaceptable".
- "En producción tal cual: se escapan 2 de cada 3 fraudes. Inaceptable para Risk".
- **Pregunta para el grupo:** "¿qué hacemos? ¿más árboles? ¿menos? ¿otra cosa?". La respuesta viene en la siguiente sección: tunear.

#### Celda 15 — Markdown anticipatorio

**Qué dice:** "Recall del fraude más bajo que CART. El default no es óptimo — lo corregimos tuneando hiperparámetros en la próxima sección".

**Qué decir:** "El default de sklearn es razonable pero no óptimo para todo problema. Ahora vamos a buscar la mejor combinación de hiperparámetros de forma sistemática".

---

### Sección 6 — GridSearchCV + StratifiedKFold (celdas 16-18)

#### Celda 16 — Markdown "## 6. GridSearchCV + StratifiedKFold"

Título.

#### Celda 17 — Definir grilla, CV y correr GridSearch

**Qué hace:**
- Define la grilla: `n_estimators ∈ {100, 300}`, `max_depth ∈ {None, 10, 20}`, `min_samples_leaf ∈ {1, 5}`. Total: 12 combinaciones.
- Define `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
- `GridSearchCV` con `scoring="recall"` — porque priorizamos detectar fraude.
- Corre el fit (entrena 12 × 5 = 60 modelos).

**Qué se ve:**
- Mejores hiperparámetros: `{'max_depth': 10, 'min_samples_leaf': 5, 'n_estimators': 100}`.
- Mejor recall en CV: **0.657**.

**Qué decir:**
- "El test es sagrado: lo tocamos UNA sola vez al final. Si probamos 12 combinaciones sobre el test, ya filtramos información — el número final ya no es honesto".
- "La solución estándar: cross-validation sobre el train. Partimos el train en 5 folds estratificados (mantienen el 3% de fraude en cada fold), probamos cada combinación en cada fold, promediamos. La mejor gana".
- "Scoring `recall` porque el caso lo pide: priorizamos detectar fraude, alineado con el 'PROBLEMA DE ALTO RECALL' del PPT teórico".

#### Celda 18 — Evaluar best estimator en test

**Qué hace:** toma el mejor modelo (`grid.best_estimator_`) y lo evalúa sobre el test set.

**Qué se ve:**
- Recall fraude: **0.73**
- Precision fraude: **0.69**
- Accuracy: 0.98.

**Qué decir:**
- "Recall 73%: detectamos 3 de cada 4 fraudes. Mejor que el default que detectaba 1 de cada 3".
- "Precision 69%: de 100 transacciones que frenamos, 69 son fraude real. Mucho mejor que el 15% de CART".
- "Recall CV 0.657 vs recall test 0.733: el modelo generaliza bien, no estaba sobreajustado a la CV. Si fueran muy distintos, sospechamos sobreajuste o azar".

---

### Sección 7 — Importancia de variables (celdas 19-20)

#### Celda 19 — Markdown "## 7. Importancia de variables"

Título.

#### Celda 20 — Plot horizontal de feature_importances_

**Qué hace:** ordena las features por su importancia Gini y muestra las top 10 en barplot horizontal.

**Qué se ve (top 4):**
1. `monto_vs_promedio_cliente` — 0.29
2. `n_tx_ultimas_24h` — 0.16
3. `hora_del_dia` — 0.12
4. `antiguedad_cuenta_dias` — 0.10

**Qué decir:**
- "La importancia Gini mide cuánto reduce cada variable la impureza acumulada en todos los splits del bosque. Es lo que el PPT teórico llama 'importancia de variables'".
- "La señal más fuerte es el ratio del monto contra el promedio del cliente. Operativamente: una transacción 3x sobre el promedio histórico del cliente es la primera alerta".
- "Después: cantidad de transacciones en las últimas 24h (señala bursting de actividad sospechosa), hora del día (la madrugada concentra más fraude) y antigüedad de la cuenta (cuentas nuevas son más riesgosas)".
- Conectar con el árbol de CART: "la #1 es la misma variable que el árbol usó como primer corte (`monto_vs_promedio_cliente <= 1.71`). Modelo y árbol coinciden".

---

### Sección 8 — Comparación final (celdas 21-23)

#### Celda 21 — Markdown "## 8. Comparación final"

Título.

#### Celda 22 — Tabla comparativa

**Qué hace:** define una función `metricas` que devuelve un dict con accuracy, precision (fraude) y recall (fraude). Construye una tabla con los tres modelos.

**Qué se ve:**

|  | Accuracy | Precision (Fraude) | Recall (Fraude) |
|---|---|---|---|
| CART | 0.851 | 0.152 | 0.867 |
| RF default | 0.979 | 0.938 | 0.333 |
| RF tuneado | 0.982 | 0.688 | 0.733 |

**Qué decir:**
- "CART tiene alto recall (0.87) pero precision pésima (0.15) — agarra muchos, pero la mayoría son falsas alarmas".
- "RF default invierte: precision alta (0.94) pero recall bajo (0.33) — flaggea poco y le escapa la mayoría".
- "RF tuneado equilibra: ni el extremo de CART ni el extremo del default. Es el modelo que llevaría Risk a producción".

#### Celda 23 — Matrices de confusión lado a lado

**Qué hace:** dibuja las tres matrices de confusión (CART, RF default, RF tuneado) en una fila.

**Qué se ve:**
- CART: muchos falsos positivos (~217 transacciones legítimas marcadas como fraude).
- RF default: muchos falsos negativos (~30 fraudes no detectados).
- RF tuneado: balance entre ambos.

**Qué decir:** "Visualmente: el cuadrante arriba-derecha (legítimas marcadas como fraude) baja drásticamente al pasar de CART a RF tuneado. El cuadrante abajo-izquierda (fraudes que se escapan) también es razonable en el tuneado".

---

### Sección 9 — Conclusión (celda 24)

**Qué dice:** vuelve sobre la pregunta de negocio inicial. Recomienda llevar a producción el **Random Forest tuneado** (recall 0.73, precision 0.69). Reconoce los dos extremos (CART demasiado inclusivo, RF default demasiado conservador) y cierra con el aprendizaje clave: la diferencia entre modelos no estuvo en el algoritmo sino en cómo elegimos los hiperparámetros con cross-validation. Anticipa Clase 09 (Boosting: árboles entrenados en secuencia).

**Qué decir:**
- "Cerramos volviendo a la pregunta que nos hicimos al principio. Risk lleva el Random Forest tuneado a producción".
- "Lo que vimos hoy: Bagging (RF). Lo que viene: Boosting (AdaBoost, XGBoost)".
- "La diferencia conceptual: RF es paralelo (cada árbol vota independiente), Boosting es secuencial (cada árbol aprende de los errores del anterior)".
- "Esto suele dar otro salto de performance en datos tabulares — y es la familia que gana la mayoría de competencias de Kaggle".

---

## Trampas pedagógicas a anticipar

1. **"¿Por qué RF default rinde peor que CART en recall?"** — el RF separa mejor las clases pero el umbral 0.50 default exige consenso mayoritario de los 300 árboles. CART con `class_weight="balanced"` y depth=3 cae rápido del lado del fraude.

2. **"¿Para qué necesito GridSearchCV?"** — para no filtrar información del test. CV usa el train particionado en folds; el test queda intacto hasta la evaluación final.

3. **"¿Por qué `n_estimators=100` ganó sobre 300?"** — más árboles no siempre es mejor. Con la grilla y datos actuales, 100 árboles ya capturan la señal. Más estabilidad estadística sin sobre-complejidad.

4. **"`max_features='sqrt'` ¿de dónde sale?"** — heurística clásica para clasificación. Para regresión sklearn usa `p/3` en RF. La raíz fuerza diversidad entre árboles.

5. **"¿Por qué un Random Forest hereda la robustez a outliers de CART?"** — porque cada árbol del bosque también corta por umbral, no por distancia. Un valor extremo cae del mismo lado del corte que cualquier valor "grande", y el voto agregado no se mueve por uno o dos casos atípicos.

---

## Cómo validar antes de la clase

```bash
cd "Clase 08 - Random Forest"
/Users/ignacioaracena/Library/Python/3.9/bin/jupyter-nbconvert --to notebook --execute practica08.ipynb --output practica08.ipynb
```

Confirmar 0 errores y 0 warnings. Si los números no coinciden con los de esta guía, **algún hiperparámetro o seed cambió** — revisar antes de presentar.

Para validación pedagógica completa (5 capas + alineación con el PPT teórico), usar el subagent global `profesor-validador` en `.claude/agents/`.

---

## Kahoot al cierre

10 preguntas conceptuales ancladas en el PPT (`kahoot.md` en esta misma carpeta). **Preguntas clave de control de comprensión:**

- **P5** (83% vs 79%): chequea que el alumno entendió el ejemplo numérico del PPT.
- **P7** (María Rosa al 79%): chequea que entendió la intervención del caso CAPS.
- **P9** (variable más importante en CAPS): vuelta de rosca — el alumno espera "ausencias previas" pero la respuesta es "días de espera".
- **P10** (alto recall): chequea que entendió por qué priorizamos recall en este tipo de problemas.

---

## Tarea para casa

Construir un `RandomForestRegressor` que prediga el `monto` desde el resto de features (sacando `es_fraude`). Comparar MAE/RMSE/R² contra una regresión lineal baseline. El código es análogo al de hoy, cambiando el scoring del GridSearch a `"neg_root_mean_squared_error"`.

Pista de negocio: estimar el monto esperado de una transacción sospechosa sirve para priorizar qué casos revisa primero el equipo de Risk.
