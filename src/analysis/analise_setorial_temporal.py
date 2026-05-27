import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
 
# Caminhos
RAIZ = Path(__file__).resolve().parents[2]
CAMINHO_DADOS = RAIZ / "data" / "processed" / "caged" / "caged_setorial_rs.csv"
CAMINHO_OUTPUT = RAIZ / "outputs" / "charts" / "evolucao_setorial_rs.png"
 
CAMINHO_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
 
# Carregamento e preparação
df = pd.read_csv(CAMINHO_DADOS)
df["Data"] = pd.to_datetime(df["Ano"].astype(str) + "-" + df["Mes"].astype(str).str.zfill(2) + "-01")
df = df.sort_values("Data")
 
setores = df["Setor"].unique()
 
cores = {
    "Agropecuária": "#4CAF50",
    "Indústria":    "#2196F3",
    "Construção":   "#FF9800",
    "Comércio":     "#9C27B0",
    "Serviços":     "#F44336",
}
 
fig, ax = plt.subplots(figsize=(14, 7))
 
for setor in setores:
    dados_setor = df[df["Setor"] == setor].copy()
    cor = cores.get(setor, "#607D8B")
    ax.plot(
        dados_setor["Data"],
        dados_setor["Saldo_Setorial"],
        marker="o",
        linewidth=2,
        markersize=5,
        label=setor,
        color=cor,
    )
 
# Marcação do evento crítico (maio/2024)
evento = pd.Timestamp("2024-05-01")
ax.axvline(x=evento, color="red", linestyle="--", linewidth=1.8, alpha=0.8)
ax.text(
    evento,
    ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 100,
    "  Enchentes\n  Mai/2024",
    color="red",
    fontsize=9,
    verticalalignment="top",
)
 
# Linha de referência zero
ax.axhline(y=0, color="black", linewidth=0.8, linestyle="-", alpha=0.4)
 
# Formatação dos eixos
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=45, ha="right", fontsize=9)
ax.set_xlabel("Mês/Ano", fontsize=11)
ax.set_ylabel("Saldo de Empregos (admissões − desligamentos)", fontsize=11)
ax.set_title(
    "Evolução do Saldo de Empregos por Setor Econômico — Rio Grande do Sul (2023–2025)",
    fontsize=13,
    fontweight="bold",
    pad=15,
)
 
ax.legend(title="Setor", loc="upper right", fontsize=9, title_fontsize=10)
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
 
plt.savefig(CAMINHO_OUTPUT, dpi=150, bbox_inches="tight")
print(f"✅ Gráfico salvo em: {CAMINHO_OUTPUT.relative_to(RAIZ)}")
plt.close()
