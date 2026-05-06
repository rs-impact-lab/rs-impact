import pandas as pd
import sys
from pathlib import Path

def inspecionar_xlsx(caminho):
    xlsx = pd.ExcelFile(caminho)
    print(f"🔍 Arquivo: {caminho}")
    print(f"📋 Abas encontradas: {xlsx.sheet_names}")
    
    for aba in xlsx.sheet_names:
        print(f"\n{'-'*50}")
        print(f"📊 ANALISANDO ABA: {aba}")
        df = pd.read_excel(xlsx, sheet_name=aba, header=4)
        
        print("\n--- Primeiras 5 colunas encontradas: ---")
        print(df.columns.tolist()[:5])
        
        print("\n--- Tipos de dados (Dtypes): ---")
        print(df.dtypes.head())
        
        print("\n--- Amostra dos dados (3 linhas): ---")
        print(df.head(3))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspecionar_xlsx(sys.argv[1])
    else:
        print("Uso: python src/analysis/diagnostico_xlsx.py caminho/do/arquivo.xlsx")