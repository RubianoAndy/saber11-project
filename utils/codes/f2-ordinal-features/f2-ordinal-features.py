EDU_NIVEL = {"Ninguno": 0, "Primaria incompleta": 1, "Primaria completa": 2,
             "Secundaria (Bachillerato) incompleta": 3, "Secundaria (Bachillerato) completa": 4,
             "Técnica o tecnológica incompleta": 5, "Técnica o tecnológica completa": 6,
             "Educación profesional incompleta": 7, "Educación profesional completa": 8, "Postgrado": 9}
PERSONAS_MEDIO = {"1 a 2": 1.5, "3 a 4": 3.5, "5 a 6": 5.5, "7 a 8": 7.5, "9 o más": 9.5}
CUARTOS_MEDIO = {"Uno": 1, "Dos": 2, "Tres": 3, "Cuatro": 4, "Cinco": 5, "Seis o mas": 6}

for padre, col in [("madre", "fami_educacionmadre"), ("padre", "fami_educacionpadre")]:
    ordinal = df[col].astype(object).map(EDU_NIVEL)
    df[f"educ_{padre}_ord"] = ordinal.astype("float32")
    df[f"educ_{padre}_desconocida"] = ordinal.isna().astype("int8")

personas = df["fami_personashogar"].astype(object).map(PERSONAS_MEDIO)
cuartos = df["fami_cuartoshogar"].astype(object).map(CUARTOS_MEDIO)
df["personas_por_cuarto"] = (personas / cuartos).astype("float32")
df["genero_F"] = (df["estu_genero"] == "F").astype("int8")
df = df.drop(columns=["estu_genero"])

print("Educación de la madre (ordinal 0-9):")
display(df["educ_madre_ord"].describe().round(2).to_frame().T)
print(f"Nivel desconocido: madre {df['educ_madre_desconocida'].mean() * 100:.1f} % · padre {df['educ_padre_desconocida'].mean() * 100:.1f} %")
print("\nPersonas por cuarto:")
display(df["personas_por_cuarto"].describe().round(2).to_frame().T)
