import pandas as pd

#NOTE: Carregador do CSV.
df_estados = pd.read_csv('raw/3-tabelas_dezembro-de-2023_Tabela_2.csv')
df_municipios = pd.read_csv('raw/3-tabelas_dezembro-de-2023_Tabela_3.csv')



print("Efetuando cruzamento de dados...")

df_cruzado = pd.merge(
    df_municipios, 
    df_estados[['Região e UF', 'Dezembro/2023 - sem ajuste Saldos']], 
    left_on='UF',
    right_on='Região e UF',
    suffixes=('_municipio', '_estado')
)

print(f"✅ Cruzamento concluído. Linhas geradas: {len(df_cruzado)}")
print(df_cruzado[['Região e UF', 'Saldos', 'Dezembro/2023 - sem ajuste Saldos']].head())

df_cruzado.to_csv('dados_municipios_com_estado.csv', index=False)