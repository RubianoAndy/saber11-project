y = df["punt_global"]
desc = y.describe().round(1)
desc["asimetría"] = round(y.skew(), 3)
desc["curtosis"] = round(y.kurt(), 3)
display(desc.to_frame("punt_global").T)

fig, axes = plt.subplots(1, 2, figsize=(13, 4.2), gridspec_kw={"width_ratios": [3, 1]})
axes[0].hist(y.dropna(), bins=80, color=C_BASE, alpha=0.9, edgecolor="white", linewidth=0.3)
axes[0].axvline(y.mean(), color=C_ACCENT, linestyle="--", linewidth=1.5, label=f"Media = {y.mean():.1f}")
axes[0].axvline(y.median(), color=TINTA, linestyle=":", linewidth=1.5, label=f"Mediana = {y.median():.1f}")
axes[0].set_title(f"Distribución del puntaje global · periodo {PERIODO} (n = {y.notna().sum():,})")
axes[0].set_xlabel("Puntaje global (0 a 500)")
axes[0].set_ylabel("Estudiantes")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v / 1000:.0f} k"))
axes[0].legend(frameon=False)

sns.boxplot(y=y, ax=axes[1], color=C_BASE, width=0.4, fliersize=1.5,
            flierprops={"markerfacecolor": GRIS, "markeredgecolor": "none", "alpha": 0.3})
axes[1].set_title("Diagrama de caja")
axes[1].set_ylabel("Puntaje global")
fig.tight_layout()
save_fig(fig, "target_distribution")
plt.show()

p = np.percentile(y.dropna(), [1, 5, 25, 50, 75, 95, 99])
print("Percentiles 1, 5, 25, 50, 75, 95, 99:", np.round(p, 1))
