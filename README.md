# Analítica de Datos — UdeSA

Materiales, notebooks y recursos de las **clases tutoriales** de **Analítica de Datos**, Negocios Digitales — Universidad de San Andrés. Otoño 2026.

Las tutoriales aplican la teoría de las magistrales (Pablo Sciolla) a **casos reales de negocio**: Topper, Naranja X, Netflix, People Analytics, AI startups. El foco no es aprender a programar, sino entender qué pregunta de negocio se contesta con cada técnica y cómo se interpretan los outputs.

---

## Contenido

| Clase | Tema | Caso de negocio | Dataset |
|---|---|---|---|
| **Clase 01** | Exploración, manipulación y visualización | AI Startups (Crunchbase / TechCrunch 2024-2025) | `startups.csv` |
| **Clase 02** | Data Profiling — pregunta, exploración, insight y storytelling | Superstore (proxy del TP de BA Datos Abiertos) | `Superstore.csv` |
| **Clase 03** | Tableau — dashboards y visualización interactiva | Superstore | `Superstore.csv` |
| **Clase 04** | Data Cleaning + Regresión Lineal | **Topper** (Alpargatas) — ROI de marketing digital | `campañas_marketing.csv` |
| **Clase 05** | Regresión Logística + KNN | **Naranja X** — aprobación de crédito personal | `solicitudes_naranjax.csv` |
| **Clase 06** | Métricas técnicas y económicas | **People Analytics** — evaluación de modelos pre-parcial | `candidatos_ofertas.csv` |
| **Clase 07** | CART (árboles de clasificación y regresión) | **Netflix** — churn + horas de visualización | `netflix_suscriptores.csv` |
| **Clase 08** | Random Forest (Bagging, GridSearchCV, feature importance) | **Mercado Pago** — detección de fraude transaccional | `transacciones_mercadopago.csv` |

---

## Material complementario sobre Claude

En la carpeta [`claude/`](claude/) está el PDF **"Claude para alumnos"** — una guía intermedia (15 páginas) que explica qué es Claude, qué es un agente, en qué se diferencia de ChatGPT/Gemini, cómo instalar y usar Claude Code, y cómo aprovecharlo para esta materia y para tu carrera.

Incluye dos roadmaps:

- **Roadmap A — 4 semanas:** orientado a usar Claude para resolver las prácticas de Analítica de Datos.
- **Roadmap B — 3-6 meses:** profundización en prompting, context engineering, tool use, MCP y agentes.

Este material va a discutirse a fondo en el **workshop de la última clase del cuatrimestre**.

---

## Estructura de cada clase

Cada carpeta contiene **sólo lo esencial**:

- `practicaNN.ipynb` — notebook del tutorial (en español, secciones numeradas, autocontenido).
- `<dataset>.csv` — datos del caso.
- `<PDF teórico>.pdf` — slides/teoría preparada por Juan que acompaña al notebook práctico, cuando aplica.

No hay `hallazgos.md` ni `documentacion_tecnica.md`: la investigación profunda del caso y la interpretación detallada de cada celda es trabajo del alumno (y entra al parcial).

---

## Cómo correr los notebooks

### Stack mínimo

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

### Opciones para ejecutar

- **Jupyter local**: `jupyter notebook` y abrir el `.ipynb` correspondiente.
- **VS Code** con la extensión de Jupyter.
- **Google Colab**: subí el notebook + el CSV de la clase y ejecutá.

Los notebooks están preparados para correrse de arriba abajo sin intervención.

---

## Programa de la materia

La materia tiene 4 módulos. Las tutoriales cubren el orden con el que Pablo presenta los temas en las magistrales:

- **Módulo 1** — EDA, estadística descriptiva, visualización, storytelling (Clases 01–03).
- **Módulo 2** — ML Supervisado: regresión lineal/logística, KNN, árboles, RF, GB, Naive Bayes. Evaluación técnica, económica y estratégica. **Parcial al cierre** (Clases 04–07 y siguientes).
- **Módulo 3** — ML No Supervisado: clustering, reducción de dimensionalidad.
- **Módulo 4** — Deep Learning. **Final al cierre.**

Evaluación: 20% quiz semanal + 20% conceptual + 30% Parcial 1 + 30% Parcial 2.

---

## Equipo docente

- **Pablo Sciolla** — Profesor titular (clases teóricas / magistrales).
- **Ignacio Aracena** y **Juan Costa** — Tutores (este repositorio).

**Analítica de Datos** · Negocios Digitales · Otoño 2026
Universidad de San Andrés
