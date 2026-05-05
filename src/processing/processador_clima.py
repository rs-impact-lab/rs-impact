import pandas as pd
from pathlib import Path
import logging

# Configuração básica de logs (essencial para backend/infra)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def processar_clima():
    raw_path = Path("data/raw/inmet")
    output_path = Path("data/processed/clima")
    output_path.mkdir(parents=True, exist_ok=True)

    arquivos = list(raw_path.rglob("*.CSV"))
    if not arquivos:
        logging.error("Nenhum arquivo CSV encontrado em data/raw/inmet/")
        return

    lista_dfs = []
    
    # Mapeamento de colunas possíveis (O INMET muda o padrão conforme o ano)
    colunas_data = ['Data', 'DATA (YYYY-MM-DD)']
    colunas_chuva = ['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)', 'PRECIPITACAO TOTAL, HORARIO (mm)']

    for f in arquivos:
        try:
            # INMET usa latin-1 e pula as primeiras 8 linhas de metadados
            df = pd.read_csv(f, sep=';', encoding='latin-1', skiprows=8, decimal=',')
            
            # Identifica as colunas corretas dinamicamente
            col_dt = next((c for c in colunas_data if c in df.columns), None)
            col_prec = next((c for c in colunas_chuva if c in df.columns), None)

            if col_dt and col_prec:
                df_clean = df[[col_dt, col_prec]].copy()
                df_clean.columns = ['data_original', 'precipitacao']
                lista_dfs.append(df_clean)
            else:
                logging.warning(f"Colunas esperadas não encontradas no arquivo: {f.name}")

        except Exception as e:
            logging.error(f"Erro ao ler {f.name}: {e}")

    if lista_dfs:
        df_full = pd.concat(lista_dfs)
        # Converte para datetime tratando erros (alguns arquivos têm formatos váriados)
        df_full['data_dt'] = pd.to_datetime(df_full['data_original'], errors='coerce')
        df_full = df_full.dropna(subset=['data_dt'])
        
        # Cria a competência para o merge
        df_full['competencia'] = df_full['data_dt'].dt.strftime('%Y%m')

        # Agrupamento mensal: Soma da chuva RS
        clima_final = df_full.groupby('competencia')['precipitacao'].sum().reset_index()
        
        save_file = output_path / "clima_rs_mensal.csv"
        clima_final.to_csv(save_file, index=False)
        logging.info(f"Sucesso! Arquivo gerado em: {save_file}")

if __name__ == "__main__":
    processar_clima()