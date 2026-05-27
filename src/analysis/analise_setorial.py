import os
import re
import pandas as pd
from pathlib import Path

# Configuração de caminhos
RAIZ = Path(__file__).resolve().parents[2]
DIR_RAW_CAGED = RAIZ / "data" / "raw" / "caged"
DIR_OUTPUT = RAIZ / "data" / "processed" / "caged"
DIR_OUTPUT.mkdir(parents=True, exist_ok=True)

meses_map = {
    'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5,
    'junho': 6, 'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
}

def extrair_dados_setoriais():
    arquivos_xlsx = list(DIR_RAW_CAGED.rglob("*.xls*"))
    if not arquivos_xlsx:
        print("❌ Nenhum arquivo Excel encontrado.")
        return

    lista_final = []

    for caminho_arq in arquivos_xlsx:
        nome_arq = os.path.basename(caminho_arq).lower()
        match_data = re.search(r'([a-zç]+)(?:-de-|\s*|_|-)(\d{4})', nome_arq)
        if not match_data: continue

        mes_nome, ano_val = match_data.group(1), int(match_data.group(2))
        mes_val = meses_map.get(mes_nome)
        if not mes_val: continue

        try:
            xls = pd.ExcelFile(caminho_arq)
            aba_alvo = [s for s in xls.sheet_names if 'tabela 3' in s.lower() or 'tab3' in s.lower()]
            if not aba_alvo: continue

            df = pd.read_excel(caminho_arq, sheet_name=aba_alvo[0], header=None)

            for idx, row in df.iterrows():
                row_str = [str(x).lower() for x in row.values]
                
                if 'rio grande do sul' in row_str or '43' in row_str:
                    setores = ['Agropecuária', 'Indústria', 'Construção', 'Comércio', 'Serviços']
                    dados_setores = row.iloc[7:28].values
                    
                    saldos = [x for x in dados_setores if isinstance(x, (int, float)) and abs(x) > 1]
                    
                    for i, setor in enumerate(setores):
                        if i < len(saldos):
                            lista_final.append({
                                'Ano': ano_val,
                                'Mes': mes_val,
                                'Setor': setor,
                                'Saldo_Setorial': int(saldos[i])
                            })
                    break
        except Exception as e:
            print(f"⚠️ Erro em {nome_arq}: {e}")

    if lista_final:
        pd.DataFrame(lista_final).to_csv(DIR_OUTPUT / "caged_setorial_rs.csv", index=False, encoding='utf-8-sig')
        print("✅ Dados processados corretamente com valores absolutos.")
    else:
        print("❌ Falha ao extrair dados.")

if __name__ == "__main__":
    extrair_dados_setoriais()