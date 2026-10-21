t0 = time.time()
conjuntos = {"lineal": {}, "arboles": {}}
for parte, (XX, yy) in partes.items():
    conjuntos["lineal"][parte] = (prep_lineal.transform(XX), yy)
    Xa = prep_arboles.transform(XX)
    Xa.loc[:, CAT_MASK] = Xa.loc[:, CAT_MASK].mask(Xa.loc[:, CAT_MASK] < 0)
    conjuntos["arboles"][parte] = (Xa, yy)

Xl_train, y_train = conjuntos["lineal"]["train"]
Xa_train, _ = conjuntos["arboles"]["train"]
Xa_val, y_val = conjuntos["arboles"]["val"]
Xa_test, y_test = conjuntos["arboles"]["test"]
COLS_ARBOLES = Xa_train.columns.tolist()
print(f"Lineal: {Xl_train.shape[1]} columnas · Árboles: {Xa_train.shape[1]} columnas ({sum(CAT_MASK)} categóricas) · {time.time() - t0:.1f} s")
