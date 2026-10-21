rng = np.random.default_rng(RANDOM_STATE)
X_sint = rng.normal(size=(50_000, 20))
y_sint = X_sint[:, :5].sum(axis=1) + rng.normal(scale=0.5, size=50_000)
t0 = time.time()
HistGradientBoostingRegressor(max_iter=50, random_state=RANDOM_STATE).fit(X_sint, y_sint)
SEGUNDOS_CONTROL = time.time() - t0
MODO_RAPIDO = SEGUNDOS_CONTROL > 15
N_ITER_HGB = 8 if MODO_RAPIDO else 16
N_ITER_RF = 4 if MODO_RAPIDO else 8
N_RF_FINAL = 200_000 if MODO_RAPIDO else None
print(f"Boosting de control (50 iteraciones, 50.000 filas): {SEGUNDOS_CONTROL:.1f} s → "
      f"{'modo rápido' if MODO_RAPIDO else 'presupuesto completo'}: "
      f"{N_ITER_HGB} combinaciones para boosting, {N_ITER_RF} para random forest, "
      f"random forest final sobre {'200.000 filas' if MODO_RAPIDO else 'todo el entrenamiento'}")
del X_sint, y_sint
