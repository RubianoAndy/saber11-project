prueba = metricas.xs("test", level=1)
orden = [m for m in ["Media (ingenuo)", "Ridge (referencia)", "Gradient boosting", "Random forest"] if m in prueba.index]
prueba = prueba.loc[orden]
colores = {"Media (ingenuo)": C_MEDIA, "Ridge (referencia)": C_RIDGE, "Gradient boosting": C_HGB, "Random forest": C_RF}
mae_media = prueba.loc["Media (ingenuo)", "MAE"]

fig, axes = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw={"width_ratios": [1.15, 1]})
y = np.arange(len(prueba))
bars = axes[0].barh(y, prueba["MAE"], color=[colores[m] for m in prueba.index], height=0.55)
for yi, (m, r) in zip(y, prueba.iterrows()):
    mejora = (1 - r["MAE"] / mae_media) * 100
    axes[0].text(r["MAE"] + 0.6, yi, f"MAE {r['MAE']:.1f}  ·  R² {r['R2']:.3f}" + (f"  ·  −{mejora:.0f} % de error" if mejora > 0 else ""),
                 va="center", fontsize=9.5)
axes[0].set_yticks(y); axes[0].set_yticklabels(prueba.index, fontsize=10); axes[0].invert_yaxis()
axes[0].set_xlim(0, 62); axes[0].set_xlabel("Error absoluto medio en prueba (puntos)")
axes[0].set_title("¿Cuánto se equivoca cada modelo? (79.919 estudiantes de prueba)"); axes[0].grid(axis="y", visible=False)

dec = pred.assign(decil=pd.qcut(pred["y_real"], 10, labels=False) + 1).groupby("decil").agg(real=("y_real", "mean"), pred=("pred_gradient", "mean"))
axes[1].plot([150, 360], [150, 360], color=TINTA, linestyle="--", linewidth=1, label="predicción perfecta")
axes[1].plot(dec["real"], dec["pred"], marker="o", color=C_HGB, linewidth=2, markersize=7, label="gradient boosting")
for d, r in dec.iterrows():
    if d in (1, 5, 10):
        axes[1].annotate(f"decil {d}: real {r['real']:.0f} → predicho {r['pred']:.0f}", (r["real"], r["pred"]),
                         textcoords="offset points", xytext=(8, -14 if d == 10 else 8), fontsize=8.5, color=GRIS)
axes[1].set_xlim(150, 360); axes[1].set_ylim(150, 360)
axes[1].set_xlabel("Puntaje real medio del decil"); axes[1].set_ylabel("Puntaje predicho medio del decil")
axes[1].set_title("¿Dónde falla? Calibración por decil del puntaje real"); axes[1].legend(frameon=False, loc="upper left")
fig.tight_layout()
save_fig(fig, "story_3_prediction")
plt.show()
dentro = {m: [(pred["y_real"] - pred[c]).abs().le(25).mean() * 100, (pred["y_real"] - pred[c]).abs().le(50).mean() * 100]
          for m, c in [("Ridge", "pred_ridge"), ("Gradient boosting", "pred_gradient")]}
display(pd.DataFrame(dentro, index=["dentro de ±25 puntos (%)", "dentro de ±50 puntos (%)"]).round(1))
