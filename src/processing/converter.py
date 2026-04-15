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
            # 1. Lemos sem pular linhas primeiro para capturar o cabeçalho completo.
            # Usamos as linhas 4 e 5 (que no Excel são onde ficam os títulos).
            df = pd.read_excel(arquivo_entrada, sheet_name=nome_aba, header=[4, 5])

            # 2. Limpeza de bordas.
            df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')

            if df.empty:
                print(f"⚠️ Pulando aba vazia: {nome_aba}")
                continue

            # Vamos achatar o cabeçalho duplo. 
            # Se a parte de cima for 'Unnamed', usamos a de baixo. Se a de baixo for 'Unnamed', usamos a de cima.
            novos_nomes = []
            for col in df.columns:
                nivel_0 = str(col[0]) if "Unnamed" not in str(col[0]) else ""
                nivel_1 = str(col[1]) if "Unnamed" not in str(col[1]) else ""
                
                # Se ambos existem, combinamos (ex: Dezembro_Admissões).
                # Se só um existe, usamos ele.
                nome_final = f"{nivel_0} {nivel_1}".strip()
                
                # Caso especial para a primeira coluna que você mostrou na imagem.
                if not nome_final or "Coluna_Sem_Nome" in nome_final:
                    nome_final = "Região e UF"
                
                novos_nomes.append(nome_final)

            df.columns = novos_nomes

            # Limpeza final nos nomes (remover espaços duplos e quebras de linha).
            df.columns = [" ".join(str(c).split()) for c in df.columns]
            
            # Resetar o index para garantir que não temos lixo.
            df = df.reset_index(drop=True)

            # Salva o CSV.
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