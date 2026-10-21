err = pred_test[["y_real"]].copy()
err["ridge"] = pred_test["y_real"] - pred_test["pred_ridge"]
err["hgb"] = pred_test["y_real"] - pred_test["pred_gradient"]
err = err.join(df.loc[err.index, ["cole_naturaleza", "cole_area_ubicacion", "cole_jornada", "cole_depto_ubicacion", "extraedad"]])
err["tramo"] = pd.cut(err["y_real"], [0, 200, 250, 300, 350, 500])

def resumen(grupo):
    g = err.groupby(grupo, observed=True)
    return pd.DataFrame({"n": g.size(),
                         "sesgo Ridge": g["ridge"].mean(), "MAE Ridge": g["ridge"].apply(lambda s: s.abs().mean()),
                         "sesgo boosting": g["hgb"].mean(), "MAE boosting": g["hgb"].apply(lambda s: s.abs().mean())}).round(1)

print("Por tramo de puntaje real:"); display(resumen("tramo").T)
print("Por naturaleza y área del colegio:"); display(resumen(["cole_naturaleza", "cole_area_ubicacion"]).T)
print("Por jornada:"); display(resumen("cole_jornada").T)
dep = resumen("cole_depto_ubicacion").sort_values("MAE boosting")
print("Departamentos con menor y mayor MAE del boosting:"); display(pd.concat([dep.head(4), dep.tail(4)]).T)

dentro = pd.DataFrame({m: [(err[m].abs() <= 25).mean() * 100, (err[m].abs() <= 50).mean() * 100] for m in ["ridge", "hgb"]},
                      index=["dentro de ±25 puntos (%)", "dentro de ±50 puntos (%)"]).round(1)
display(dentro)

fig, axes = plt.subplots(1, 2, figsize=(13, 4.2), gridspec_kw={"width_ratios": [1, 1.2]})
tr = resumen("tramo")
x = np.arange(len(tr)); w = 0.38
axes[0].bar(x - w / 2, tr["sesgo Ridge"], w, color=C_RIDGE, label="Ridge")
axes[0].bar(x + w / 2, tr["sesgo boosting"], w, color=C_HGB, label="Gradient boosting")
axes[0].axhline(0, color=TINTA, linewidth=0.8)
axes[0].set_xticks(x); axes[0].set_xticklabels([str(i) for i in tr.index], fontsize=9)
axes[0].set_title("Sesgo (residuo medio) por tramo de puntaje real"); axes[0].set_ylabel("Puntos"); axes[0].legend(frameon=False)
axes[1].barh(dep.index, dep["MAE boosting"], color=[C_ACCENT if v > err["hgb"].abs().mean() else C_HGB for v in dep["MAE boosting"]])
axes[1].axvline(err["hgb"].abs().mean(), color=TINTA, linestyle="--", linewidth=1, label=f"MAE global = {err['hgb'].abs().mean():.1f}")
axes[1].set_title("MAE del gradient boosting por departamento del colegio"); axes[1].tick_params(axis="y", labelsize=7)
axes[1].set_xlim(20, dep["MAE boosting"].max() + 3); axes[1].legend(frameon=False, loc="lower right"); axes[1].grid(axis="y", visible=False)
fig.tight_layout()
save_fig(fig, "error_analysis")
plt.show()

peores = err.reindex(err["hgb"].abs().sort_values(ascending=False).index[:10])
peores = peores.join(df.loc[peores.index, ["educ_madre_ord", "fami_estratovivienda", "fami_tieneinternet"]])
peores.insert(1, "pred_boosting", (peores["y_real"] - peores["hgb"]).round(0))
print("Los diez estudiantes peor predichos por el boosting:")
display(peores.drop(columns=["ridge", "tramo"]).round(0))
