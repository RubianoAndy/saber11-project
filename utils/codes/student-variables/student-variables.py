def resumen_por(col, orden=None, min_n=0):
    """Tamaño, media, mediana y desviación del puntaje global por categoría de `col`."""
    tabla = (df.groupby(col, observed=True)["punt_global"]
               .agg(n="size", media="mean", mediana="median", desv="std").round(1))
    if orden is not None:
        tabla = tabla.reindex([o for o in orden if o in tabla.index])
    return tabla[tabla["n"] >= min_n]

def caja_por(ax, col, orden=None, titulo=None, color=C_BASE, rot=0, min_n=0):
    """Diagrama de caja del puntaje global por categoría, con el tamaño de cada grupo en el eje."""
    tabla = resumen_por(col, orden, min_n)
    sns.boxplot(data=df[df[col].isin(tabla.index)], x=col, y="punt_global", order=tabla.index,
                ax=ax, color=color, width=0.6, showfliers=False)
    ax.set_xticklabels([f"{c}\n(n = {n:,})" for c, n in zip(tabla.index, tabla["n"])], rotation=rot,
                       ha="right" if rot else "center", fontsize=8.5)
    ax.set_title(titulo or col)
    ax.set_xlabel("")
    ax.set_ylabel("Puntaje global")
    return tabla

df["edad_grupo"] = pd.cut(df["edad"], bins=[12, 15, 16, 17, 18, 20, 25, 80],
                          labels=["13-15", "16", "17", "18", "19-20", "21-25", "26+"], right=True)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.3), gridspec_kw={"width_ratios": [1, 2.2, 1.6]})
t_genero = caja_por(axes[0], "estu_genero", ["F", "M"], "Género del estudiante")
t_edad = caja_por(axes[1], "edad_grupo", None, "Edad al presentar la prueba (años)")
t_doc = caja_por(axes[2], "estu_tipodocumento", None, "Tipo de documento", min_n=1000)
fig.tight_layout()
save_fig(fig, "student_variables")
plt.show()

print("Género:"); display(t_genero.T)
print("Edad:"); display(t_edad.T)
print("Tipo de documento (grupos con n ≥ 1.000):"); display(t_doc.T)
