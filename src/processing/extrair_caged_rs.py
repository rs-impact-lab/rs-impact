import os
import re
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Definição exata dos diretórios que o script utiliza
DIR_RAW_CAGED = BASE_DIR / "data" / "raw" / "caged"
DIR_PROCESSED = BASE_DIR / "data" / "processed" / "caged"

# Garante que o diretório de saída existe
DIR_PROCESSED.mkdir(parents=True, exist_ok=True)

print(f"🚀 Iniciando extração de dados do CAGED (RS)...")
print(f"📂 Buscando em: {DIR_RAW_CAGED}\n")

arquivos_excel = sorted(list(DIR_RAW_CAGED.rglob("*.xlsx")))

dados_consolidados = []

for arq in arquivos_excel:
    nome_arquivo = arq.name.lower()
    ano_busca = re.search(r"202\d", arq.as_posix())
    ano = ano_busca.group(0) if ano_busca else "Desconhecido"
    
    meses_pt = ["janeiro", "fevereiro", "marco", "março", "abril", "maio", "junho", 
                "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    mes = "Desconhecido"
    for m in meses_pt:
        if m in nome_arquivo:
            mes = m.replace("março", "marco")
            break

    print(f"📦 Processando: {ano}/{mes} -> {arq.name}")

    try:
        xls = pd.ExcelFile(arq)
        aba_alvo = [s for s in xls.sheet_names if 'tabela 3' in s.lower() or 'tab 3' in s.lower() or 'tab3' in s.lower()]
        
        if not aba_alvo:
            print(f"  ⚠️ Aba 'Tabela 3' não encontrada. Abas disponíveis: {xls.sheet_names}")
            continue
            
        df = pd.read_excel(arq, sheet_name=aba_alvo[0], header=None)
        
        linha_rs = None
        for idx, linha in df.iterrows():
            coluna_uf = str(linha.values[0]).strip().upper() if pd.notna(linha.values[0]) else ""
            coluna_uf_alt = str(linha.values[1]).strip().upper() if len(linha.values) > 1 and pd.notna(linha.values[1]) else ""
            coluna_nome = str(linha.values[2]).strip().lower() if len(linha.values) > 2 and pd.notna(linha.values[2]) else ""
            
            if coluna_uf == "RS" or coluna_uf_alt == "RS" or "rio grande do sul" in coluna_nome:
                linha_rs = linha.values
                break
                
        if linha_rs is not None:
            dados_limpos = [val for val in linha_rs if pd.notna(val)]
        
            numeros = [float(v) for v in dados_limpos if isinstance(v, (int, float)) or str(v).replace('.','',1).isdigit()]
            
            if len(numeros) >= 4:
                dados_consolidados.append({
                    "Ano": int(ano),
                    "Mes": mes,
                    "Valores_Identificados": numeros[:6]
                })
                print(f"  ✅ Dados do RS isolados com sucesso.")
            else:
                print(f"  ❌ Estrutura numérica inesperada na linha do RS: {dados_limpos}")
        else:
            print(f"  ❌ Linha do Rio Grande do Sul (RS) não foi localizada nesta aba.")
            
    except Exception as e:
        print(f"  💥 Erro crítico ao ler arquivo: {e}")

if dados_consolidados:
    df_caged_rs = pd.DataFrame(dados_consolidados)
    caminho_saida = DIR_PROCESSED / "caged_rs_raw_extracted.csv"
    df_caged_rs.to_csv(caminho_saida, index=False, encoding="utf-8")
    print(f"\n✨ Etapa concluída! Arquivo temporário de checagem salvo em: {caminho_saida}")
    print(df_caged_rs.head(15))
else:
    print("\n🚨 Falha: Nenhum dado do RS pôde ser extraído. Verifique os nomes das abas ou arquivos.")