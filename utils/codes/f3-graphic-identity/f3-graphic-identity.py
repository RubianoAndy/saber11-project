C_BASE, C_ACCENT, C_NEU = "#2a78d6", "#eb6834", "#5B7C99"
C_HGB, C_RF, C_RIDGE = "#2a78d6", "#2CA02C", "#eb6834"
TINTA, GRIS = "#0b0b0b", "#52514e"
PALETTE = [C_BASE, C_ACCENT, "#2CA02C", "#9467BD", "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22"]

sns.set_style("whitegrid")
sns.set_palette(PALETTE)
plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 110,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.edgecolor": "#d9d8d3", "axes.labelcolor": GRIS,
    "axes.spines.top": False, "axes.spines.right": False,
    "text.color": TINTA, "xtick.color": GRIS, "ytick.color": GRIS,
    "font.size": 10, "axes.titlesize": 12, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "axes.titlepad": 12,
    "grid.color": "#eeede9", "grid.linewidth": 0.8,
})

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

def save_fig(fig, name):
    """Guarda la figura en assets/images/data/<name>.png."""
    path = FIG_DIR / f"{name}.png"
    fig.savefig(path, bbox_inches="tight")
    print(f"Figura guardada: {path.relative_to(PROJECT_ROOT) if path.is_relative_to(PROJECT_ROOT) else path}")

def evaluar(y_true, y_pred):
    """MAE, RMSE y R² en un diccionario."""
    return {"MAE": round(mean_absolute_error(y_true, y_pred), 2),
            "RMSE": round(root_mean_squared_error(y_true, y_pred), 2),
            "R2": round(r2_score(y_true, y_pred), 4)}

def tabla_metricas(modelos, conjuntos):
    """Tabla modelo × parte con las tres métricas, a partir de modelos ajustados y matrices por parte."""
    filas = {}
    for nombre, (modelo, rep) in modelos.items():
        for parte, (XX, yy) in conjuntos[rep].items():
            filas[(nombre, parte)] = evaluar(yy, modelo.predict(XX))
    tabla = pd.DataFrame(filas).T
    tabla.index.names = ["modelo", "parte"]
    return tabla
