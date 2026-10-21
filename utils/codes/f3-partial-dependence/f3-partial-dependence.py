jornada_cats = prep_arboles.named_transformers_["nom"].categories_[NOM_COLS.index("cole_jornada")]
fig, axes = plt.subplots(1, 4, figsize=(16, 3.8))
PartialDependenceDisplay.from_estimator(hgb, Xa_muestra, ["educ_madre_ord", "edad", "personas_por_cuarto"],
                                        method="brute", kind="average", percentiles=(0.01, 0.99), grid_resolution=40,
                                        ax=axes[:3], line_kw={"color": C_HGB, "linewidth": 2}, random_state=RANDOM_STATE)
for ax, titulo, xl in zip(axes[:3], ["Educación de la madre (0 = ninguno, 9 = posgrado)", "Edad al presentar la prueba", "Personas por cuarto"],
                          ["nivel ordinal", "años", "razón"]):
    ax.set_title(titulo, fontsize=10); ax.set_xlabel(xl); ax.set_ylabel("Puntaje global predicho (parcial)")

pd_jornada = []
col = COLS_ARBOLES.index("cole_jornada")
for k, etiqueta in enumerate(jornada_cats):
    Xtmp = Xa_muestra.copy(); Xtmp.iloc[:, col] = float(k)
    pd_jornada.append((etiqueta, hgb.predict(Xtmp).mean()))
pd_jornada = pd.Series(dict(pd_jornada)).sort_values()
bars = axes[3].barh(pd_jornada.index, pd_jornada.values, color=C_HGB)
axes[3].bar_label(bars, labels=[f"{v:.0f}" for v in pd_jornada.values], padding=3, fontsize=8.5)
axes[3].set_xlim(pd_jornada.min() - 15, pd_jornada.max() + 20)
axes[3].set_title("Jornada del colegio", fontsize=10); axes[3].set_xlabel("Puntaje global predicho (parcial)")
fig.suptitle("Dependencia parcial del gradient boosting (5.000 filas de prueba)", x=0.01, ha="left", fontweight="bold")
fig.tight_layout()
save_fig(fig, "partial_dependence")
plt.show()
