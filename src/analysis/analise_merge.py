import pandas as pd

# Carregar as duas tabelas.
df_estados = pd.read_csv('raw/3-tabelas_dezembro-de-2023_Tabela_2.csv')
df_municipios = pd.read_csv('raw/3-tabelas_dezembro-de-2023_Tabela_3.csv')

# Para cruzar, precisamos de uma coluna em comum. 
# Na Tabela 3, geralmente temos o nome do estado ou UF.
# Vamos fazer um merge simplificado.
# Nota: Verifique se os nomes das colunas de UF batem entre os arquivos.

print("Efetuando cruzamento de dados...")

# Exemplo de merge: Trazendo o saldo do Estado para a linha de cada Município.
df_cruzado = pd.merge(
    df_municipios, 
    df_estados[['Região e UF', 'Dezembro/2023 - sem ajuste Saldos']], 
    left_on='UF', # Ajuste o nome dessa coluna conforme o CSV da Tabela 3.
    right_on='Região e UF',
    suffixes=('_municipio', '_estado')
)

print(f"✅ Cruzamento concluído. Linhas geradas: {len(df_cruzado)}")
print(df_cruzado[['Região e UF', 'Saldos', 'Dezembro/2023 - sem ajuste Saldos']].head())

# Salvar o "Master File".
df_cruzado.to_csv('dados_municipios_com_estado.csv', index=False)