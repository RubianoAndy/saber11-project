deciles = pd.qcut(df[TARGET], q=10, labels=False).to_numpy()
posiciones = np.arange(len(df))
pos_train, pos_temp = train_test_split(posiciones, test_size=0.30, random_state=RANDOM_STATE, stratify=deciles)
pos_val, pos_test = train_test_split(pos_temp, test_size=0.50, random_state=RANDOM_STATE, stratify=deciles[pos_temp])
idx_train, idx_val, idx_test = df.index[pos_train], df.index[pos_val], df.index[pos_test]

particion = pd.Series("train", index=df.index, name="particion")
particion.loc[idx_val] = "val"
particion.loc[idx_test] = "test"
particion = particion.astype("category")

df.to_parquet(PROCESSED_DIR / "saber11_fase2.parquet")
particion.to_frame().to_parquet(PROCESSED_DIR / "particion.parquet")
json.dump({"NUM_COLS": NUM_COLS, "BIN_COLS": BIN_COLS, "NOM_COLS": NOM_COLS,
           "HIGH_CARD_COLS": HIGH_CARD_COLS, "TARGET": TARGET},
          open(PROCESSED_DIR / "columnas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

X, y = df[FEATURES], df[TARGET]
X_train, y_train = X.loc[idx_train], y.loc[idx_train]
X_val, y_val = X.loc[idx_val], y.loc[idx_val]
X_test, y_test = X.loc[idx_test], y.loc[idx_test]

control = pd.DataFrame({
    "entrenamiento": y_train.describe(), "validación": y_val.describe(), "prueba": y_test.describe()}).round(1)
print(f"Solapamiento entre partes: {len(set(idx_train) & set(idx_val) | set(idx_train) & set(idx_test) | set(idx_val) & set(idx_test))}")
display(control.T)

fig, ax = plt.subplots(figsize=(11, 3.8))
for nombre, serie, color in [("entrenamiento", y_train, C_BASE), ("validación", y_val, C_ACCENT), ("prueba", y_test, "#2CA02C")]:
    sns.kdeplot(serie, ax=ax, color=color, linewidth=1.8, label=f"{nombre} (n = {len(serie):,})")
ax.set_title("Distribución del puntaje global en las tres partes de la partición estratificada")
ax.set_xlabel("Puntaje global"); ax.set_ylabel("Densidad"); ax.legend(frameon=False)
save_fig(fig, "split_check")
plt.show()
