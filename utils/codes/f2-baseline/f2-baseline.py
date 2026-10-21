Xl_val, Xl_test = prep_lineal.transform(X_val), prep_lineal.transform(X_test)

resultados = {}
t0 = time.time()
media = DummyRegressor(strategy="mean").fit(Xl_train, y_train)
resultados["Media (ingenuo)"] = {p: evaluar(yy, media.predict(XX)) for p, XX, yy in
                                 [("train", Xl_train, y_train), ("val", Xl_val, y_val), ("test", Xl_test, y_test)]}

lineal = Ridge(alpha=1e-6).fit(Xl_train, y_train)
resultados["Lineal sin regularizar"] = {p: evaluar(yy, lineal.predict(XX)) for p, XX, yy in
                                        [("train", Xl_train, y_train), ("val", Xl_val, y_val), ("test", Xl_test, y_test)]}

ALPHAS = np.logspace(-2, 3, 11)
ridge_cv = RidgeCV(alphas=ALPHAS, cv=5, scoring="neg_mean_absolute_error").fit(Xl_train, y_train)
ridge = Ridge(alpha=ridge_cv.alpha_).fit(Xl_train, y_train)
resultados["Ridge (referencia)"] = {p: evaluar(yy, ridge.predict(XX)) for p, XX, yy in
                                    [("train", Xl_train, y_train), ("val", Xl_val, y_val), ("test", Xl_test, y_test)]}
print(f"alpha elegido por validación cruzada: {ridge_cv.alpha_:g} | entrenamiento de los tres modelos: {time.time() - t0:.1f} s")

tabla = pd.concat({m: pd.DataFrame(r).T for m, r in resultados.items()}, axis=0)
tabla.index.names = ["modelo", "parte"]
display(tabla)

joblib.dump(ridge, MODELS_DIR / "baseline_ridge.joblib")
tabla.to_csv(PROCESSED_DIR / "metricas_fase2.csv")
pd.DataFrame({"y_real": y_test, "pred_ridge": ridge.predict(Xl_test)}, index=y_test.index).to_parquet(PROCESSED_DIR / "predicciones_fase2.parquet")
print("Modelo de referencia y métricas guardados.")
