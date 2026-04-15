# Dicionário de Dados e Fontes (Datasets)

Este documento detalha a origem, a estrutura e o mapeamento dos dados utilizados no projeto  **Economia RS Impact** .

## 1. CAGED (Cadastro Geral de Empregados e Desempregados)

Os dados do CAGED são a base para medir a movimentação do mercado de trabalho formal (CLT).

* **Fonte:** [Portal Novo CAGED - Ministério do Trabalho e Emprego](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/novo-caged/meses-anteriores)
* **Frequência:** Mensal.
* **Granularidade:** Estadual e Municipal.

### Mapeamento de Colunas (Tabela 3 - Estaduais)

Devido à instabilidade nos nomes das colunas entre diferentes meses/tabelas, utilizamos o seguinte mapeamento para normalização:

| Nome Original (Exemplo)                  | Nome Normalizado    | Descrição                                         |
| ---------------------------------------- | ------------------- | --------------------------------------------------- |
| `UF`ou `Unidade da Federação`      | `uf`              | Sigla do Estado (Foco: RS)                          |
| `Saldos`ou `Saldo`                   | `saldo_empregos`  | Diferença entre Admissões e Desligamentos         |
| `Admissões`                           | `admissoes`       | Total de contratações no período                 |
| `Desligamentos`                        | `desligamentos`   | Total de demissões no período                     |
| `Grupamento de Atividades Econômicas` | `setor_economico` | Categoria do trabalho (Indústria, Comércio, etc.) |

---

## 2. Dados Climáticos (INMET)

Dados utilizados para correlacionar o volume de chuvas com os impactos econômicos.

* **Fonte:** [INMET - Instituto Nacional de Meteorologia](https://portal.inmet.gov.br/dadoshistoricos)
* **Dataset:** Séries Históricas de Estações Meteorológicas (RS).
* **Métricas principais:** Precipitação Total (mm).

### Estrutura de Dados

* **Data:** Data da medição (YYYY-MM-DD).
* **Precipitação Total (mm):** Volume de chuva acumulado.
* **Estação:** Nome ou Código da estação no RS (Ex: Porto Alegre, Bento Gonçalves).

---

## 3. Metodologia de Filtro e Limpeza

### Estratégia "RS-Only"

Para otimizar o processamento (Big Data), aplicamos um filtro inicial no carregamento dos dados:

1. **Filtro por UF:** Apenas linhas onde a coluna de estado contém o termo `RS`.
2. **Conversão de Tipos:** Colunas de movimentação econômica são forçadas para `int64` para evitar erros de cálculo com strings.
3. **Encoding:** Todos os arquivos são lidos/salvos em `utf-8-sig` para preservar a acentuação padrão brasileira.

---

### Notas Técnicas:

> **TODO:** Validar se a coluna `Município` está presente em todos os arquivos da `Tabela 3` caso decidamos fazer uma análise por cidade (Ex: Canoas vs Porto Alegre).
> **FIXME:** Alguns arquivos de 2024 podem vir com delimitador `;` em vez de `,`. O `converter.py` deve tratar isso.
>
