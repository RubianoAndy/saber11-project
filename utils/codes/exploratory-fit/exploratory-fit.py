from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

PREDICTORAS = [c for c in num.columns if not c.startswith("punt_")]
muestra = num[PREDICTORAS + ["punt_global"]].dropna().sample(200_000, random_state=RANDOM_STATE)
X_tr, X_te, y_tr, y_te = train_test_split(muestra[PREDICTORAS], muestra["punt_global"],
                                          test_size=0.2, random_state=RANDOM_STATE)
lineal = LinearRegression().fit(X_tr, y_tr)
pred = lineal.predict(X_te)
print(f"Filas completas usadas: {len(muestra):,} (80 % entrenamiento / 20 % prueba)")
print(f"R² en prueba : {r2_score(y_te, pred):.3f}")
print(f"MAE en prueba: {mean_absolute_error(y_te, pred):.1f} puntos "
      f"(desviación del puntaje: {y_te.std():.1f}; MAE de predecir la media: "
      f"{mean_absolute_error(y_te, np.full_like(y_te, y_tr.mean())):.1f})")

coefs = pd.Series(lineal.coef_, index=PREDICTORAS).sort_values(key=np.abs, ascending=False)
display(coefs.round(2).to_frame("coeficiente (puntos por unidad)").T)
