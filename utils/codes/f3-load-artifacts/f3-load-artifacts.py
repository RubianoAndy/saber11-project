ARTEFACTOS = ["saber11_fase2.parquet", "particion.parquet", "columnas.json", "cat_mask.json"]
MODELOS_F2 = ["prep_lineal.joblib", "prep_arboles.joblib", "baseline_ridge.joblib"]

def preparar_fase2():
    """Reconstruye el conjunto, la partición y los preprocesadores de la fase 2 (mismo código y semilla)."""
    raw = pd.read_parquet(kagglehub.dataset_download("andyrubiano/saber-11-resultados-2022-4", path="saber11_20224.parquet"))
    d = raw.drop_duplicates().reset_index(drop=True).set_index("estu_consecutivo")
    d = d.drop(columns=["punt_lectura_critica", "punt_matematicas", "punt_sociales_ciudadanas", "punt_c_naturales",
                        "punt_ingles", "desemp_ingles", "periodo", "estu_estudiante", "estu_estadoinvestigacion",
                        "estu_privado_libertad", "cole_cod_dane_establecimiento", "cole_cod_dane_sede", "cole_codigo_icfes",
                        "cole_nombre_establecimiento", "cole_nombre_sede", "cole_cod_depto_ubicacion", "cole_cod_mcpio_ubicacion",
                        "estu_cod_depto_presentacion", "estu_cod_mcpio_presentacion", "estu_depto_presentacion",
                        "estu_mcpio_presentacion", "estu_cod_reside_depto", "estu_cod_reside_mcpio", "estu_depto_reside",
                        "estu_mcpio_reside", "estu_nacionalidad", "estu_pais_reside", "estu_tipodocumento"])
    nac = pd.to_datetime(d["estu_fechanacimiento"], format="%d/%m/%Y", errors="coerce")
    d["edad"] = ((pd.Timestamp("2022-09-04") - nac).dt.days / 365.25).round(1)
    d.loc[(d["edad"] < 13) | (d["edad"] > 80), "edad"] = np.nan
    d["edad"] = d["edad"].fillna(d["edad"].median())
    d["extraedad"] = (d["edad"] >= 19).astype("int8")
    d = d.drop(columns=["estu_fechanacimiento"])
    fami = [c for c in d.columns if c.startswith("fami_")]
    d["cuestionario_incompleto"] = d[fami].isna().any(axis=1).astype("int8")
    for col, et in [(c, "No respondió") for c in fami] + [("cole_bilingue", "No reportado"), ("cole_caracter", "No reportado")]:
        d[col] = d[col].cat.add_categories([et]).fillna(et)
    for col in d.columns[d.isna().any()]:
        d[col] = d[col].fillna(d[col].mode().iloc[0])
    edu = {"Ninguno": 0, "Primaria incompleta": 1, "Primaria completa": 2, "Secundaria (Bachillerato) incompleta": 3,
           "Secundaria (Bachillerato) completa": 4, "Técnica o tecnológica incompleta": 5, "Técnica o tecnológica completa": 6,
           "Educación profesional incompleta": 7, "Educación profesional completa": 8, "Postgrado": 9}
    for p, col in [("madre", "fami_educacionmadre"), ("padre", "fami_educacionpadre")]:
        o = d[col].astype(object).map(edu)
        d[f"educ_{p}_ord"] = o.astype("float32"); d[f"educ_{p}_desconocida"] = o.isna().astype("int8")
    per = d["fami_personashogar"].astype(object).map({"1 a 2": 1.5, "3 a 4": 3.5, "5 a 6": 5.5, "7 a 8": 7.5, "9 o más": 9.5})
    cua = d["fami_cuartoshogar"].astype(object).map({"Uno": 1, "Dos": 2, "Tres": 3, "Cuatro": 4, "Cinco": 5, "Seis o mas": 6})
    d["personas_por_cuarto"] = (per / cua).astype("float32")
    d["genero_F"] = (d["estu_genero"] == "F").astype("int8")
    d["naturaleza_area"] = (d["cole_naturaleza"].astype(str) + " · " + d["cole_area_ubicacion"].astype(str)).astype("category")
    d = d.drop(columns=["estu_genero", "fami_educacionmadre", "fami_educacionpadre"])
    cols = {"NUM_COLS": ["edad", "educ_madre_ord", "educ_padre_ord", "personas_por_cuarto"],
            "BIN_COLS": ["extraedad", "cuestionario_incompleto", "educ_madre_desconocida", "educ_padre_desconocida", "genero_F"],
            "NOM_COLS": ["fami_estratovivienda", "fami_personashogar", "fami_cuartoshogar", "fami_tieneinternet", "fami_tienecomputador",
                         "fami_tieneautomovil", "fami_tienelavadora", "cole_naturaleza", "cole_area_ubicacion", "naturaleza_area",
                         "cole_jornada", "cole_caracter", "cole_calendario", "cole_genero", "cole_sede_principal", "cole_bilingue",
                         "cole_depto_ubicacion"],
            "HIGH_CARD_COLS": ["cole_mcpio_ubicacion"], "TARGET": "punt_global"}
    for c in cols["NOM_COLS"] + cols["HIGH_CARD_COLS"]:
        d[c] = d[c].astype("category").cat.remove_unused_categories()
    deciles = pd.qcut(d["punt_global"], q=10, labels=False).to_numpy()
    pos = np.arange(len(d))
    p_tr, p_tmp = train_test_split(pos, test_size=0.30, random_state=RANDOM_STATE, stratify=deciles)
    p_va, p_te = train_test_split(p_tmp, test_size=0.50, random_state=RANDOM_STATE, stratify=deciles[p_tmp])
    part = pd.Series("train", index=d.index, name="particion"); part.iloc[p_va] = "val"; part.iloc[p_te] = "test"
    d.to_parquet(PROCESSED_DIR / "saber11_fase2.parquet"); part.astype("category").to_frame().to_parquet(PROCESSED_DIR / "particion.parquet")
    json.dump(cols, open(PROCESSED_DIR / "columnas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    feats = cols["NUM_COLS"] + cols["BIN_COLS"] + cols["NOM_COLS"] + cols["HIGH_CARD_COLS"]
    Xtr, ytr = d.loc[part == "train", feats], d.loc[part == "train", "punt_global"]
    pl = ColumnTransformer([("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), cols["NUM_COLS"]),
                            ("bin", "passthrough", cols["BIN_COLS"]),
                            ("nom", OneHotEncoder(handle_unknown="ignore", sparse_output=False, dtype=np.float32), cols["NOM_COLS"]),
                            ("mcpio", TargetEncoder(target_type="continuous", random_state=RANDOM_STATE), cols["HIGH_CARD_COLS"])],
                           verbose_feature_names_out=False).set_output(transform="pandas").fit(Xtr, ytr)
    pa = ColumnTransformer([("num", "passthrough", cols["NUM_COLS"]), ("bin", "passthrough", cols["BIN_COLS"]),
                            ("nom", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1, encoded_missing_value=-1, dtype=np.float32), cols["NOM_COLS"]),
                            ("mcpio", TargetEncoder(target_type="continuous", random_state=RANDOM_STATE), cols["HIGH_CARD_COLS"])],
                           verbose_feature_names_out=False).set_output(transform="pandas").fit(Xtr, ytr)
    json.dump([c in cols["NOM_COLS"] for c in pa.get_feature_names_out()], open(PROCESSED_DIR / "cat_mask.json", "w"))
    joblib.dump(pl, MODELS_DIR / "prep_lineal.joblib"); joblib.dump(pa, MODELS_DIR / "prep_arboles.joblib")
    joblib.dump(Ridge(alpha=0.01).fit(pl.transform(Xtr), ytr), MODELS_DIR / "baseline_ridge.joblib")

faltan = [a for a in ARTEFACTOS if not (PROCESSED_DIR / a).exists()] + [m for m in MODELOS_F2 if not (MODELS_DIR / m).exists()]
if faltan:
    print(f"Artefactos de la fase 2 no encontrados ({faltan}); se reconstruyen desde Kaggle ...")
    t0 = time.time(); preparar_fase2(); print(f"Reconstrucción completa en {time.time() - t0:.0f} s")
else:
    print("Artefactos de la fase 2 encontrados; se reutilizan.")

df = pd.read_parquet(PROCESSED_DIR / "saber11_fase2.parquet")
particion = pd.read_parquet(PROCESSED_DIR / "particion.parquet")["particion"]
COLS = json.load(open(PROCESSED_DIR / "columnas.json", encoding="utf-8"))
CAT_MASK = json.load(open(PROCESSED_DIR / "cat_mask.json"))
NUM_COLS, BIN_COLS, NOM_COLS, HIGH_CARD_COLS, TARGET = (COLS[k] for k in ["NUM_COLS", "BIN_COLS", "NOM_COLS", "HIGH_CARD_COLS", "TARGET"])
FEATURES = NUM_COLS + BIN_COLS + NOM_COLS + HIGH_CARD_COLS
prep_lineal = joblib.load(MODELS_DIR / "prep_lineal.joblib")
prep_arboles = joblib.load(MODELS_DIR / "prep_arboles.joblib")
ridge = joblib.load(MODELS_DIR / "baseline_ridge.joblib")

partes = {p: (df.loc[particion == p, FEATURES], df.loc[particion == p, TARGET]) for p in ["train", "val", "test"]}
print({p: f"{len(v[1]):,}" for p, v in partes.items()}, "| variables:", len(FEATURES))
assert [len(partes[p][1]) for p in ["train", "val", "test"]] == [372_954, 79_919, 79_919]
