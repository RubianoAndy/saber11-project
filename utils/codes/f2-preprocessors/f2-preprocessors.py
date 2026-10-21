prep_lineal = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), NUM_COLS),
    ("bin", "passthrough", BIN_COLS),
    ("nom", OneHotEncoder(handle_unknown="ignore", sparse_output=False, dtype=np.float32), NOM_COLS),
    ("mcpio", TargetEncoder(target_type="continuous", random_state=RANDOM_STATE), HIGH_CARD_COLS),
], verbose_feature_names_out=False).set_output(transform="pandas")

prep_arboles = ColumnTransformer([
    ("num", "passthrough", NUM_COLS),
    ("bin", "passthrough", BIN_COLS),
    ("nom", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1, encoded_missing_value=-1,
                           dtype=np.float32), NOM_COLS),
    ("mcpio", TargetEncoder(target_type="continuous", random_state=RANDOM_STATE), HIGH_CARD_COLS),
], verbose_feature_names_out=False).set_output(transform="pandas")

t0 = time.time()
Xl_train = prep_lineal.fit_transform(X_train, y_train)
Xa_train = prep_arboles.fit_transform(X_train, y_train)
CAT_MASK = [c in NOM_COLS for c in Xa_train.columns]
print(f"Representación lineal : {Xl_train.shape[1]} columnas | "
      f"Representación árboles: {Xa_train.shape[1]} columnas ({sum(CAT_MASK)} categóricas) | ajuste: {time.time() - t0:.1f} s")

joblib.dump(prep_lineal, MODELS_DIR / "prep_lineal.joblib")
joblib.dump(prep_arboles, MODELS_DIR / "prep_arboles.joblib")
json.dump(CAT_MASK, open(PROCESSED_DIR / "cat_mask.json", "w"))
print("Preprocesadores guardados en models/")
