BIENES = ["fami_tieneinternet", "fami_tienecomputador", "fami_tieneautomovil", "fami_tienelavadora"]
filas = []
for col in BIENES:
    g = df.groupby(col, observed=True)["punt_global"].agg(["size", "mean"])
    filas.append({"variable": col.replace("fami_tiene", "tiene_"),
                  "n_si": int(g.loc["Si", "size"]), "n_no": int(g.loc["No", "size"]),
                  "media_si": round(g.loc["Si", "mean"], 1), "media_no": round(g.loc["No", "mean"], 1),
                  "diferencia": round(g.loc["Si", "mean"] - g.loc["No", "mean"], 1)})
bienes = pd.DataFrame(filas).set_index("variable").sort_values("diferencia", ascending=False)
display(bienes)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.3), gridspec_kw={"width_ratios": [1.3, 1, 1]})
bars = axes[0].barh(bienes.index, bienes["diferencia"], color=C_BASE)
axes[0].bar_label(bars, labels=[f"+{v:.1f}" for v in bienes["diferencia"]], padding=4, fontsize=9)
axes[0].set_title("Diferencia de media (tiene − no tiene), en puntos")
axes[0].set_xlabel("Puntos de puntaje global")
axes[0].set_xlim(0, bienes["diferencia"].max() * 1.2)
axes[0].grid(axis="y", visible=False)
t_personas = caja_por(axes[1], "fami_personashogar", ORDEN["fami_personashogar"], "Personas en el hogar")
t_cuartos = caja_por(axes[2], "fami_cuartoshogar", ORDEN["fami_cuartoshogar"], "Cuartos del hogar")
fig.tight_layout()
save_fig(fig, "family_binary")
plt.show()

print("Personas en el hogar:"); display(t_personas.T)
print("Cuartos del hogar:"); display(t_cuartos.T)
