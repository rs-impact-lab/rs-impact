import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def processar_caged():
    raiz = Path(__file__).resolve().parents[2]
    raw_path = raiz / "data/raw/caged/2023"
    output_path = raiz / "data/processed/caged"
    output_path.mkdir(parents=True, exist_ok=True)

    COL_UF = "UF"
    COL_COMPETENCIA = "Competência"
    COL_SALDO = "Saldos"
    FILTRO_UF = "RS"

    arquivos = list(raw_path.rglob("*.xlsx"))
    if not arquivos:
        logging.error(f"Nenhum arquivo .xlsx encontrado em: {raw_path}")
        return

    lista_dfs = []

    for f in arquivos:
        try:
            df = pd.read_excel(f, sheet_name=0, header=4)
            df.columns = df.columns.astype(str).str.strip()

            if COL_UF in df.columns:
                df_rs = df[df[COL_UF].astype(str).str.contains(FILTRO_UF, na=False)].copy()
                
                disponiveis = [c for c in [COL_COMPETENCIA, COL_SALDO] if c in df_rs.columns]
                df_rs = df_rs[disponiveis]
                
                lista_dfs.append(df_rs)
                logging.info(f"OK: {f.name} ({len(df_rs)} linhas)")
            else:
                logging.warning(f"UF não encontrada em {f.name}")

        except Exception as e:
            logging.error(f"Erro em {f.name}: {e}")

    if lista_dfs:
        df_final = pd.concat(lista_dfs, ignore_index=True)
        
        df_final[COL_COMPETENCIA] = (
            df_final[COL_COMPETENCIA]
            .astype(str)
            .str.replace(r"\D", "", regex=True)
            .str.zfill(6)
        )
        
        df_final["Ano"] = df_final[COL_COMPETENCIA].str[:4].astype(int)
        df_final["Mes"] = df_final[COL_COMPETENCIA].str[4:6].astype(int)

        save_file = output_path / "caged_rs_consolidado.csv"
        df_final.to_csv(save_file, index=False, encoding="utf-8-sig")
        logging.info(f"✅ CAGED processado! Dataset salvo em: {save_file}")

if __name__ == "__main__":
    processar_caged()