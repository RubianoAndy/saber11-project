C_BASE, C_ACCENT, C_NEU = "#2a78d6", "#eb6834", "#5B7C99"
C_HGB, C_RF, C_RIDGE, C_MEDIA = "#2a78d6", "#2CA02C", "#eb6834", "#7F7F7F"
TINTA, GRIS, CLARO = "#0b0b0b", "#52514e", "#d9d8d3"
BLOQUE_COLOR = {"Hogar": "#2a78d6", "Colegio": "#eb6834", "Estudiante": "#9467BD", "Geografía": "#2CA02C"}

sns.set_style("whitegrid")
plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 160,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.edgecolor": CLARO, "axes.labelcolor": GRIS,
    "axes.spines.top": False, "axes.spines.right": False,
    "text.color": TINTA, "xtick.color": GRIS, "ytick.color": GRIS,
    "font.size": 10, "axes.titlesize": 12.5, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "axes.titlepad": 12,
    "grid.color": "#eeede9", "grid.linewidth": 0.8,
})
RANDOM_STATE = 42

def save_fig(fig, name):
    """Guarda la figura en assets/images/data/<name>.png (160 dpi para el informe y la sustentación)."""
    path = FIG_DIR / f"{name}.png"
    fig.savefig(path, bbox_inches="tight")
    print(f"Figura guardada: {path.relative_to(PROJECT_ROOT) if path.is_relative_to(PROJECT_ROOT) else path}")

def miles(v, _=None):
    return f"{v / 1000:g} k"
