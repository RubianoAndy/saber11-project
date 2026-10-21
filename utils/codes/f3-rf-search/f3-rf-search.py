espacio_rf = {
    "n_estimators": [100, 200],
    "max_depth": [None, 12, 20],
    "min_samples_leaf": [20, 50, 100],
    "max_features": ["sqrt", 0.5, 1.0],
}
rf_base = RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=N_JOBS)

t0 = time.time()
busqueda_rf = RandomizedSearchCV(rf_base, espacio_rf, n_iter=N_ITER_RF, cv=cv, scoring="neg_mean_absolute_error",
                                 random_state=RANDOM_STATE, n_jobs=1, refit=False).fit(Xs, ys)
T_BUSQUEDA_RF = time.time() - t0

res_rf = (pd.DataFrame(busqueda_rf.cv_results_)
            .assign(MAE_cv=lambda d: -d["mean_test_score"], desv=lambda d: d["std_test_score"],
                    segundos=lambda d: d["mean_fit_time"] * 3)
            .sort_values("MAE_cv")
            [["param_n_estimators", "param_max_depth", "param_min_samples_leaf", "param_max_features", "MAE_cv", "desv", "segundos"]])
res_rf.columns = [c.replace("param_", "") for c in res_rf.columns]
res_rf.to_csv(PROCESSED_DIR / "busqueda_rf.csv", index=False)
MEJOR_RF = busqueda_rf.best_params_
print(f"{N_ITER_RF} combinaciones × 3 pliegues sobre 100.000 filas en {T_BUSQUEDA_RF:.0f} s | mejor MAE (cv): {-busqueda_rf.best_score_:.2f}")
print("Mejores hiperparámetros:", MEJOR_RF)
display(res_rf.reset_index(drop=True))
