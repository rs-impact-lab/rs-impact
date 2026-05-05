import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def processar_caged():
    raw_path = Path("data/raw/caged")
    output_path = Path("data/processed/caged")
    output_path.mkdir(parents=True, exist_ok=True)

    # Configurações baseadas na exploração[cite: 1]
    COL_UF = "UF"
    COL_COMPETENCIA = "Competência"
    COL_SALDO = "Saldos"
    FILTRO_UF = "RS"

    arquivos = list(raw_path.rglob("*.xlsx"))
    lista_dfs = []

    for f in arquivos:
        try:
            # header=4 pula as linhas de título do Ministério do Trabalho[cite: 1]
            df = pd.read_excel(f, sheet_name=0, header=4)
            
            # Limpeza de nomes de colunas (remove espaços extras)
            df.columns = df.columns.astype(str).str.strip()

            if COL_UF in df.columns:
                # Filtra apenas RS
                df_rs = df[df[COL_UF].astype(str).str.contains(FILTRO_UF, na=False)].copy()
                
                # Mantém colunas essenciais
                cols_to_keep = [c for c in [COL_COMPETENCIA, COL_SALDO] if c in df_rs.columns]
                df_rs = df_rs[cols_to_keep]
                
                lista_dfs.append(df_rs)
                logging.info(f"Processado {f.name}: {len(df_rs)} registros encontrados.")
            else:
                logging.warning(f"Coluna {COL_UF} não encontrada em {f.name}")

        except Exception as e:
            logging.error(f"Erro ao processar {f.name}: {e}")

    if lista_dfs:
        df_final = pd.concat(lista_dfs, ignore_index=True)
        
        # Formatação da Competência e geração das colunas para merge
        df_final[COL_COMPETENCIA] = df_final[COL_COMPETENCIA].astype(str).str.replace(r"\D", "", regex=True).str.zfill(6)
        
        # Garante que temos as colunas para o Notebook 03[cite: 1]
        df_final["Ano"] = df_final[COL_COMPETENCIA].str[:4].astype(int)
        df_final["Mes"] = df_final[COL_COMPETENCIA].str[4:6].astype(int)

        save_file = output_path / "caged_rs_consolidado.csv"
        df_final.to_csv(save_file, index=False, encoding="utf-8-sig")
        logging.info(f"Sucesso! Dataset CAGED pronto em: {save_file}")

if __name__ == "__main__":
    processar_caged()