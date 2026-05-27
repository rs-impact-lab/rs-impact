import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CAMINHO_DADOS = RAIZ / "data" / "processed" / "caged" / "caged_setorial_rs.csv"
CAMINHO_OUTPUT = RAIZ / "outputs" / "charts" / "impacto_setorial_maio_2024.png"

ANO_ALVO  = 2024
MES_ALVO  = 5

df = pd.read_csv(CAMINHO_DADOS)
df_mes = df[(df["Ano"] == ANO_ALVO) & (df["Mes"] == MES_ALVO)].copy()
df_mes = df_mes.sort_values("Saldo_Setorial")

cores = df_mes["Saldo_Setorial"].apply(lambda x: "#d9534f" if x < 0 else "#5b9bd5")

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(df_mes["Setor"], df_mes["Saldo_Setorial"], color=cores)

for bar, val in zip(bars, df_mes["Saldo_Setorial"]):
    offset = -0.6 if val < 0 else 0.1
    ax.text(val + offset, bar.get_y() + bar.get_height() / 2,
            str(val), va="center", ha="right" if val < 0 else "left",
            fontsize=11, fontweight="bold")

ax.axvline(x=0, color="black", linewidth=0.8)
ax.set_xlabel("Saldo Líquido de Vagas", fontsize=11)
ax.set_ylabel("Setor", fontsize=11)
ax.set_title(f"Saldo de Empregos por Setor Econômico no RS — Maio/{ANO_ALVO}",
             fontsize=13, fontweight="bold")
ax.grid(axis="x", linestyle="--", alpha=0.4)
fig.tight_layout()

plt.savefig(CAMINHO_OUTPUT, dpi=150, bbox_inches="tight")
print(f"✅ Gráfico salvo em: {CAMINHO_OUTPUT.relative_to(RAIZ)}")
plt.close()
