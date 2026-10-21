BLOQUE = {}
for c in COLS["NOM_COLS"] + COLS["NUM_COLS"] + COLS["BIN_COLS"] + COLS["HIGH_CARD_COLS"]:
    if c in ("cole_depto_ubicacion", "cole_mcpio_ubicacion"): BLOQUE[c] = "Geografía"
    elif c.startswith("cole_") or c == "naturaleza_area": BLOQUE[c] = "Colegio"
    elif c.startswith("fami_") or c.startswith("educ_") or c in ("personas_por_cuarto", "cuestionario_incompleto"): BLOQUE[c] = "Hogar"
    else: BLOQUE[c] = "Estudiante"
NOMBRE = {"cole_mcpio_ubicacion": "Municipio del colegio", "edad": "Edad", "cole_jornada": "Jornada", "educ_madre_ord": "Educación de la madre",
          "educ_padre_ord": "Educación del padre", "cole_depto_ubicacion": "Departamento", "fami_estratovivienda": "Estrato", "genero_F": "Género",
          "naturaleza_area": "Naturaleza × área", "fami_tienecomputador": "Computador", "cole_naturaleza": "Naturaleza", "fami_cuartoshogar": "Cuartos del hogar",
          "fami_tieneinternet": "Internet", "personas_por_cuarto": "Personas por cuarto", "fami_tieneautomovil": "Automóvil", "cole_caracter": "Carácter",
          "fami_personashogar": "Personas en el hogar", "extraedad": "Extraedad", "fami_tienelavadora": "Lavadora", "cole_area_ubicacion": "Área",
          "cole_genero": "Género del colegio", "cole_calendario": "Calendario", "cole_sede_principal": "Sede principal", "cole_bilingue": "Bilingüe",
          "educ_madre_desconocida": "Educ. madre desconocida", "educ_padre_desconocida": "Educ. padre desconocida", "cuestionario_incompleto": "Cuestionario incompleto"}

imp = pd.DataFrame({"permutación": importancias["Gradient boosting"], "SHAP": shap_imp.reindex(importancias.index)})
imp_norm = imp / imp.max()
top = imp_norm.sort_values("SHAP", ascending=False).head(14)
bloques = (imp["SHAP"].groupby(pd.Series(BLOQUE)).sum() / imp["SHAP"].sum() * 100).sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1.6, 1]})
yy = np.arange(len(top))
axes[0].barh(yy - 0.2, top["SHAP"], height=0.4, color=[BLOQUE_COLOR[BLOQUE[c]] for c in top.index], label="SHAP (|valor| medio)")
axes[0].barh(yy + 0.2, top["permutación"], height=0.4, color=[BLOQUE_COLOR[BLOQUE[c]] for c in top.index], alpha=0.45, label="permutación (aumento del MAE)")
axes[0].set_yticks(yy); axes[0].set_yticklabels([NOMBRE.get(c, c) for c in top.index], fontsize=9.5); axes[0].invert_yaxis()
axes[0].set_xlabel("Importancia relativa al máximo de cada método (1 = municipio)")
axes[0].set_title("¿Qué variables explican la predicción del boosting? Dos métodos, un mismo ranking")
axes[0].legend(handles=[Patch(color=TINTA, label="SHAP (|valor| medio)"), Patch(color=TINTA, alpha=0.45, label="permutación (aumento del MAE)")]
               + [Patch(color=v, label=k) for k, v in BLOQUE_COLOR.items()], frameon=False, fontsize=8.5, loc="lower right")
bars = axes[1].bar(bloques.index, bloques.values, color=[BLOQUE_COLOR[b] for b in bloques.index], width=0.62)
axes[1].bar_label(bars, labels=[f"{v:.0f} %" for v in bloques.values], padding=3, fontsize=10)
axes[1].set_ylim(0, bloques.max() * 1.25); axes[1].set_ylabel("Participación en la suma de |SHAP| (%)")
axes[1].set_title("¿Qué bloque pesa más en conjunto?"); axes[1].grid(axis="x", visible=False)
fig.tight_layout()
save_fig(fig, "story_4_importance")
plt.show()
display(imp.sort_values("SHAP", ascending=False).head(10).round(2).T)
