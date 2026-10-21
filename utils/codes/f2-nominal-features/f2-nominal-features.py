df["naturaleza_area"] = (df["cole_naturaleza"].astype(str) + " · " + df["cole_area_ubicacion"].astype(str)).astype("category")

NUM_COLS = ["edad", "educ_madre_ord", "educ_padre_ord", "personas_por_cuarto"]
BIN_COLS = ["extraedad", "cuestionario_incompleto", "educ_madre_desconocida", "educ_padre_desconocida", "genero_F"]
NOM_COLS = ["fami_estratovivienda", "fami_personashogar", "fami_cuartoshogar", "fami_tieneinternet",
            "fami_tienecomputador", "fami_tieneautomovil", "fami_tienelavadora",
            "cole_naturaleza", "cole_area_ubicacion", "naturaleza_area", "cole_jornada", "cole_caracter",
            "cole_calendario", "cole_genero", "cole_sede_principal", "cole_bilingue", "cole_depto_ubicacion"]
HIGH_CARD_COLS = ["cole_mcpio_ubicacion"]
FEATURES = NUM_COLS + BIN_COLS + NOM_COLS + HIGH_CARD_COLS

df = df.drop(columns=["fami_educacionmadre", "fami_educacionpadre"])
assert set(FEATURES) == set(df.columns) - {TARGET}, set(df.columns) ^ set(FEATURES) ^ {TARGET}
for col in NOM_COLS + HIGH_CARD_COLS:
    df[col] = df[col].astype("category").cat.remove_unused_categories()

resumen = pd.DataFrame({
    "grupo": (["numérica"] * len(NUM_COLS) + ["binaria"] * len(BIN_COLS)
              + ["nominal"] * len(NOM_COLS) + ["alta cardinalidad"] * len(HIGH_CARD_COLS)),
    "niveles": [df[c].nunique() for c in FEATURES],
}, index=FEATURES)
print(f"Variables explicativas: {len(FEATURES)} | objetivo: {TARGET} | filas: {len(df):,}")
display(resumen.T)
