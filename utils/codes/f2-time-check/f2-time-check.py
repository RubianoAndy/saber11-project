rng = np.random.default_rng(RANDOM_STATE)
X_sint = rng.normal(size=(50_000, 20))
y_sint = X_sint[:, :5].sum(axis=1) + rng.normal(scale=0.5, size=50_000)
t0 = time.time()
HistGradientBoostingRegressor(max_iter=50, random_state=RANDOM_STATE).fit(X_sint, y_sint)
SEGUNDOS_CONTROL = time.time() - t0
MODO_RAPIDO = SEGUNDOS_CONTROL > 15
print(f"Boosting de control (50 iteraciones, 50.000 filas): {SEGUNDOS_CONTROL:.1f} s "
      f"→ {'entorno lento: modo rápido activado' if MODO_RAPIDO else 'entorno dentro del presupuesto'}")
del X_sint, y_sint
