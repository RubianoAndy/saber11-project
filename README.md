<div align="center">
    <img src="assets/images/Logo.png" width="250" alt="Logo Universidad de La Salle">
</div>

# Predicción del puntaje global de la prueba Saber 11 a partir de variables socioeconómicas y del colegio

## 📋 Información General

<div align="center">
    <img src="assets/images/author/Andy Rubiano.png" width="200" alt="Foto de Andrés Giovanny Rubiano Muñoz" style="border-radius: 10px;">
</div>

| Aspecto | Detalles |
|--------|----------|
| **Autor** | Andrés Giovanny Rubiano Muñoz "Andy Rubiano" |
| **Correo** | arubiano67@unisalle.edu.co |
| **Asignatura** | Ciencia de Datos |
| **Actividad** | Proyecto Integrador de Ciencia de Datos e Inteligencia Artificial · Fases 1 a 4 |
| **Programa** | Maestría en Inteligencia Artificial |
| **Universidad** | Universidad de La Salle |
| **Líneas de Trabajo** | Análisis Exploratorio de Datos, Aprendizaje Supervisado y No Supervisado, Interpretabilidad, Despliegue |
| **Año** | 2026 |
| **Estado** | Cuadernos de las fases 1 a 3 completados · Tablero desplegado · Sustentación pendiente |
| **Tablero** | [saber11-dashboard.streamlit.app](https://saber11-dashboard.streamlit.app/) · código en [RubianoAndy/saber11-dashboard](https://github.com/RubianoAndy/saber11-dashboard) |

---

## 🎯 Descripción del Proyecto

La prueba Saber 11 es el examen de Estado que presentan en Colombia los estudiantes que terminan la educación media. Su puntaje global, en una escala de 0 a 500, decide en buena medida el acceso a la educación superior, a becas y a los cupos de las universidades públicas. El ICFES publica, por cada aplicación, un registro anónimo por estudiante con el resultado de la prueba y un cuestionario sociodemográfico sobre su hogar y su colegio.

Este proyecto recorre el ciclo completo de un problema de ciencia de datos sobre esos registros, desde la formulación hasta el despliegue de un tablero, con tres frentes de modelado:

- **Regresión** del puntaje global.
- **Clasificación** del nivel de desempeño (Bajo, Medio, Alto: terciles del puntaje).
- **Segmentación** no supervisada de los estudiantes por su perfil de resultados.

> ¿En qué medida las características socioeconómicas del hogar, las características del colegio y las características demográficas del estudiante permiten predecir el puntaje global de la prueba Saber 11, y cuáles de esas características tienen mayor peso?

El trabajo se organiza en cuatro fases:

- **Fase 1 · Problema y exploración de datos** — planteamiento, descripción detallada de las 51 variables, calidad de los datos y análisis exploratorio. ✅ `01_planteamiento_y_eda.ipynb`
- **Fase 2 · Preparación y modelo base** — mecanismo de los faltantes, atípicos, variables derivadas, codificación y escalado sin fuga, partición estratificada y modelos de referencia. ✅ `02_preparacion_y_baseline.ipynb`
- **Fase 3 · Modelado y evaluación** — regresión regularizada y ensambles, clasificadores, perceptrón multicapa en PyTorch, segmentación con K-means y jerárquico, hiperparámetros por validación cruzada e interpretabilidad. ✅ `03_modelos_y_evaluacion.ipynb`
- **Fase 4 · Tablero y comunicación** — tablero interactivo desplegado en Streamlit Community Cloud. ✅ [saber11-dashboard](https://saber11-dashboard.streamlit.app/) · informe y sustentación pendientes

Una restricción metodológica atraviesa todo el proyecto: el puntaje global es un **promedio ponderado de los puntajes por área**, de modo que esos puntajes no pueden usarse como variables explicativas sin incurrir en una fuga de información (*data leakage*). Solo se emplean en la segmentación, donde son la materia de estudio y no un predictor.

### Objetivos Principales

- Describir el conjunto de datos *Resultados únicos Saber 11* (origen, licencia, variables, tamaño y calidad) y caracterizar la distribución de la variable objetivo.
- Identificar, mediante análisis exploratorio, las variables con mayor asociación con el puntaje global y las que deben excluirse por fuga de información o por falta de valor predictivo.
- Preparar los datos sin fuga y establecer modelos de referencia (*baseline*) con su métrica inicial.
- Entrenar y comparar modelos de regresión y clasificación, ajustar sus hiperparámetros con validación cruzada y evaluarlos con métricas apropiadas (MAE, RMSE, R², exactitud, F1, AUC-ROC, silueta).
- Segmentar a los estudiantes e interpretar los modelos (importancia por permutación, SHAP, dependencia parcial, análisis de errores).
- Comunicar los resultados en un tablero interactivo con predicción en vivo.

---

## 📚 Estructura del Repositorio

```
.
├── README.md                         # Este archivo
├── requirements.txt                  # Dependencias de Python para ejecución local
├── .gitignore                        # Excluye .venv/, data/, models/ y temporales
├── assets/
│   └── images/
│       ├── Logo.png                  # Logo institucional
│       ├── author/                   # Fotografía del autor
│       └── data/                     # Figuras generadas por los cuadernos
├── dashboard/
│   └── README.md                     # Enlace al repositorio y a la aplicación publicada del tablero
├── docs/
│   └── plan-computo-colab.md         # Plan de cómputo para Colab (de una etapa anterior del proyecto)
├── data/
│   ├── raw/                          # Copias locales opcionales (ignorado por git); los cuadernos leen desde Kaggle
│   └── processed/                    # Conjunto limpio, partición, métricas, predicciones, clústeres (ignorado por git)
├── models/                           # Preprocesadores y modelos entrenados con joblib y PyTorch (ignorado por git)
└── notebooks/
    ├── 01_planteamiento_y_eda.ipynb          # Fase 1
    ├── 02_preparacion_y_baseline.ipynb       # Fase 2
    └── 03_modelos_y_evaluacion.ipynb         # Fase 3
```

El tablero vive en su propio repositorio, [RubianoAndy/saber11-dashboard](https://github.com/RubianoAndy/saber11-dashboard), para que su despliegue sea liviano; es autónomo (descarga la muestra desde Kaggle y entrena los modelos al arrancar).

---

## 🧪 Metodología

Cada fase se desarrolla en un **cuaderno de Google Colab** dentro de `notebooks/`. Los cuadernos corren de forma independiente: el 02 y el 03 reconstruyen los artefactos de las fases anteriores desde Kaggle si no los encuentran.

### Fase 1 · Conjunto de datos

Se utiliza el conjunto **Resultados únicos Saber 11**, publicado por el ICFES en el Portal Nacional de Datos Abiertos ([datos.gov.co/d/kgxf-xxbe](https://www.datos.gov.co/Educaci-n/Resultados-nicos-Saber-11/kgxf-xxbe)) bajo licencia **CC BY-SA 4.0**, periodo **2022-4**. Se trabaja con una **muestra representativa de 1.000 estudiantes**, extraída por muestreo estratificado de los 532.792 evaluados y publicada en Kaggle como [`andyrubiano/saber-11-muestra-2022-4`](https://www.kaggle.com/datasets/andyrubiano/saber-11-muestra-2022-4) (la población completa está en [`andyrubiano/saber-11-resultados-2022-4`](https://www.kaggle.com/datasets/andyrubiano/saber-11-resultados-2022-4)). Es la única fuente que consumen los cuadernos, de modo que el análisis es reproducible aunque el portal actualice sus datos.

| Aspecto | Valor |
|---|---|
| Fuente original | ICFES · datos.gov.co, conjunto `kgxf-xxbe`, periodo 2022-4 |
| Población | 532.792 estudiantes únicos (el portal publica cada fila dos veces) |
| Muestra | 1.000 estudiantes, estratificada por naturaleza × área del colegio × tercil de puntaje (asignación proporcional, semilla 42) |
| Representatividad | Diferencias máximas de 3,0 puntos porcentuales por categoría; 0 de 11 pruebas χ² significativas; medias dentro de un error estándar |
| Columnas | 51: identificación, colegio `cole_*`, estudiante `estu_*`, hogar `fami_*`, resultados |
| Variable objetivo | `punt_global` — puntaje global (0 a 500) |
| Excluidas por fuga | `punt_lectura_critica`, `punt_matematicas`, `punt_sociales_ciudadanas`, `punt_c_naturales`, `punt_ingles`, `desemp_ingles` |

El cuaderno 01 incluye el diccionario completo de variables, el análisis del mecanismo de los faltantes (no son aleatorios: el cuestionario incompleto se asocia con 24,6 puntos menos), la detección de atípicos, estadística descriptiva univariada, correlaciones de Spearman, pruebas χ² con V de Cramér y una verificación de la versatilidad de la muestra frente a la población.

### Fase 2 · Preparación y modelo de referencia

| Aspecto | Valor |
|---|---|
| Conjunto de trabajo | 1.000 estudiantes × 24 variables explicativas (4 numéricas, 5 binarias, 15 nominales) |
| Faltantes | Categoría *No respondió* más indicador de cuestionario incompleto; imputación por mediana dentro del preprocesador (elegida frente a KNN y a eliminar filas) |
| Atípicos | Edad winsorizada en el percentil 99 (35 años); los atípicos del puntaje se conservan por ser reales |
| Variables derivadas | `personas_por_cuarto`, `extraedad`, `cuestionario_incompleto`, indicadores de educación desconocida, interacción naturaleza × área, estrato agrupado, seis regiones |
| Partición | 70 / 15 / 15 estratificada por nivel de desempeño (700 / 150 / 150), semilla 42; preprocesadores ajustados solo en entrenamiento |
| Referencias | Ridge (`alpha` = 56): **MAE 35,0 · RMSE 42,7 · R² 0,305** en prueba · regresión logística: **F1 macro 0,482 · AUC-ROC 0,664** |

### Fase 3 · Modelos y evaluación

Hiperparámetros por búsqueda con **validación cruzada de 5 pliegues repetida 3 veces** sobre el entrenamiento; el mejor modelo de cada bloque se elige por su puntuación de validación cruzada y la prueba (150 estudiantes) se usa una sola vez, con intervalo de confianza por *bootstrap*.

| Regresión | MAE cv | MAE prueba | R² prueba |
|---|---|---|---|
| **Gradient Boosting** (100 árboles, profundidad 2) | **34,53** | 34,33 | 0,286 |
| Random Forest | 34,62 | 33,81 | 0,314 |
| ElasticNet / Ridge | 34,76 / 34,77 | 34,97 / 35,00 | 0,304 / 0,305 |
| Lasso | 34,93 | 35,22 | 0,287 |
| Perceptrón multicapa (PyTorch, parada temprana) | 35,19 | 34,37 | 0,310 |
| Predecir la media | — | 42,20 | 0,000 |

| Clasificación | F1 cv | F1 macro prueba | AUC-ROC prueba |
|---|---|---|---|
| **SVM (RBF)** | **0,508** | 0,498 | 0,680 |
| Regresión logística | 0,507 | 0,482 | 0,664 |
| Random Forest | 0,503 | 0,463 | 0,693 |
| KNN | 0,482 | 0,502 | 0,681 |

**Segmentación:** K-means por nivel (puntajes por área y edad, K = 3: alto desempeño, bajo a medio y adultos de jornada nocturna y sabatina; silueta 0,38) y por perfil relativo (áreas menos el promedio del estudiante, K = 2: fuerte en lectura crítica y débil en inglés, o al revés; silueta 0,19); jerárquico de Ward con dendrograma (índice de Rand ajustado 0,40 frente a K-means) y DBSCAN, que confirma que los adultos son ruido y no un grupo propio.

**Interpretabilidad:** SHAP (aditividad exacta) y permutación coinciden en que la edad es la variable dominante, seguida de la educación de la madre y del padre, la región, el internet en el hogar y la jornada.

### Fase 4 · Tablero

Cinco vistas (panorama, brechas, predicción en vivo con explicación SHAP, segmentos y modelos) con filtros por departamento, naturaleza, jornada y género. Ver [`dashboard/README.md`](dashboard/README.md).

---

## 📊 Resultados

| Hallazgo | Cifra |
|---|---|
| Mejor regresor por validación cruzada | Gradient Boosting: MAE 34,3 en prueba, R² 0,286, 18,7 % mejor que predecir la media |
| Ganancia sobre el modelo lineal | De 0,2 a 1,2 puntos de MAE: real pero pequeña; el contexto socioeconómico y escolar explica cerca del 30 % de la varianza |
| Mejor clasificador por validación cruzada | SVM: F1 macro 0,498 y AUC-ROC 0,680; la clase *Medio* es la difícil (F1 0,38) porque los terciles cortan un puntaje continuo |
| Variables más importantes | Edad, educación de la madre y del padre, región, internet en el hogar, jornada |
| Brechas | Privado − oficial 32,4 puntos; con − sin internet 32,8; hombres − mujeres 9,3; 11,2 % de los estudiantes en extraedad |
| Límite del modelo | Comprime los extremos: sesgos de −50 puntos por debajo de 200 y +57 por encima de 300; acierta a ±25 puntos en el 43 % de los casos |

> ⚠️ **El modelo describe desigualdades estructurales; no debe usarse para decidir sobre estudiantes individuales.** Con 700 estudiantes de entrenamiento, los intervalos de confianza de los modelos se solapan: las diferencias entre ellos no son concluyentes y por eso se prefiere el más simple y estable.

---

## ⚙️ Requisitos

> ℹ️ **No requiere instalación en Google Colab.** El conjunto de datos se descarga desde Kaggle con `kagglehub`, sin necesidad de cuenta, en segundos, y las dependencias vienen preinstaladas (los cuadernos instalan `shap` si falta). Cada cuaderno corre en pocos minutos; el 03 es el más pesado (búsquedas con validación cruzada, SHAP y la red en PyTorch, que corre en CPU).

Para ejecutarlo localmente se usa un entorno virtual. Desde Git Bash, en la raíz del repositorio:

```bash
py -3.14 -m venv .venv
```

```bash
source .venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```

```bash
python -m ipykernel install --sys-prefix --name python3 --display-name "Python 3"
```

```bash
for nb in notebooks/0*.ipynb; do JUPYTER_PATH="$PWD/.venv/share/jupyter" jupyter nbconvert --to notebook --execute --inplace "$nb"; done
```

El cuarto comando registra el entorno virtual como el kernel `python3` de Jupyter, y `JUPYTER_PATH` hace que Jupyter lo prefiera sobre el Python del sistema. En VS Code basta con seleccionar `.venv` como kernel. Los cuadernos detectan la raíz del repositorio y escriben las figuras en `assets/images/data/`, los datos derivados en `data/processed/` y los modelos en `models/`.

| Etapa | Dependencias |
|---|---|
| Descarga de datos | `kagglehub` |
| Carga y agregación | `pandas`, `numpy`, `pyarrow` |
| Visualización | `matplotlib`, `seaborn` |
| Estadística | `scipy` |
| Modelos, búsqueda y segmentación | `scikit-learn`, `joblib` |
| Interpretabilidad | `shap` |
| Perceptrón multicapa | `torch` |

---

## 📋 Estado del Proyecto

### ✅ Fase 1 · Problema y exploración de datos

- ✅ Planteamiento, diccionario completo de variables, calidad de los datos, mecanismo de los faltantes, atípicos y análisis exploratorio con pruebas de independencia
- ✅ Muestra representativa de 1.000 estudiantes publicada en Kaggle y verificada frente a la población

### ✅ Fase 2 · Preparación y modelo base

- ✅ Limpieza, variables derivadas, partición estratificada, preprocesadores sin fuga y modelos de referencia (Ridge y regresión logística)
- ✅ Artefactos en `data/processed/` y `models/`

### ✅ Fase 3 · Modelado y evaluación

- ✅ Regresión (Ridge, Lasso, ElasticNet, Random Forest, Gradient Boosting, perceptrón en PyTorch), clasificación (Random Forest, SVM, KNN), K-means, jerárquico y DBSCAN
- ✅ Validación cruzada repetida, intervalos por *bootstrap*, SHAP, permutación, dependencia parcial y análisis de errores

### ✅ Fase 4 · Tablero

- ✅ Tablero en Streamlit desplegado: [saber11-dashboard.streamlit.app](https://saber11-dashboard.streamlit.app/)

### ⏳ Pendiente

- ⏳ Informe final
- ⏳ Sustentación (28 nov. 2026)
- ⏳ Publicar los cuadernos en Google Colab y registrar sus enlaces en esta sección

---

## 🔑 Palabras Clave

`Ciencia de Datos` · `Análisis Exploratorio de Datos` · `Saber 11` · `ICFES` · `Regresión` · `Clasificación` · `Clustering` · `Gradient Boosting` · `SVM` · `PyTorch` · `SHAP` · `Streamlit` · `Datos Abiertos` · `Fuga de Información` · `Nivel Socioeconómico`

---

## 🔗 Recursos

- [Tablero publicado](https://saber11-dashboard.streamlit.app/) · [código del tablero](https://github.com/RubianoAndy/saber11-dashboard)
- [Dataset — Resultados únicos Saber 11 (datos.gov.co)](https://www.datos.gov.co/Educaci-n/Resultados-nicos-Saber-11/kgxf-xxbe)
- [Muestra utilizada — Saber 11 Colombia - Muestra 2022-4 (Kaggle)](https://www.kaggle.com/datasets/andyrubiano/saber-11-muestra-2022-4)
- [Población — Saber 11 Colombia - Resultados 2022-4 (Kaggle)](https://www.kaggle.com/datasets/andyrubiano/saber-11-resultados-2022-4)
- [kagglehub](https://github.com/Kaggle/kagglehub)
- [ICFES — Prueba Saber 11](https://www.icfes.gov.co/evaluaciones-icfes/saber-11/)
- [scikit-learn — Documentación](https://scikit-learn.org/stable/)
- [SHAP — Documentación](https://shap.readthedocs.io/)
- [PyTorch — Documentación](https://pytorch.org/docs/stable/)
- [Streamlit — Documentación](https://docs.streamlit.io/)

---

## 📧 Contacto

**Andrés Giovanny Rubiano Muñoz**
Maestría en Inteligencia Artificial · Universidad de La Salle
arubiano67@unisalle.edu.co

---

## 📄 Derechos Reservados

© 2026 Andrés Giovanny Rubiano Muñoz (Andy Rubiano). Todos los derechos reservados.

Este trabajo académico y su contenido —investigación, código, metodologías y documentación— son propiedad intelectual conjunta de:

- **Andrés Giovanny Rubiano Muñoz** (Andy Rubiano) — Autor
- **Universidad de La Salle** — Institución académica

Los datos utilizados pertenecen al ICFES y se distribuyen bajo licencia CC BY-SA 4.0 a través del Portal Nacional de Datos Abiertos de Colombia. El uso, reproducción o distribución del resto del trabajo requiere autorización previa escrita de los titulares de derechos.

---

<div align="center">
  Universidad de La Salle | Bogotá D. C., Colombia
</div>
