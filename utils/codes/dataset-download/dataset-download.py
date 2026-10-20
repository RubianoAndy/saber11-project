DATASET_ID = "kgxf-xxbe"
PERIODO = "20224"
RAW_FILE = DATA_RAW / f"saber11_{PERIODO}.csv"
URL = (f"https://www.datos.gov.co/resource/{DATASET_ID}.csv"
       f"?periodo={PERIODO}&$limit=1200000&$order=estu_consecutivo")

if RAW_FILE.exists():
    print(f"Archivo en caché: {RAW_FILE.name} ({RAW_FILE.stat().st_size / 1e6:,.0f} MB)")
else:
    import urllib.request
    t0 = time.time()
    print("Descargando desde datos.gov.co ...")
    urllib.request.urlretrieve(URL, RAW_FILE)
    print(f"Descarga completa: {RAW_FILE.stat().st_size / 1e6:,.0f} MB en {time.time() - t0:,.0f} s")

SCORE_COLS = ["punt_matematicas", "punt_lectura_critica", "punt_sociales_ciudadanas",
              "punt_c_naturales", "punt_ingles", "punt_global"]
ID_COLS = ["estu_consecutivo", "estu_fechanacimiento"]

header = pd.read_csv(RAW_FILE, nrows=0).columns.tolist()
dtypes = {c: "category" for c in header if c not in SCORE_COLS + ID_COLS}
dtypes.update({c: "float32" for c in SCORE_COLS})
dtypes.update({c: "string" for c in ID_COLS})

t0 = time.time()
df = pd.read_csv(RAW_FILE, dtype=dtypes, low_memory=False)
print(f"\nFuente: datos.gov.co · {DATASET_ID} · periodo {PERIODO}")
print(f"Registros: {len(df):,} | Columnas: {df.shape[1]} | "
      f"Memoria: {df.memory_usage(deep=True).sum() / 1e6:,.0f} MB | Lectura: {time.time() - t0:,.0f} s")
df.head(3)
