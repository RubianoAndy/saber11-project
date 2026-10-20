EDU_NIVEL = {"Ninguno": 0, "Primaria incompleta": 1, "Primaria completa": 2,
             "Secundaria (Bachillerato) incompleta": 3, "Secundaria (Bachillerato) completa": 4,
             "Técnica o tecnológica incompleta": 5, "Técnica o tecnológica completa": 6,
             "Educación profesional incompleta": 7, "Educación profesional completa": 8, "Postgrado": 9}
ESTRATO_NIVEL = {"Sin Estrato": 0, **{f"Estrato {i}": i for i in range(1, 7)}}
PERSONAS_NIVEL = {"1 a 2": 1, "3 a 4": 2, "5 a 6": 3, "7 a 8": 4, "9 o más": 5}
CUARTOS_NIVEL = {"Uno": 1, "Dos": 2, "Tres": 3, "Cuatro": 4, "Cinco": 5, "Seis o mas": 6}

def binaria(col, positivo):
    return df[col].map(lambda v: np.nan if pd.isna(v) else float(v == positivo))

num = pd.DataFrame({
    "estrato": df["fami_estratovivienda"].astype(object).map(ESTRATO_NIVEL),
    "educ_madre": df["fami_educacionmadre"].astype(object).map(EDU_NIVEL),
    "educ_padre": df["fami_educacionpadre"].astype(object).map(EDU_NIVEL),
    "personas_hogar": df["fami_personashogar"].astype(object).map(PERSONAS_NIVEL),
    "cuartos_hogar": df["fami_cuartoshogar"].astype(object).map(CUARTOS_NIVEL),
    "tiene_internet": binaria("fami_tieneinternet", "Si"),
    "tiene_computador": binaria("fami_tienecomputador", "Si"),
    "tiene_automovil": binaria("fami_tieneautomovil", "Si"),
    "tiene_lavadora": binaria("fami_tienelavadora", "Si"),
    "colegio_no_oficial": binaria("cole_naturaleza", "NO OFICIAL"),
    "colegio_urbano": binaria("cole_area_ubicacion", "URBANO"),
    "colegio_bilingue": binaria("cole_bilingue", "S"),
    "calendario_B": binaria("cole_calendario", "B"),
    "jornada_completa_unica": df["cole_jornada"].isin(["COMPLETA", "UNICA"]).astype(float),
    "genero_F": binaria("estu_genero", "F"),
    "edad": df["edad"],
    "punt_lectura_critica": df["punt_lectura_critica"],
    "punt_matematicas": df["punt_matematicas"],
    "punt_sociales_ciudadanas": df["punt_sociales_ciudadanas"],
    "punt_c_naturales": df["punt_c_naturales"],
    "punt_ingles": df["punt_ingles"],
    "punt_global": df["punt_global"],
})

corr = num.corr(method="spearman")
ranking = corr["punt_global"].drop("punt_global").sort_values(key=np.abs, ascending=False)
print("Correlación de Spearman con punt_global (ordenada por magnitud):")
display(ranking.round(3).to_frame("rho").T)

fig, ax = plt.subplots(figsize=(13, 11))
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(corr, mask=mask, cmap="RdBu_r", vmin=-1, vmax=1, center=0, annot=True, fmt=".2f",
            annot_kws={"size": 7}, square=True, linewidths=0.4, cbar_kws={"shrink": 0.6}, ax=ax)
ax.set_title("Matriz de correlación de Spearman entre variables candidatas, puntajes por área y puntaje global")
ax.tick_params(axis="both", labelsize=8.5)
save_fig(fig, "correlation_matrix")
plt.show()
