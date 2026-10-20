fig, axes = plt.subplots(3, 1, figsize=(13, 13))
t_estrato = caja_por(axes[0], "fami_estratovivienda", ORDEN["fami_estratovivienda"], "Estrato de la vivienda")
t_madre = caja_por(axes[1], "fami_educacionmadre", ORDEN["fami_educacionmadre"],
                   "Máximo nivel educativo de la madre", rot=25)
t_padre = caja_por(axes[2], "fami_educacionpadre", ORDEN["fami_educacionpadre"],
                   "Máximo nivel educativo del padre", rot=25)
fig.tight_layout()
save_fig(fig, "family_ordinal")
plt.show()

print("Estrato:"); display(t_estrato.T)
print("Educación de la madre:"); display(t_madre.T)
print("Educación del padre:"); display(t_padre.T)
