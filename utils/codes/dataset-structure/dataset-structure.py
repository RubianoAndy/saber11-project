estructura = pd.DataFrame({
    "tipo": df.dtypes.astype(str),
    "no_nulos": df.notna().sum(),
    "pct_nulos": (df.isna().mean() * 100).round(2),
    "valores_unicos": df.nunique(),
    "ejemplo": df.iloc[0].astype(str).str.slice(0, 30),
})
estructura.index.name = "columna"
display(estructura)
