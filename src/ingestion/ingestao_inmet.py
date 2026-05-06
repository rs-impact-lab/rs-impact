import requests
import zipfile
import io
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def baixar_dados_inmet():
    raiz = Path(__file__).resolve().parents[2]
    base_raw_path = raiz / "data" / "raw" / "inmet"
    
    urls = {
        "2023": "https://portal.inmet.gov.br/uploads/dadoshistoricos/2023.zip",
        "2024": "https://portal.inmet.gov.br/uploads/dadoshistoricos/2024.zip",
        "2025": "https://portal.inmet.gov.br/uploads/dadoshistoricos/2025.zip"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Arch Linux; Linux x86_64) AppleWebKit/537.36"
    }

    for ano, url in urls.items():
        destino_ano = base_raw_path / ano
        destino_ano.mkdir(parents=True, exist_ok=True)

        logging.info(f"🛰️ Iniciando download de {ano}...")
        
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()

            logging.info(f"📦 Extraindo arquivos de {ano} em {destino_ano}...")
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(destino_ano)
            
            logging.info(f"✅ Ano {ano} concluído com sucesso.")

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Erro ao baixar {ano}: {e}")
        except zipfile.BadZipFile:
            logging.error(f"❌ O arquivo baixado de {ano} não é um ZIP válido.")

if __name__ == "__main__":
    baixar_dados_inmet()