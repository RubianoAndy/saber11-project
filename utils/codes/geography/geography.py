geo = (df.groupby("cole_depto_ubicacion", observed=True)["punt_global"]
         .agg(n="size", media="mean", mediana="median", desv="std").round(1)
         .sort_values("media", ascending=True))
display(geo.sort_values("media", ascending=False).T)

fig, ax = plt.subplots(figsize=(10, 0.3 * len(geo) + 1.5))
colores = [C_ACCENT if m < df["punt_global"].mean() else C_BASE for m in geo["media"]]
bars = ax.barh(geo.index, geo["media"], color=colores)
ax.bar_label(bars, labels=[f"{m:.0f}  (n = {n:,})" for m, n in zip(geo["media"], geo["n"])],
             padding=4, fontsize=8, color=GRIS)
ax.axvline(df["punt_global"].mean(), color=TINTA, linestyle="--", linewidth=1,
           label=f"Media nacional = {df['punt_global'].mean():.1f}")
ax.set_xlim(geo["media"].min() - 20, geo["media"].max() + 60)
ax.set_title("Puntaje global medio por departamento del colegio")
ax.set_xlabel("Puntaje global medio")
ax.tick_params(axis="y", labelsize=8.5)
ax.grid(axis="y", visible=False)
ax.legend(frameon=False, loc="lower right")
save_fig(fig, "geography")
plt.show()

print(f"Brecha entre el departamento con mayor y menor media: "
      f"{geo['media'].max() - geo['media'].min():.1f} puntos "
      f"({geo['media'].idxmax()} vs. {geo['media'].idxmin()})")
