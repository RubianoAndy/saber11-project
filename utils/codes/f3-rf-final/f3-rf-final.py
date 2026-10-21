t0 = time.time()
if N_RF_FINAL is None:
    X_rf, y_rf = Xa_train, y_train
else:
    sel = np.random.default_rng(RANDOM_STATE).choice(len(Xa_train), N_RF_FINAL, replace=False)
    X_rf, y_rf = Xa_train.iloc[sel], y_train.iloc[sel]
rf = RandomForestRegressor(**MEJOR_RF, random_state=RANDOM_STATE, n_jobs=N_JOBS).fit(X_rf, y_rf)
T_RF = time.time() - t0
print(f"Random forest final sobre {len(y_rf):,} filas: {T_RF:.0f} s · {MEJOR_RF['n_estimators']} árboles · "
      f"profundidad media {np.mean([t.get_depth() for t in rf.estimators_]):.1f}")
modelos["Random forest"] = (rf, "arboles")
joblib.dump(rf, MODELS_DIR / "rf.joblib", compress=3)
display(tabla_metricas({"Random forest": modelos["Random forest"]}, conjuntos))
