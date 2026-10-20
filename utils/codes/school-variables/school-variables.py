fig, axes = plt.subplots(2, 4, figsize=(17, 8.5))
axes = axes.ravel()
t_nat = caja_por(axes[0], "cole_naturaleza", ["OFICIAL", "NO OFICIAL"], "Naturaleza del colegio")
t_area = caja_por(axes[1], "cole_area_ubicacion", ["URBANO", "RURAL"], "Área de ubicación")
t_cal = caja_por(axes[2], "cole_calendario", ["A", "B", "OTRO"], "Calendario")
t_bil = caja_por(axes[3], "cole_bilingue", ["N", "S"], "Colegio bilingüe")
t_jor = caja_por(axes[4], "cole_jornada", None, "Jornada", rot=25, min_n=1000)
t_car = caja_por(axes[5], "cole_caracter", None, "Carácter", rot=25, min_n=1000)
t_gen = caja_por(axes[6], "cole_genero", ["MIXTO", "FEMENINO", "MASCULINO"], "Género del colegio", rot=25)
t_sede = caja_por(axes[7], "cole_sede_principal", ["S", "N"], "Es sede principal")
fig.tight_layout()
save_fig(fig, "school_variables")
plt.show()

for nombre, tabla in [("Naturaleza", t_nat), ("Área", t_area), ("Calendario", t_cal), ("Bilingüe", t_bil),
                      ("Jornada", t_jor), ("Carácter", t_car), ("Género del colegio", t_gen)]:
    print(f"{nombre}:"); display(tabla.T)
