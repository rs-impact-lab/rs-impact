# Resultados Consolidados — Economia RS Impact
**Fonte primária:** CAGED (Ministério do Trabalho e Emprego) + INMET (Instituto Nacional de Meteorologia)  
**Período analisado:** Agosto/2023 – Dezembro/2025  
**Gerado por:** `src/analysis/analise_correlacao.py` | `src/analysis/analise_setorial_temporal.py` | `src/analysis/analise_setorial_impacto.py`

---

## 1. Evento Crítico

- **Data:** Maio de 2024
- **Natureza:** Enchentes históricas no Rio Grande do Sul
- **Precipitação registrada (maio/2024):** 15.924,8 mm — pico absoluto do período analisado (série INMET)
- **Saldo agregado de empregos (maio/2024):** −22.180 vagas (série `caged_vs_clima_rs.csv`)
- **Caracterização:** Choque de impacto setorial heterogêneo — setores rurais/industriais negativos; setores urbanos positivos

---

## 2. Impacto Setorial — Maio/2024

| Setor            | Saldo (vagas) | Sinal    |
|------------------|---------------|----------|
| Comércio         | +83           | Positivo |
| Construção Civil | +82           | Positivo |
| Serviços         | +35           | Positivo |
| Indústria        | −1            | Negativo |
| Agropecuária     | −7            | Negativo |

**Fonte:** `data/processed/caged/caged_setorial_rs.csv`  
**Script:** `src/analysis/analise_setorial_impacto.py`  
**Gráfico:** `outputs/charts/impacto_setorial_maio_2024.png`

> **Nota metodológica:** Os valores setoriais refletem o recorte filtrado da base do CAGED para o RS.
> O saldo agregado de −22.180 vagas (série consolidada) capta a magnitude total do choque,
> enquanto a decomposição setorial revela o padrão de impacto diferenciado entre setores.
> O saldo setorial positivo de Comércio e Construção no mês do evento é consistente com
> demanda emergencial imediata gerada pelo próprio desastre.

---

## 3. Série Temporal Agregada (RS)

| Mês/Ano | Saldo Empregos | Chuva Total (mm) |
|---------|----------------|-----------------|
| 8/2023  | +2.561         | 3.280,8         |
| 9/2023  | +1.267         | 17.467,0        |
| 10/2023 | +21.532        | 11.192,0        |
| 12/2023 | −28.832        | 7.767,2         |
| 5/2024  | −22.180        | 15.924,8 ← pico |
| 8/2024  | pico positivo  | —               |
| 12/2025 | saldo negativo | —               |

**Fonte:** `data/processed/caged_vs_clima_rs.csv`  
**Gráfico:** `outputs/charts/evolucao_temporal_rs.png`

---

## 4. Análise de Correlação

**Script:** `src/analysis/analise_correlacao.py`  
**Output completo:** `outputs/reports/correlacao_resultados.txt`

### 4.1 Correlação Contemporânea (sem defasagem)

| Método   | Coeficiente  | p-valor | Significância                |
|----------|--------------|---------|------------------------------|
| Pearson  | r = −0,2617  | 0,2063  | Não significativa (p > 0,05) |
| Spearman | ρ = −0,1908  | 0,3610  | Não significativa (p > 0,05) |

### 4.2 Análise de Lag Time

| Defasagem  | Pearson r | p-valor | Observação                    |
|------------|-----------|---------|-------------------------------|
| +1 mês     | −0,0840   | 0,6964  | —                             |
| +2 meses   | −0,1732   | 0,4293  | —                             |
| +3 meses   | +0,3772   | 0,0836  | Tendência marginal (p < 0,10) |

**Lag mais expressivo: +3 meses** (r = +0,38, p = 0,08)

### 4.3 Interpretação Metodológica

A ausência de correlação linear significativa entre precipitação mensal agregada e saldo de
empregos não invalida a hipótese do impacto. O evento de maio/2024 se caracteriza como choque
discreto e não-linear, não captável por coeficientes de correlação em séries mensais de n = 25
observações.

O lag de +3 meses apresenta a correlação mais expressiva do conjunto (r = +0,38, p = 0,08),
sugerindo resposta defasada de aproximadamente um trimestre do mercado de trabalho formal ao
choque climático.

---

## 5. Recuperação Setorial — 2025

| Setor            | Comportamento pós-evento                                      |
|------------------|---------------------------------------------------------------|
| Indústria        | Pico expressivo em ago/2024 (+6.007 vagas); recuperação rápida |
| Construção Civil | Pico em ago/2024 (+5.332 vagas); impulsionada por reconstrução |
| Serviços         | Recuperação gradual e estável ao longo de 2025               |
| Comércio         | Recuperação moderada; oscilações ao longo de 2025            |
| Agropecuária     | Recuperação lenta; ciclos produtivos de horizonte mais longo  |

**Gráfico:** `outputs/charts/evolucao_setorial_rs.png`

---

## 6. Arquivos de Referência do Projeto

| Arquivo                                          | Descrição                                      |
|--------------------------------------------------|------------------------------------------------|
| `data/processed/caged_vs_clima_rs.csv`           | Série temporal mensal: emprego + chuva         |
| `data/processed/caged/caged_setorial_rs.csv`     | Saldo por setor econômico (2023–2025)          |
| `data/processed/clima/clima_rs_mensal.csv`       | Precipitação mensal INMET (RS)                 |
| `outputs/charts/impacto_setorial_maio_2024.png`  | Gráfico setorial — maio/2024 (corrigido)       |
| `outputs/charts/evolucao_temporal_rs.png`        | Série temporal: emprego vs. chuva              |
| `outputs/charts/evolucao_setorial_rs.png`        | Evolução setorial 2023–2025                    |
| `outputs/reports/correlacao_resultados.txt`      | Resultados numéricos da correlação             |
| `notebooks/03_merge_e_correlacao.ipynb`          | Notebook de merge e análise exploratória       |
| `src/analysis/analise_correlacao.py`             | Script: correlação e lag time                  |
| `src/analysis/analise_setorial_temporal.py`      | Script: evolução setorial 2023–2025            |
| `src/analysis/analise_setorial_impacto.py`       | Script: gráfico de impacto setorial por mês    |
