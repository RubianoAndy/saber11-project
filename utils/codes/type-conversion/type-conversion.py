FECHA_PRUEBA = pd.Timestamp("2022-09-04")
fecha_nac = pd.to_datetime(df["estu_fechanacimiento"], format="%d/%m/%Y", errors="coerce")
df["edad"] = ((FECHA_PRUEBA - fecha_nac).dt.days / 365.25).round(1)
fuera_rango = (df["edad"] < 13) | (df["edad"] > 80)
print(f"Fechas no interpretables : {fecha_nac.isna().sum():,}")
print(f"Edades fuera de [13, 80] : {fuera_rango.sum():,} → se marcan como faltantes")
df.loc[fuera_rango, "edad"] = np.nan

ORDEN = {
    "fami_estratovivienda": ["Sin Estrato", "Estrato 1", "Estrato 2", "Estrato 3",
                             "Estrato 4", "Estrato 5", "Estrato 6"],
    "fami_educacionmadre": ["Ninguno", "Primaria incompleta", "Primaria completa",
                            "Secundaria (Bachillerato) incompleta", "Secundaria (Bachillerato) completa",
                            "Técnica o tecnológica incompleta", "Técnica o tecnológica completa",
                            "Educación profesional incompleta", "Educación profesional completa",
                            "Postgrado", "No sabe", "No Aplica"],
    "fami_personashogar": ["1 a 2", "3 a 4", "5 a 6", "7 a 8", "9 o más"],
    "fami_cuartoshogar": ["Uno", "Dos", "Tres", "Cuatro", "Cinco", "Seis o mas"],
    "desemp_ingles": ["A-", "A1", "A2", "B1", "B+"],
}
ORDEN["fami_educacionpadre"] = ORDEN["fami_educacionmadre"]

for col, orden in ORDEN.items():
    presentes = [o for o in orden if o in df[col].cat.categories]
    faltan = [c for c in df[col].cat.categories if c not in orden]
    if faltan:
        print(f"  {col}: categorías no previstas en el orden → {faltan}")
    df[col] = df[col].cat.set_categories(presentes + faltan, ordered=True)

print("\nEdad al presentar la prueba:")
display(df["edad"].describe().round(1).to_frame().T)
