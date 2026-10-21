EDU = {0: "Ninguno", 1: "Primaria inc.", 2: "Primaria", 3: "Secundaria inc.", 4: "Secundaria", 5: "Técnica inc.",
       6: "Técnica", 7: "Profesional inc.", 8: "Profesional", 9: "Posgrado"}
desc = df.assign(educ_madre=df["educ_madre_ord"].map(EDU).fillna("No sabe / no respondió"),
                 tramo_edad=pd.cut(df["edad"], [0, 17, 18, 20, 100], labels=["16-17", "18", "19-20", "21+"]))
DIMENSIONES = [("Educación de la madre", "educ_madre", "Hogar"), ("Jornada del colegio", "cole_jornada", "Colegio"),
               ("Edad al presentar", "tramo_edad", "Estudiante"), ("Departamento del colegio", "cole_depto_ubicacion", "Geografía"),
               ("Naturaleza × área", "naturaleza_area", "Colegio"), ("Estrato", "fami_estratovivienda", "Hogar"),
               ("Internet en el hogar", "fami_tieneinternet", "Hogar"), ("Computador en el hogar", "fami_tienecomputador", "Hogar"),
               ("Carácter del colegio", "cole_caracter", "Colegio"), ("Género", "genero_F", "Estudiante")]
filas = []
for etiqueta, col, bloque in DIMENSIONES:
    g = desc.groupby(col, observed=True)["punt_global"].agg(["mean", "size"])
    g = g[g["size"] >= 1000]
    filas.append({"dimensión": etiqueta, "bloque": bloque, "grupo bajo": str(g["mean"].idxmin()), "media baja": g["mean"].min(),
                  "grupo alto": str(g["mean"].idxmax()), "media alta": g["mean"].max(), "brecha": g["mean"].max() - g["mean"].min()})
brechas = pd.DataFrame(filas).sort_values("brecha", ascending=True)
brechas["grupo alto"] = brechas["grupo alto"].replace({"1": "Mujer", "0": "Hombre"}); brechas["grupo bajo"] = brechas["grupo bajo"].replace({"1": "Mujer", "0": "Hombre"})
brechas.to_csv(PROCESSED_DIR / "brechas.csv", index=False)

fig, ax = plt.subplots(figsize=(12, 6.4))
for i, r in enumerate(brechas.itertuples()):
    ax.plot([r._4, r._6], [i, i], color=CLARO, linewidth=3, zorder=1)
    ax.scatter(r._4, i, s=70, color=C_ACCENT, zorder=2); ax.scatter(r._6, i, s=70, color=C_BASE, zorder=2)
    ax.text(r._4 - 3, i, f"{r._3} ({r._4:.0f})", ha="right", va="center", fontsize=8.5, color=GRIS)
    ax.text(r._6 + 3, i, f"{r._5} ({r._6:.0f})", ha="left", va="center", fontsize=8.5, color=GRIS)
    ax.text((r._4 + r._6) / 2, i + 0.32, f"{r.brecha:.0f} puntos", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=TINTA)
ax.set_yticks(range(len(brechas))); ax.set_yticklabels(brechas["dimensión"], fontsize=10)
ax.set_xlim(150, 360); ax.set_xlabel("Puntaje global medio (escala 0 a 500)")
ax.axvline(df["punt_global"].mean(), color=TINTA, linestyle=":", linewidth=1)
ax.text(df["punt_global"].mean() + 1.5, len(brechas) - 0.55, f"media nacional {df['punt_global'].mean():.0f}", fontsize=8.5, color=GRIS, va="top")
ax.set_title("¿Cuánto separa el contexto a los estudiantes? Brecha entre el grupo de menor y mayor puntaje medio por dimensión")
ax.legend(handles=[Patch(color=C_ACCENT, label="grupo de menor puntaje"), Patch(color=C_BASE, label="grupo de mayor puntaje")],
          frameon=False, loc="lower right")
ax.grid(axis="y", visible=False)
save_fig(fig, "story_1_gaps")
plt.show()
display(brechas.sort_values("brecha", ascending=False).round(1).set_index("dimensión"))
