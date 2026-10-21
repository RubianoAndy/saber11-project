brechas_df = pd.read_csv(PROCESSED_DIR / "brechas.csv").set_index("dimensión")
resumen = pd.DataFrame([
    ("Datos", "Estudiantes del periodo 2022-4 (sin duplicados)", f"{len(df):,}"),
    ("Datos", "Variables explicativas tras la preparación", f"{len(COLS['NUM_COLS'] + COLS['BIN_COLS'] + COLS['NOM_COLS'] + COLS['HIGH_CARD_COLS'])}"),
    ("Datos", "Partición entrenamiento / validación / prueba", "70 % / 15 % / 15 %, estratificada por deciles"),
    ("Brechas", "Educación de la madre (Ninguno → Posgrado)", f"{brechas_df.loc['Educación de la madre', 'brecha']:.0f} puntos"),
    ("Brechas", "Jornada del colegio (nocturna → completa)", f"{brechas_df.loc['Jornada del colegio', 'brecha']:.0f} puntos"),
    ("Brechas", "Departamento del colegio (Chocó → Bogotá)", f"{brechas_df.loc['Departamento del colegio', 'brecha']:.0f} puntos"),
] + [("Modelos (prueba)", m, f"MAE {r['MAE']:.2f} · RMSE {r['RMSE']:.2f} · R² {r['R2']:.3f}") for m, r in prueba.iterrows()]
  + [("Interpretación", "Variables más importantes (SHAP)", ", ".join(NOMBRE.get(c, c) for c in shap_imp.sort_values(ascending=False).index[:5])),
     ("Interpretación", "Participación del bloque Hogar / Colegio / Estudiante / Geografía", " / ".join(f"{bloques.get(b, 0):.0f} %" for b in ["Hogar", "Colegio", "Estudiante", "Geografía"])),
     ("Límites", "Estudiantes de prueba a ≤ 25 puntos de su puntaje real (boosting)", f"{dentro['Gradient boosting'][0]:.1f} %"),
     ("Límites", "Subestimación media de quienes obtienen ≥ 350 puntos", f"{sobresalientes['residuo'].mean():.0f} puntos")],
    columns=["bloque", "indicador", "valor"]).set_index(["bloque", "indicador"])
resumen.to_csv(PROCESSED_DIR / "resumen_final.csv")
display(resumen)
