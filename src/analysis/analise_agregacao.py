import pandas as pd

#NOTE: Carregador do CSV.
df = pd.read_csv('raw/3-tabelas_dezembro-de-2023_Tabela_2.csv')

coluna_saldo = 'Dezembro/2023 - sem ajuste Saldos'
coluna_grupo = 'Região e UF'

agrupado = df.groupby(coluna_grupo)[coluna_saldo].sum().reset_index()

agrupado = agrupado.sort_values(by=coluna_saldo, ascending=False)

print("📊 Soma de Saldos por Localidade:")
print(agrupado)

agrupado.to_csv('resumo_saldos_regiao.csv', index=False)