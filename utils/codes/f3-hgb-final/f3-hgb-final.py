t0 = time.time()
hgb = HistGradientBoostingRegressor(**MEJOR_HGB, categorical_features=CAT_MASK, early_stopping=False, random_state=RANDOM_STATE)
hgb.fit(Xa_train, y_train)
T_HGB = time.time() - t0
print(f"Boosting final: {hgb.n_iter_} iteraciones sobre {len(y_train):,} filas en {T_HGB:.0f} s")
modelos["Gradient boosting"] = (hgb, "arboles")
joblib.dump(hgb, MODELS_DIR / "hgb.joblib")
display(tabla_metricas({"Gradient boosting": modelos["Gradient boosting"]}, conjuntos))
