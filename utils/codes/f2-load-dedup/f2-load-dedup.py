KAGGLE_DATASET = "andyrubiano/saber-11-resultados-2022-4"
PARQUET_FILE = "saber11_20224.parquet"

t0 = time.time()
parquet_path = kagglehub.dataset_download(KAGGLE_DATASET, path=PARQUET_FILE)
raw = pd.read_parquet(parquet_path)
n_raw = len(raw)
df = raw.drop_duplicates().reset_index(drop=True)
del raw

print(f"Fuente   : Kaggle · {KAGGLE_DATASET} · {PARQUET_FILE} (origen: ICFES, datos.gov.co kgxf-xxbe, CC BY-SA 4.0)")
print(f"Filas publicadas: {n_raw:,} | tras eliminar duplicados: {len(df):,} | "
      f"estu_consecutivo único: {df['estu_consecutivo'].is_unique} | carga: {time.time() - t0:.1f} s")
assert len(df) == 532_792 and df["estu_consecutivo"].is_unique, "El conjunto no coincide con el documentado en la fase 1"
