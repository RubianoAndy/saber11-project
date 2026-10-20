faltantes = (df.isna().mean() * 100).round(2)
faltantes = faltantes[faltantes > 0].sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(9, 0.42 * len(faltantes) + 1.2))
bars = ax.barh(faltantes.index, faltantes.values, color=C_NEU)
ax.bar_label(bars, labels=[f"{v:.1f} %" for v in faltantes.values], padding=4, fontsize=9, color=GRIS)
ax.set_title("Porcentaje de valores faltantes por columna (solo columnas con faltantes)")
ax.set_xlabel("% de registros sin dato")
ax.set_xlim(0, faltantes.max() * 1.18)
ax.grid(axis="y", visible=False)
save_fig(fig, "missing_values")
plt.show()

fami_cols = [c for c in df.columns if c.startswith("fami_")]
sin_cuestionario = df[fami_cols].isna().all(axis=1)
algun_faltante = df[fami_cols].isna().any(axis=1)
print(f"Registros sin ningún dato del cuestionario (fami_* todo nulo): {sin_cuestionario.sum():,} "
      f"({sin_cuestionario.mean() * 100:.2f} %)")
print(f"Registros con al menos un fami_* faltante                   : {algun_faltante.sum():,} "
      f"({algun_faltante.mean() * 100:.2f} %)")
print(f"Registros con cuestionario completo                          : {(~algun_faltante).sum():,} "
      f"({(~algun_faltante).mean() * 100:.2f} %)")

comparacion = pd.DataFrame({
    "sin_cuestionario": df.loc[sin_cuestionario, "punt_global"].describe(),
    "con_cuestionario": df.loc[~sin_cuestionario, "punt_global"].describe(),
}).round(1)
display(comparacion.T)
