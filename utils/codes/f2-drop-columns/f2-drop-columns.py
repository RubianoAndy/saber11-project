TARGET = "punt_global"
LEAK_COLS = ["punt_lectura_critica", "punt_matematicas", "punt_sociales_ciudadanas",
             "punt_c_naturales", "punt_ingles", "desemp_ingles"]
CONST_COLS = ["periodo", "estu_estudiante", "estu_estadoinvestigacion", "estu_privado_libertad"]
ID_COLS = ["cole_cod_dane_establecimiento", "cole_cod_dane_sede", "cole_codigo_icfes",
           "cole_nombre_establecimiento", "cole_nombre_sede", "cole_cod_depto_ubicacion",
           "cole_cod_mcpio_ubicacion"]
REDUNDANT_COLS = ["estu_cod_depto_presentacion", "estu_cod_mcpio_presentacion", "estu_depto_presentacion",
                  "estu_mcpio_presentacion", "estu_cod_reside_depto", "estu_cod_reside_mcpio",
                  "estu_depto_reside", "estu_mcpio_reside", "estu_nacionalidad", "estu_pais_reside",
                  "estu_tipodocumento"]

df = df.set_index("estu_consecutivo")
df = df.drop(columns=LEAK_COLS + CONST_COLS + ID_COLS + REDUNDANT_COLS)
print(f"Columnas conservadas ({df.shape[1]}): {df.columns.tolist()}")
