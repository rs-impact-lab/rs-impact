import pandas as pd
from pathlib import Path

raiz     = Path(__file__).resolve().parents[2]
pasta    = raiz / "data" / "raw" / "caged" / "2023"
arquivos = sorted(pasta.glob("*.xlsx"))

if not arquivos:
    print("❌ Nenhum xlsx encontrado em", pasta)
    exit()

f = arquivos[0]
print(f"📄 Arquivo: {f.name}")
print("=" * 70)

df_raw = pd.read_excel(f, sheet_name=0, header=None, nrows=15)
print("🔍 Primeiras 15 linhas brutas (sem header):\n")
for i, row in df_raw.iterrows():
    valores = [str(v)[:30] for v in row if str(v) != 'nan']
    if valores:
        print(f"  linha {i:02d}: {valores}")

print("\n" + "=" * 70)

print("\n🔎 Testando qual header_row encontra a coluna 'UF':\n")
for h in range(10):
    try:
        df = pd.read_excel(f, sheet_name=0, header=h, nrows=3)
        df.columns = df.columns.astype(str).str.strip()
        tem_uf = any("UF" == c.upper().strip() for c in df.columns)
        print(f"  header={h}: {list(df.columns[:6])}{'  ✅ TEM UF' if tem_uf else ''}")
    except Exception as e:
        print(f"  header={h}: ERRO — {e}")

print("\n" + "=" * 70)
print("\n📋 Abas disponíveis no arquivo:")
xls = pd.ExcelFile(f)
for s in xls.sheet_names:
    print(f"  • '{s}'")
