pred_test = ridge.predict(Xl_test)
resid = y_test - pred_test
muestra = np.random.default_rng(RANDOM_STATE).choice(len(y_test), 20_000, replace=False)

fig, axes = plt.subplots(1, 2, figsize=(13, 4.6), gridspec_kw={"width_ratios": [1.1, 1]})
axes[0].scatter(pred_test[muestra], y_test.values[muestra], s=4, alpha=0.25, color=C_BASE, edgecolors="none")
lims = [100, 450]
axes[0].plot(lims, lims, color=TINTA, linewidth=1, linestyle="--", label="predicción perfecta")
axes[0].set_xlim(lims); axes[0].set_ylim(50, 500)
axes[0].set_title("Puntaje real frente a predicho · Ridge · conjunto de prueba (muestra de 20.000)")
axes[0].set_xlabel("Puntaje predicho"); axes[0].set_ylabel("Puntaje real"); axes[0].legend(frameon=False)

axes[1].hist(resid, bins=80, color=C_ACCENT, alpha=0.9, edgecolor="white", linewidth=0.3)
axes[1].axvline(0, color=TINTA, linewidth=1, linestyle="--")
axes[1].set_title(f"Residuos (real − predicho): media {resid.mean():.1f}, desviación {resid.std():.1f}")
axes[1].set_xlabel("Residuo en puntos"); axes[1].set_ylabel("Estudiantes")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v / 1000:g} k"))
fig.tight_layout()
save_fig(fig, "baseline_diagnostics")
plt.show()

por_tramo = pd.DataFrame({"real": y_test, "pred": pred_test}).assign(
    tramo=lambda d: pd.cut(d["real"], [0, 200, 250, 300, 350, 500]))
sesgo = por_tramo.groupby("tramo", observed=True).apply(
    lambda g: pd.Series({"n": len(g), "residuo medio": (g["real"] - g["pred"]).mean(),
                         "MAE": (g["real"] - g["pred"]).abs().mean()})).round(1)
print("Sesgo del modelo por tramo de puntaje real:")
display(sesgo.T)
