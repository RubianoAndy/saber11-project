media = DummyRegressor(strategy="mean").fit(Xl_train, y_train)
modelos_todos = {"Media (ingenuo)": (media, "lineal"), **modelos}
tabla = tabla_metricas(modelos_todos, conjuntos)
tabla.to_csv(PROCESSED_DIR / "metricas_fase3.csv")
display(tabla)

prueba = tabla.xs("test", level="parte")
tiempos = pd.DataFrame({
    "búsqueda (s)": [0, 0, round(T_BUSQUEDA_HGB), round(T_BUSQUEDA_RF)],
    "entrenamiento final (s)": [0, 0, round(T_HGB), round(T_RF)],
    "sobreajuste (MAE train − test)": (tabla.xs("train", level="parte")["MAE"] - prueba["MAE"]).round(2).values,
}, index=prueba.index)
display(tiempos)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
colores = [GRIS, C_RIDGE, C_HGB, C_RF]
for ax, metrica, titulo in [(axes[0], "MAE", "Error absoluto medio en prueba (menor es mejor)"),
                            (axes[1], "R2", "R² en prueba (mayor es mejor)")]:
    bars = ax.bar(prueba.index, prueba[metrica], color=colores, width=0.6)
    ax.bar_label(bars, labels=[f"{v:.2f}" if metrica == "MAE" else f"{v:.3f}" for v in prueba[metrica]], padding=3, fontsize=9)
    ax.set_title(titulo); ax.tick_params(axis="x", labelsize=9); ax.grid(axis="x", visible=False)
axes[0].set_ylim(0, 50); axes[1].set_ylim(0, 0.5)
fig.tight_layout()
save_fig(fig, "model_comparison")
plt.show()

pred_test = pd.DataFrame({"y_real": y_test}, index=y_test.index)
for nombre, (m, rep) in modelos_todos.items():
    pred_test["pred_" + nombre.split(" ")[0].lower().replace("(", "")] = m.predict(conjuntos[rep]["test"][0])
pred_test.to_parquet(PROCESSED_DIR / "predicciones_fase3.parquet")
MEJOR = prueba["MAE"].idxmin()
print(f"Mejor modelo en prueba: {MEJOR} (MAE {prueba.loc[MEJOR, 'MAE']:.2f}, R² {prueba.loc[MEJOR, 'R2']:.3f})")
