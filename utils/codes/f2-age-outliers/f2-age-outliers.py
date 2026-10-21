FECHA_PRUEBA = pd.Timestamp("2022-09-04")
fecha_nac = pd.to_datetime(df["estu_fechanacimiento"], format="%d/%m/%Y", errors="coerce")
df["edad"] = ((FECHA_PRUEBA - fecha_nac).dt.days / 365.25).round(1)
fuera = (df["edad"] < 13) | (df["edad"] > 80)
df.loc[fuera, "edad"] = np.nan
edad_faltante = df["edad"].isna().sum()
df["edad"] = df["edad"].fillna(df["edad"].median())
df["extraedad"] = (df["edad"] >= 19).astype("int8")
df = df.drop(columns=["estu_fechanacimiento"])
print(f"Edades no válidas imputadas con la mediana ({df['edad'].median():.1f} años): {edad_faltante:,}")
print(f"Estudiantes en extraedad (≥ 19 años): {df['extraedad'].sum():,} ({df['extraedad'].mean() * 100:.1f} %)")

q1, q3 = df[TARGET].quantile([0.25, 0.75])
iqr = q3 - q1
atipicos = (df[TARGET] < q1 - 1.5 * iqr) | (df[TARGET] > q3 + 1.5 * iqr)
print(f"\nPuntaje global: Q1 = {q1:.0f}, Q3 = {q3:.0f}, límites de Tukey [{q1 - 1.5 * iqr:.0f}, {q3 + 1.5 * iqr:.0f}]")
print(f"Valores atípicos por el criterio de 1,5 IQR: {atipicos.sum():,} ({atipicos.mean() * 100:.2f} %) → se conservan")
print(f"Puntajes exactamente 0: {(df[TARGET] == 0).sum():,} → se conservan")
