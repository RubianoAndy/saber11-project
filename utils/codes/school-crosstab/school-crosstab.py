cruce = df.pivot_table(index="cole_naturaleza", columns="cole_area_ubicacion", values="punt_global",
                       aggfunc=["mean", "size"], observed=True)
cruce.columns = [f"{a}_{b}" for a, b in cruce.columns]
display(cruce.round(1))
