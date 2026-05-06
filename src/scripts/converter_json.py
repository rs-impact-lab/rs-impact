import pandas as pd
import json
import warnings
import logging
from pathlib import Path

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def excel_para_json_multi():
    raiz = Path(__file__).resolve().parents[2]
    input_path = raiz / "data" / "raw" / "caged"
    output_path = raiz / "data" / "processed" / "caged_json"
    output_path.mkdir(parents=True, exist_ok=True)

    arquivos_xlsx = list(input_path.rglob("*.xlsx"))

    if not arquivos_xlsx:
        logging.warning("⚠️ Nenhum arquivo .xlsx encontrado em data/raw/caged")
        return

    for caminho_xlsx in arquivos_xlsx:
        try:
            logging.info(f"📂 Processando: {caminho_xlsx.name}")
            
            xlsx = pd.ExcelFile(caminho_xlsx, engine='openpyxl')
            dict_tabelas = {}

            for nome_aba in xlsx.sheet_names:
                logging.info(f"  📖 Lendo aba: {nome_aba}")
                df = pd.read_excel(xlsx, sheet_name=nome_aba, header=4)
                
                df = df.dropna(how='all')
                
                dict_tabelas[nome_aba] = df.to_dict(orient="records")

            nome_arquivo = caminho_xlsx.stem + ".json"
            caminho_final = output_path / nome_arquivo
            
            with open(caminho_final, "w", encoding="utf-8") as f:
                json.dump(dict_tabelas, f, ensure_ascii=False, indent=2)
            
            logging.info(f"✅ Sucesso: {nome_arquivo}")

        except Exception as e:
            logging.error(f"❌ Falha em {caminho_xlsx.name}: {e}")

if __name__ == "__main__":
    excel_para_json_multi()