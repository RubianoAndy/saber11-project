sel = np.random.default_rng(RANDOM_STATE).choice(len(Xa_test), 5_000, replace=False)
Xa_muestra, y_muestra = Xa_test.iloc[sel], y_test.iloc[sel]

t0 = time.time()
importancias = {}
for nombre in ["Gradient boosting", "Random forest"]:
    m = modelos[nombre][0]
    pi = permutation_importance(m, Xa_muestra, y_muestra, scoring="neg_mean_absolute_error",
                                n_repeats=5, random_state=RANDOM_STATE, n_jobs=N_JOBS)
    importancias[nombre] = pd.Series(pi.importances_mean, index=COLS_ARBOLES)
importancias = pd.DataFrame(importancias)
importancias.to_csv(PROCESSED_DIR / "importancias.csv")
print(f"Importancia por permutación (5.000 filas × 5 repeticiones × 2 modelos): {time.time() - t0:.0f} s")

top = importancias.sort_values("Gradient boosting", ascending=False).head(15)
fig, ax = plt.subplots(figsize=(10, 6.2))
yy = np.arange(len(top))
ax.barh(yy + 0.2, top["Gradient boosting"], height=0.4, color=C_HGB, label="Gradient boosting")
ax.barh(yy - 0.2, top["Random forest"], height=0.4, color=C_RF, label="Random forest")
ax.set_yticks(yy); ax.set_yticklabels(top.index, fontsize=9); ax.invert_yaxis()
ax.set_title("Importancia por permutación: aumento del MAE al barajar cada variable (5.000 filas de prueba)")
ax.set_xlabel("Aumento del MAE en puntos"); ax.legend(frameon=False)
save_fig(fig, "permutation_importance")
plt.show()
display(top.round(2).T)
