sel_shap = np.random.default_rng(RANDOM_STATE).choice(len(Xa_muestra), 1_000, replace=False)
Xa_shap = Xa_muestra.iloc[sel_shap]
pred_shap = hgb.predict(Xa_shap)

def error_aditividad(valores):
    return float(np.abs(valores.values.sum(axis=1) + valores.base_values - pred_shap).mean())

t0 = time.time()
sv_tree = shap.TreeExplainer(hgb)(Xa_shap, check_additivity=False)
err_tree = error_aditividad(sv_tree)
print(f"TreeExplainer: {time.time() - t0:.0f} s · error de aditividad medio {err_tree:.1f} puntos")

if err_tree > 1:
    t0 = time.time()
    fondo = Xa_train.iloc[np.random.default_rng(RANDOM_STATE).choice(len(Xa_train), 100, replace=False)]
    explainer = shap.Explainer(hgb.predict, shap.maskers.Independent(fondo, max_samples=100), algorithm="permutation", seed=RANDOM_STATE)
    shap_values = explainer(Xa_shap, max_evals=2 * Xa_shap.shape[1] + 1, silent=True)
    metodo = "explicador por permutación (agnóstico)"
    print(f"{metodo}: {time.time() - t0:.0f} s · error de aditividad medio {error_aditividad(shap_values):.3f} puntos")
else:
    shap_values, metodo = sv_tree, "TreeExplainer"

shap_abs = pd.Series(np.abs(shap_values.values).mean(axis=0), index=COLS_ARBOLES).sort_values(ascending=False)
shap_abs.to_csv(PROCESSED_DIR / "shap_importancia.csv")

fig = plt.figure(figsize=(10, 7))
shap.plots.beeswarm(shap_values, max_display=15, show=False)
plt.title(f"Valores SHAP del gradient boosting · {metodo} · {len(Xa_shap):,} estudiantes de prueba", loc="left", fontweight="bold")
plt.gcf().set_size_inches(10, 7)
save_fig(plt.gcf(), "shap_beeswarm")
plt.show()
display(shap_abs.head(12).round(2).to_frame("|SHAP| medio (puntos)").T)
