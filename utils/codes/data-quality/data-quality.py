n_inicial = len(df)
duplicados = df.duplicated().sum()
print(f"Registros descargados                : {n_inicial:,}")
print(f"Registros duplicados (fila completa) : {duplicados:,} ({duplicados / n_inicial * 100:.2f} %)")
print(f"Valores distintos de estu_consecutivo: {df['estu_consecutivo'].nunique():,}")

df = df.drop_duplicates().reset_index(drop=True)
repetidos = df["estu_consecutivo"].duplicated(keep=False).sum()
print()
print(f"Registros tras eliminar duplicados   : {len(df):,}")
print(f"estu_consecutivo es único            : {df['estu_consecutivo'].is_unique}"
      + ("" if repetidos == 0 else f" ({repetidos:,} filas comparten identificador con contenido distinto)"))

n_unique = df.nunique()
constantes = n_unique[n_unique <= 1].index.tolist()
print(f"\nColumnas constantes (1 valor)        : {constantes}")

print("\nColumnas con muy poca variación (categoría dominante > 99 %):")
for col in df.columns.drop(SCORE_COLS + ID_COLS):
    share = df[col].value_counts(normalize=True, dropna=False).iloc[0]
    if share > 0.99 and col not in constantes:
        top = df[col].value_counts(dropna=False).index[0]
        print(f"  {col:<32} {str(top):<22} {share * 100:6.2f} %")

print("\nCardinalidad de las variables categóricas:")
card = n_unique.drop(SCORE_COLS + ID_COLS).sort_values(ascending=False)
display(card.to_frame("valores_unicos").T)
