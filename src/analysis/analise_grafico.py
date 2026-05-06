import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#NOTE: Carregador do CSV.
caminho = 'raw/3-tabelas_dezembro-de-2023_Tabela_2.csv'
df = pd.read_csv(caminho)

df_estados = df[~df['Região e UF'].isin(['Brasil', 'Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste'])]

plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

df_plot = df_estados.melt(id_vars='Região e UF', 
                          value_vars=['Dezembro/2023 - sem ajuste Admissões', 
                                      'Dezembro/2023 - sem ajuste Desligamentos'],
                          var_name='Tipo', value_name='Total')

sns.barplot(data=df_plot, x='Região e UF', y='Total', hue='Tipo')
plt.xticks(rotation=45)
plt.title('Admissões vs Desligamentos por Estado (Dezembro/2023)')
plt.tight_layout()

plt.savefig('graficos/grafico_comparativo.png')
print("✅ Gráfico salvo como 'grafico_comparativo.png'")
plt.show()