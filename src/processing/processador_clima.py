import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def processar_clima():
    # Localiza a raiz do projeto (2 níveis acima deste script)
    raiz = Path(__file__).resolve().parents[2]
    raw_path = raiz / "data/raw/inmet"
    output_path = raiz / "data/processed/clima"
    output_path.mkdir(parents=True, exist_ok=True)

    # Busca recursiva ignorando case (pega .csv e .CSV)
    arquivos = list(raw_path.rglob("*.[cC][sS][vV]"))
    
    if not arquivos:
        logging.error(f"Nenhum arquivo CSV encontrado em: {raw_path}")
        return

    lista_dfs = []
    colunas_data = ['Data', 'DATA (YYYY-MM-DD)']
    colunas_chuva = ['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)', 'PRECIPITACAO TOTAL, HORARIO (mm)']

    for f in arquivos:
        try:
            # INMET usa latin-1 e pula as primeiras 8 linhas
            df = pd.read_csv(f, sep=';', encoding='latin-1', skiprows=8, decimal=',')
            
            # Limpeza de colunas (strip para evitar espaços invisíveis)
            df.columns = df.columns.str.strip()

            col_dt = next((c for c in colunas_data if c in df.columns), None)
            col_prec = next((c for c in colunas_chuva if c in df.columns), None)

            if col_dt and col_prec:
                df_clean = df[[col_dt, col_prec]].copy()
                df_clean.columns = ['data_original', 'precipitacao']
                lista_dfs.append(df_clean)
            else:
                logging.warning(f"Colunas não encontradas em: {f.name}")

        except Exception as e:
            logging.error(f"Erro em {f.name}: {e}")

    if lista_dfs:
        df_full = pd.concat(lista_dfs)
        df_full['data_dt'] = pd.to_datetime(df_full['data_original'], errors='coerce')
        df_full = df_full.dropna(subset=['data_dt'])
        df_full['competencia'] = df_full['data_dt'].dt.strftime('%Y%m')

        # Agrupamento mensal: Soma da chuva RS
        clima_final = df_full.groupby('competencia')['precipitacao'].sum().reset_index()
        
        save_file = output_path / "clima_rs_mensal.csv"
        clima_final.to_csv(save_file, index=False)
        logging.info(f"✅ Clima processado: {len(clima_final)} meses consolidados.")

if __name__ == "__main__":
    processar_clima()