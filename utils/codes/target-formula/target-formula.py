calc = ((3 * df["punt_lectura_critica"] + 3 * df["punt_matematicas"] + 3 * df["punt_sociales_ciudadanas"]
         + 3 * df["punt_c_naturales"] + 1 * df["punt_ingles"]) / 13 * 5)
diff = (df["punt_global"] - calc.round()).abs()
completos = calc.notna()
print(f"Registros con las cinco pruebas    : {completos.sum():,} de {len(df):,}")
print(f"Coinciden exactamente con la fórmula: {(diff[completos] == 0).mean() * 100:.2f} %")
print(f"Diferencia absoluta máxima          : {diff[completos].max():.0f} puntos")
print(f"Diferencia absoluta ≤ 1 punto       : {(diff[completos] <= 1).mean() * 100:.2f} %")

corr_areas = df[SCORE_COLS].corr(method="pearson")["punt_global"].drop("punt_global").sort_values(ascending=False)
display(corr_areas.round(3).to_frame("correlación de Pearson con punt_global").T)
