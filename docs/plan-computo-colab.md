# Plan de cómputo para las fases 2 y 3 en Google Colab

El conjunto de trabajo tiene 532.792 estudiantes y unas 22 variables explicativas. Este documento fija cómo se van a preparar los datos y entrenar los modelos para que cada cuaderno corra completo en el plan gratuito de Colab (2 núcleos de CPU, unos 12 GB de RAM, desconexión tras inactividad) sin recortar el alcance del proyecto.

## 1. Medición de referencia

Tiempos medidos el 20 de octubre de 2026 en un equipo local limitado a 2 núcleos (`OMP_NUM_THREADS=2`), con scikit-learn 1.9. Colab gratuito suele ser entre 2 y 4 veces más lento; la columna de la derecha es el presupuesto que se asume para Colab.

| Tarea | Local, 2 núcleos | Presupuesto en Colab |
|---|---|---|
| Carga del Parquet desde Kaggle y deduplicación | 1 s | 10 s |
| Matriz *one-hot* de 150 columnas, 532.792 filas (324 MB) | 2 s | 10 s |
| Ridge sobre 426.000 filas de entrenamiento | 0,4 s | 2 s |
| `HistGradientBoostingRegressor`, 300 iteraciones, 426.000 filas | 8 s | 30 s |
| `RandomForestRegressor`, 100 árboles, 100.000 filas | 9 s | 40 s |
| Búsqueda aleatoria de boosting, 8 combinaciones × 3 pliegues, 100.000 filas | 18 s | 1 min |

Conclusión: la memoria no es una restricción en ninguna fase. El tiempo solo lo es si se entrena un Random Forest sobre todas las filas o se corre la validación cruzada completa con muchas combinaciones. Ambas cosas se evitan con las reglas de abajo.

## 2. Reglas de diseño

1. **Deduplicar antes de particionar.** Es la primera operación tras la carga. Un mismo estudiante en entrenamiento y prueba invalida cualquier métrica.
2. **Partición estratificada y fija.** 70 % entrenamiento, 15 % validación, 15 % prueba, con `random_state = 42` y estratificación por deciles de `punt_global`. Los índices se guardan en `data/processed/particion.parquet` para que las fases 3 y 4 usen exactamente las mismas filas.
3. **Dos representaciones de las variables, una por familia de modelos.**
   - *One-hot* con `dummy_na=True` para los modelos lineales (unas 150 columnas en `float32`).
   - Códigos enteros con `categorical_features` para el boosting por histogramas, que maneja categorías y faltantes de forma nativa y evita la matriz ancha.
4. **Ajuste de hiperparámetros sobre una muestra, entrenamiento final con todo.** La búsqueda se hace con `RandomizedSearchCV` sobre 100.000 filas de entrenamiento y validación cruzada de 3 pliegues. El mejor modelo de cada familia se reentrena con las 373.000 filas de entrenamiento y se evalúa una sola vez en prueba.
5. **Modelos candidatos de la fase 3.** Regresión lineal regularizada (Ridge) como referencia; `HistGradientBoostingRegressor` de scikit-learn como modelo principal; `RandomForestRegressor` como segundo modelo adicional, entrenado con `min_samples_leaf ≥ 20` y, si en Colab supera los 5 minutos, sobre una muestra de 200.000 filas documentada en el informe. No se usan KNN ni SVR: su costo crece de forma cuadrática con las filas.
6. **Interpretabilidad sobre una muestra.** Importancia por permutación y SHAP se calculan sobre 5.000 filas de prueba, con semilla fija. SHAP para boosting por histogramas se obtiene con `shap.TreeExplainer`; si la versión instalada no soporta el estimador, se usa `shap.Explainer` con una muestra de fondo de 500 filas.
7. **Guardar lo que cuesta calcular.** Modelos ajustados con `joblib` en `models/` y resultados de búsqueda en CSV dentro de `data/processed/`. Si Colab desconecta la sesión, el cuaderno retoma desde el último artefacto guardado en lugar de repetir la búsqueda. Los archivos se ignoran en git salvo los CSV de resultados.
8. **Una celda de control de tiempo al inicio de cada cuaderno.** Entrena un boosting de 50 iteraciones sobre 50.000 filas y reporta los segundos. Si tarda más de 15 s, el cuaderno reduce automáticamente el número de combinaciones de la búsqueda a la mitad y lo deja registrado en la salida.

## 3. Presupuesto por cuaderno

| Cuaderno | Contenido | Tiempo estimado en Colab |
|---|---|---|
| `02_preparacion_y_baseline` | Carga, deduplicación, limpieza, variables derivadas, dos representaciones, partición, Ridge con su métrica | < 3 min |
| `03_modelos_y_evaluacion` | Búsqueda aleatoria para boosting y Random Forest, reentrenamiento final, comparación, importancia, SHAP, análisis de errores | 10 a 25 min |
| `04_visualizaciones` | Gráficas finales a partir de los artefactos guardados | < 2 min |

## 4. Qué se verifica en la primera ejecución en Colab

- Que `kagglehub` descargue el Parquet sin cuenta.
- La salida de la celda de control de tiempo, para ajustar los presupuestos de esta tabla con cifras reales de Colab.
- Que los artefactos se guarden en Google Drive montado o se descarguen al final de la sesión, porque el disco de Colab se borra al cerrar.
