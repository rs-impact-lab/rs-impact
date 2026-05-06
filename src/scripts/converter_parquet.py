import pandas as pd
import os
from pathlib import Path
import warnings
import re
import numpy as np

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

def limpar_nome_coluna(col):
    if not col or "Unnamed" in str(col):
        return ""
    s = str(col).strip().lower()
    s = re.sub(r'[^\w\s]', '', s)
    s = re.sub(r'\s+', '_', s)
    return s

def tratar_e_converter():
    raiz = Path(__file__).resolve().parents[2]
    input_base = raiz / "data" / "raw" / "caged"
    output_base = raiz / "data" / "processed" / "caged-parquet"

    anos = ["2023", "2024", "2025"]

    for ano in anos:
        input_dir = input_base / ano
        output_dir = output_base / ano
        
        if not input_dir.exists():
            continue
            
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n📅 Processando ano: {ano}")

        for arquivo in input_dir.glob("*.xlsx"):
            print(f"📖 Lendo: {arquivo.name}")
            
            try:
                xl = pd.ExcelFile(arquivo)
                
                for aba in xl.sheet_names:
                    if aba in ['Sumário', 'CAGED']:
                        continue

                    df = pd.read_excel(xl, sheet_name=aba, header=[4, 5])

                    novas_cols = []
                    for col in df.columns:
                        p1 = limpar_nome_coluna(col[0])
                        p2 = limpar_nome_coluna(col[1])
                        nome_final = f"{p1}_{p2}".strip("_")
                        if not nome_final:
                            nome_final = f"coluna_{len(novas_cols)}"
                        novas_cols.append(nome_final)
                    
                    df.columns = novas_cols

                    df = df.dropna(how='all').reset_index(drop=True)
                    if df.empty:
                        continue
                    
                    df = df.dropna(subset=[df.columns[1]], thresh=1)
                    
                    col_uf = [c for c in df.columns if 'uf' in c]
                    if col_uf:
                        df = df[df[col_uf[0]].astype(str).str.contains('RS|Rio Grande', case=False, na=False)]

                    if df.empty:
                        continue

                    for col in df.columns:
                        df[col] = df[col].astype(str).replace(['---', '--', '-', 'nan', 'None', ''], '0')
                        
                        temp_numeric = pd.to_numeric(df[col], errors='coerce')
                        
                        if temp_numeric.notna().sum() > (len(df) * 0.5):
                            df[col] = temp_numeric.fillna(0)
                        else:
                            df[col] = df[col].str.replace(r'\.0$', '', regex=True)

                    nome_limpo_aba = aba.replace(" ", "_").lower()
                    nome_saida = f"{arquivo.stem}_{nome_limpo_aba}.parquet"
                    
                    df.to_parquet(output_dir / nome_saida, index=False, compression='snappy', engine='pyarrow')
                    print(f"   ✅ Aba '{aba}' -> {nome_saida}")

            except Exception as e:
                print(f"   ❌ Erro ao processar {arquivo.name}: {e}")

if __name__ == "__main__":
    tratar_e_converter()