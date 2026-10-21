geo = (df.assign(internet=(df["fami_tieneinternet"] == "Si").astype(float))
         .groupby("cole_depto_ubicacion", observed=True)
         .agg(puntaje=("punt_global", "mean"), internet=("internet", "mean"), n=("punt_global", "size"))
         .assign(internet=lambda d: d["internet"] * 100))
pend, inter = np.polyfit(geo["internet"], geo["puntaje"], 1, w=np.sqrt(geo["n"]))
geo["residuo"] = geo["puntaje"] - (pend * geo["internet"] + inter)
geo.to_csv(PROCESSED_DIR / "geografia.csv")

fig, ax = plt.subplots(figsize=(12, 7))
ax.scatter(geo["internet"], geo["puntaje"], s=geo["n"] / 120, color=[C_ACCENT if r < -4 else (C_BASE if r > 4 else C_NEU) for r in geo["residuo"]],
           alpha=0.75, edgecolors="white", linewidths=0.8, zorder=2)
xs = np.linspace(geo["internet"].min() - 3, geo["internet"].max() + 3, 50)
ax.plot(xs, pend * xs + inter, color=TINTA, linestyle="--", linewidth=1, zorder=1,
        label=f"tendencia ponderada: +{pend:.2f} puntos por cada punto porcentual de internet")
for nombre, r in geo.iterrows():
    if r["n"] > 30000 or abs(r["residuo"]) > 6 or r["internet"] < 50:
        ax.annotate(nombre.title(), (r["internet"], r["puntaje"]), textcoords="offset points", xytext=(6, 4), fontsize=8.5, color=GRIS)
ax.set_xlabel("Estudiantes con internet en el hogar (%)"); ax.set_ylabel("Puntaje global medio del departamento")
ax.set_title("¿Es la brecha regional una brecha socioeconómica? Puntaje medio frente a acceso a internet, por departamento del colegio")
ax.legend(handles=[Patch(color=C_BASE, label="rinde por encima de su contexto (> 4 puntos)"),
                   Patch(color=C_ACCENT, label="rinde por debajo de su contexto (< −4 puntos)"),
                   Patch(color=C_NEU, label="dentro de ±4 puntos"), plt.Line2D([], [], color=TINTA, linestyle="--", label=ax.get_legend_handles_labels()[1][0])],
          frameon=False, loc="lower right", fontsize=9)
save_fig(fig, "story_2_geography")
plt.show()
print(f"Correlación entre acceso a internet y puntaje medio departamental: {np.corrcoef(geo['internet'], geo['puntaje'])[0, 1]:.2f}")
display(geo.sort_values("residuo").round(1).iloc[np.r_[0:4, -4:0]].T)
