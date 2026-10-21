err = pred.assign(error=(pred["y_real"] - pred["pred_gradient"]).abs(), residuo=pred["y_real"] - pred["pred_gradient"],
                  tramo=pd.cut(pred["y_real"], [0, 150, 200, 250, 300, 350, 500], labels=["< 150", "150-200", "200-250", "250-300", "300-350", "≥ 350"]))
err = err.join(df.loc[err.index, ["cole_naturaleza", "cole_jornada", "educ_madre_ord"]])
por_tramo = err.groupby("tramo", observed=True).agg(n=("error", "size"), mae=("error", "mean"), sesgo=("residuo", "mean"))
sobresalientes = err[err["y_real"] >= 350]
resumen_sob = sobresalientes.groupby("cole_naturaleza", observed=True).agg(n=("y_real", "size"), real=("y_real", "mean"), predicho=("pred_gradient", "mean"))
resumen_sob["subestimación"] = resumen_sob["real"] - resumen_sob["predicho"]

fig, axes = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw={"width_ratios": [1.2, 1]})
bars = axes[0].bar(por_tramo.index.astype(str), por_tramo["mae"], color=[C_ACCENT if m > 35 else C_HGB for m in por_tramo["mae"]], width=0.62)
axes[0].bar_label(bars, labels=[f"{m:.0f} pts\n(n = {n:,})" for m, n in zip(por_tramo["mae"], por_tramo["n"])], padding=3, fontsize=8.5)
axes[0].axhline(err["error"].mean(), color=TINTA, linestyle="--", linewidth=1); axes[0].text(5.45, err["error"].mean() + 1, f"MAE global {err['error'].mean():.1f}", ha="right", fontsize=9, color=GRIS)
axes[0].set_ylim(0, por_tramo["mae"].max() * 1.3); axes[0].set_xlabel("Puntaje real del estudiante"); axes[0].set_ylabel("Error absoluto medio (puntos)")
axes[0].set_title("¿Para quién falla? Error del boosting según el puntaje real"); axes[0].grid(axis="x", visible=False)

muestra = sobresalientes.sample(min(1500, len(sobresalientes)), random_state=RANDOM_STATE)
for nat, color in [("OFICIAL", C_HGB), ("NO OFICIAL", C_ACCENT)]:
    m = muestra[muestra["cole_naturaleza"] == nat]
    axes[1].scatter(m["pred_gradient"], m["y_real"], s=14, alpha=0.5, color=color, edgecolors="none", label=f"colegio {nat.lower()} (n = {resumen_sob.loc[nat, 'n']:,})")
axes[1].plot([200, 470], [200, 470], color=TINTA, linestyle="--", linewidth=1)
axes[1].axhline(350, color=CLARO, linewidth=1)
for nat, yy in [("OFICIAL", 455), ("NO OFICIAL", 440)]:
    r = resumen_sob.loc[nat]
    axes[1].text(203, yy, f"{nat.title()}: real {r['real']:.0f}, predicho {r['predicho']:.0f} → {r['subestimación']:.0f} puntos por debajo", fontsize=9, color=TINTA)
axes[1].set_xlim(200, 470); axes[1].set_ylim(340, 470); axes[1].set_xlabel("Puntaje predicho por el boosting"); axes[1].set_ylabel("Puntaje real (≥ 350)")
axes[1].set_title("Los sobresalientes que el contexto no anticipa"); axes[1].legend(frameon=False, loc="lower right", fontsize=9)
fig.tight_layout()
save_fig(fig, "story_5_errors")
plt.show()
print(f"Estudiantes de prueba con 350 puntos o más: {len(sobresalientes):,} ({len(sobresalientes) / len(pred) * 100:.1f} %); "
      f"el modelo predice 350 o más para {(pred['pred_gradient'] >= 350).sum():,} de ellos")
display(resumen_sob.round(1).T)
