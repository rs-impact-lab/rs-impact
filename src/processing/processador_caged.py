
import re
import pandas as pd
from pathlib import Path
import logging
 
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
 
ANOS      = ["2023", "2024", "2025"]
FILTRO_UF = "RS"
 
MESES_PT = {
    "janeiro": 1,  "fevereiro": 2, "março": 3,   "marco": 3,
    "abril":   4,  "maio":      5, "junho":  6,   "julho":    7,
    "agosto":  8,  "setembro":  9, "outubro": 10,
    "novembro": 11, "dezembro": 12,
}
 
ABA_ALVO = "Tabela 3" 
 
 
def _competencia(mes_nome: str, ano: str) -> str | None:
    n = MESES_PT.get(mes_nome.lower().strip())
    return f"{ano}{n:02d}" if n else None
 
 
def _ler_xlsx(caminho: Path) -> pd.DataFrame | None:
    nome = caminho.name
    try:
        xls = pd.ExcelFile(caminho)
        if ABA_ALVO not in xls.sheet_names:
            logging.warning(f"[{nome}] Aba '{ABA_ALVO}' não encontrada. "
                            f"Abas: {xls.sheet_names}")
            return None
 
        raw = pd.read_excel(caminho, sheet_name=ABA_ALVO, header=None)
 
        grupo    = raw.iloc[4].fillna(method="ffill").astype(str).str.strip()
        subgrupo = raw.iloc[5].astype(str).str.strip()
 
        nomes = []
        for g, s in zip(grupo, subgrupo):
            if s and s not in ("nan", ""):
                nomes.append(f"{g} | {s}")
            else:
                nomes.append(g)
 
        df = raw.iloc[6:].copy()
        df.columns = nomes
        df = df.dropna(how="all")
 

        col_uf = next((c for c in df.columns if c.strip().upper() == "UF"), None)
        if col_uf is None:
            df.columns.values[0] = "UF"
            col_uf = "UF"
 
        df_rs = df[df[col_uf].astype(str).str.strip().str.upper() == FILTRO_UF].copy()
        if df_rs.empty:
            logging.warning(f"[{nome}] Nenhuma linha RS encontrada.")
            return None
 
        col_saldo = next(
            (c for c in df_rs.columns
             if "saldo" in c.lower() and "sem ajuste" in c.lower()),
            None
        )
        if col_saldo is None:
            logging.warning(f"[{nome}] Coluna de Saldo mensal não encontrada. "
                            f"Colunas disponíveis: {[c for c in df_rs.columns[:12]]}")
            return None
 
        m = re.search(r"([A-Za-zçÇãÃõÕáÁéÉíÍóÓúÚ]+)/(\d{4})", col_saldo)
        if not m:
            logging.warning(f"[{nome}] Não extraiu mês/ano de: '{col_saldo}'")
            return None
        competencia = _competencia(m.group(1), m.group(2))
        if not competencia:
            logging.warning(f"[{nome}] Mês desconhecido: '{m.group(1)}'")
            return None
 
        col_mun = next((c for c in df_rs.columns if "munic" in c.lower()), None)
 
        cols_manter = [col_uf]
        if col_mun:
            cols_manter.append(col_mun)
        cols_manter.append(col_saldo)
 
        df_out = df_rs[cols_manter].copy()
        df_out = df_out.rename(columns={col_uf: "UF", col_saldo: "Saldo_Mensal"})
        if col_mun:
            df_out = df_out.rename(columns={col_mun: "Municipio"})
 
        df_out["Saldo_Mensal"] = pd.to_numeric(
            df_out["Saldo_Mensal"].astype(str).str.replace(",", ".", regex=False),
            errors="coerce"
        )
        df_out = df_out.dropna(subset=["Saldo_Mensal"])
        df_out["Competencia"] = competencia
        df_out["Ano"] = int(competencia[:4])
        df_out["Mes"] = int(competencia[4:])
 
        logging.info(
            f"OK  {nome:<55} → {len(df_out):>4} municípios RS | "
            f"competência {competencia} | saldo RS = {df_out['Saldo_Mensal'].sum():+,.0f}"
        )
        return df_out
 
    except Exception as e:
        logging.error(f"[{nome}] Erro inesperado: {e}", exc_info=False)
        return None
 
 
def processar_caged():
    raiz        = Path(__file__).resolve().parents[2]
    raw_path    = raiz / "data" / "raw" / "caged"
    output_path = raiz / "data" / "processed" / "caged"
    output_path.mkdir(parents=True, exist_ok=True)
 
    arquivos: list[Path] = []
    for ano in ANOS:
        pasta = raw_path / ano
        if pasta.exists():
            arquivos += sorted(pasta.glob("*.xlsx"))
        else:
            logging.warning(f"Pasta não encontrada: {pasta}")
 
    if not arquivos:
        logging.error(f"Nenhum .xlsx encontrado em {raw_path}")
        return
 
    logging.info(f"📂 {len(arquivos)} arquivo(s) encontrados\n")
 
    lista_dfs = [r for f in arquivos if (r := _ler_xlsx(f)) is not None]
 
    if not lista_dfs:
        logging.error("Nenhum dado extraído. Verifique os avisos acima.")
        return
 
    df_final = pd.concat(lista_dfs, ignore_index=True).sort_values(["Ano", "Mes"])
 
    logging.info(f"\n{'='*60}")
    logging.info(f"✅ CAGED consolidado")
    logging.info(f"   Linhas        : {len(df_final):,}")
    logging.info(f"   Meses cobertos: {df_final['Competencia'].nunique()} "
                 f"({df_final['Competencia'].min()} → {df_final['Competencia'].max()})")
    logging.info(f"   Anos          : {sorted(df_final['Ano'].unique())}")
 
    logging.info("\nSaldo mensal RS (soma dos municípios):")
    for _, row in (
        df_final.groupby(["Competencia"])["Saldo_Mensal"]
        .sum().reset_index().sort_values("Competencia")
    ).iterrows():
        logging.info(f"   {row['Competencia']}  {row['Saldo_Mensal']:+10,.0f} postos")
 
    save_file = output_path / "caged_rs_consolidado.csv"
    df_final.to_csv(save_file, index=False, encoding="utf-8-sig")
    logging.info(f"\n💾 Salvo em: {save_file}")
    logging.info(f"{'='*60}")
 
 
if __name__ == "__main__":
    processar_caged()
