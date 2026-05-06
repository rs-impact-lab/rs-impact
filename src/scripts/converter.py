import pandas as pd
import sys
import os

def converter_para_csv(arquivo_entrada):
    if not os.path.exists(arquivo_entrada):
        print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
        return

    extensao = os.path.splitext(arquivo_entrada)[1].lower()
    nome_base = os.path.splitext(arquivo_entrada)[0]

    try:
        print(f"Lendo arquivo {extensao}...")
        
        excel_file = pd.ExcelFile(arquivo_entrada)
        abas_nomes = excel_file.sheet_names

        for nome_aba in abas_nomes:

            df = pd.read_excel(arquivo_entrada, sheet_name=nome_aba, header=[4, 5])

            df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')

            if df.empty:
                print(f"⚠️ Pulando aba vazia: {nome_aba}")
                continue

            novos_nomes = []
            for col in df.columns:
                nivel_0 = str(col[0]) if "Unnamed" not in str(col[0]) else ""
                nivel_1 = str(col[1]) if "Unnamed" not in str(col[1]) else ""
                
                nome_final = f"{nivel_0} {nivel_1}".strip()

                if not nome_final or "Coluna_Sem_Nome" in nome_final:
                    nome_final = "Região e UF"
                
                novos_nomes.append(nome_final)

            df.columns = novos_nomes

            df.columns = [" ".join(str(c).split()) for c in df.columns]
            
            df = df.reset_index(drop=True)


            arquivo_saida_aba = f"{nome_base}_{nome_aba.replace(' ', '_')}.csv"
            df.to_csv(arquivo_saida_aba, index=False, encoding='utf-8-sig')
            print(f"✅ Aba '{nome_aba}' corrigida 100%: {arquivo_saida_aba}")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python converter.py nome_do_arquivo.xlsx")
    else:
        converter_para_csv(sys.argv[1])