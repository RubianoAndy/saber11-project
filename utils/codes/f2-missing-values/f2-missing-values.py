FAMI_COLS = [c for c in df.columns if c.startswith("fami_")]
df["cuestionario_incompleto"] = df[FAMI_COLS].isna().any(axis=1).astype("int8")

def agregar_categoria(serie, etiqueta):
    serie = serie.cat.add_categories([etiqueta]) if etiqueta not in serie.cat.categories else serie
    return serie.fillna(etiqueta)

for col in FAMI_COLS:
    df[col] = agregar_categoria(df[col], "No respondió")
for col in ["cole_bilingue", "cole_caracter"]:
    df[col] = agregar_categoria(df[col], "No reportado")

restantes = df.columns[df.isna().any()].tolist()
for col in restantes:
    df[col] = df[col].fillna(df[col].mode().iloc[0])
print(f"Cuestionario incompleto: {df['cuestionario_incompleto'].sum():,} estudiantes ({df['cuestionario_incompleto'].mean() * 100:.2f} %)")
print(f"Columnas rellenadas con la moda (faltantes residuales): {restantes}")
print(f"Faltantes que quedan en el conjunto: {int(df.isna().sum().sum())}")
