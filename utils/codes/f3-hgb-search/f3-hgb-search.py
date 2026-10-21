muestra = np.random.default_rng(RANDOM_STATE).choice(len(Xa_train), 100_000, replace=False)
Xs, ys = Xa_train.iloc[muestra], y_train.iloc[muestra]
cv = KFold(n_splits=3, shuffle=True, random_state=RANDOM_STATE)

espacio_hgb = {
    "learning_rate": [0.03, 0.05, 0.1, 0.2],
    "max_iter": [200, 400, 800],
    "max_leaf_nodes": [15, 31, 63, 127],
    "min_samples_leaf": [20, 50, 100, 200],
    "l2_regularization": [0.0, 0.5, 1.0, 5.0],
}
hgb_base = HistGradientBoostingRegressor(categorical_features=CAT_MASK, early_stopping=False, random_state=RANDOM_STATE)

t0 = time.time()
busqueda_hgb = RandomizedSearchCV(hgb_base, espacio_hgb, n_iter=N_ITER_HGB, cv=cv, scoring="neg_mean_absolute_error",
                                  random_state=RANDOM_STATE, n_jobs=N_JOBS, refit=False).fit(Xs, ys)
T_BUSQUEDA_HGB = time.time() - t0

res_hgb = (pd.DataFrame(busqueda_hgb.cv_results_)
             .assign(MAE_cv=lambda d: -d["mean_test_score"], desv=lambda d: d["std_test_score"],
                     segundos=lambda d: d["mean_fit_time"] * 3)
             .sort_values("MAE_cv")
             [["param_learning_rate", "param_max_iter", "param_max_leaf_nodes", "param_min_samples_leaf",
               "param_l2_regularization", "MAE_cv", "desv", "segundos"]])
res_hgb.columns = [c.replace("param_", "") for c in res_hgb.columns]
res_hgb.to_csv(PROCESSED_DIR / "busqueda_hgb.csv", index=False)
MEJOR_HGB = busqueda_hgb.best_params_
print(f"{N_ITER_HGB} combinaciones × 3 pliegues sobre 100.000 filas en {T_BUSQUEDA_HGB:.0f} s | mejor MAE (cv): {-busqueda_hgb.best_score_:.2f}")
print("Mejores hiperparámetros:", MEJOR_HGB)
display(res_hgb.head(8).reset_index(drop=True))
