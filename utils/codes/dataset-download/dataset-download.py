import kagglehub

KAGGLE_DATASET = "andyrubiano/saber-11-resultados-2022-4"
PARQUET_FILE = "saber11_20224.parquet"
PERIODO = "20224"

SCORE_COLS = ["punt_matematicas", "punt_lectura_critica", "punt_sociales_ciudadanas",
              "punt_c_naturales", "punt_ingles", "punt_global"]
ID_COLS = ["estu_consecutivo", "estu_fechanacimiento"]

t0 = time.time()
parquet_path = kagglehub.dataset_download(KAGGLE_DATASET, path=PARQUET_FILE)
df = pd.read_parquet(parquet_path)

print(f"Fuente   : Kaggle · {KAGGLE_DATASET} · {PARQUET_FILE}")
print(f"Origen   : ICFES · datos.gov.co, conjunto kgxf-xxbe, periodo 2022-4 (CC BY-SA 4.0)")
print(f"Registros: {len(df):,} | Columnas: {df.shape[1]} | "
      f"Memoria: {df.memory_usage(deep=True).sum() / 1e6:,.0f} MB | Carga: {time.time() - t0:,.1f} s")
df.head(3)
