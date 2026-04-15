import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o CSV da Tabela 2.
caminho = 'raw/3-tabelas_dezembro-de-2023_Tabela_2.csv'
df = pd.read_csv(caminho)

# Filtrar para remover o total "Brasil" e as regiões, focando nos estados.
# Assumindo que os estados não são as primeiras linhas de resumo.
df_estados = df[~df['Região e UF'].isin(['Brasil', 'Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste'])]

# Configurar o estilo do gráfico.
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

# Preparar os dados para o gráfico de barras comparativo.
df_plot = df_estados.melt(id_vars='Região e UF', 
                          value_vars=['Dezembro/2023 - sem ajuste Admissões', 
                                      'Dezembro/2023 - sem ajuste Desligamentos'],
                          var_name='Tipo', value_name='Total')

sns.barplot(data=df_plot, x='Região e UF', y='Total', hue='Tipo')
plt.xticks(rotation=45)
plt.title('Admissões vs Desligamentos por Estado (Dezembro/2023)')
plt.tight_layout()

# Salvar e mostrar.
plt.savefig('graficos/grafico_comparativo.png')
print("✅ Gráfico salvo como 'grafico_comparativo.png'")
plt.show()