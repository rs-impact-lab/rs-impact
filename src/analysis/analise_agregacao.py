import pandas as pd

# Carregar o CSV.
df = pd.read_csv('raw/3-tabelas_dezembro-de-2023_Tabela_2.csv')

# Realizar o agrupamento e soma.
# O nome da coluna pode variar dependendo de como o cabeçalho foi mesclado.
coluna_saldo = 'Dezembro/2023 - sem ajuste Saldos'
coluna_grupo = 'Região e UF'

agrupado = df.groupby(coluna_grupo)[coluna_saldo].sum().reset_index()

# Ordenar pelos maiores saldos.
agrupado = agrupado.sort_values(by=coluna_saldo, ascending=False)

print("📊 Soma de Saldos por Localidade:")
print(agrupado)

# Opcional: Salvar o resumo.
agrupado.to_csv('resumo_saldos_regiao.csv', index=False)