# Economia RS Impact — Projeto de Análise de Dados

## Participantes

* Lucas
* Rodrigo

---

# Estrutura do Projeto

```text
economia-rs-impact/
│
├── data/
│   ├── raw/
│   │   ├── caged/
│   │   ├── exportacoes/
│   │   └── agro/
│   │
│   └── processed/
│
├── notebooks/
│
├── src/
│   ├── ingestion/
│   ├── processing/
│   └── analysis/
│
├── outputs/
│   ├── tables/
│   └── charts/
│
├── docs/
│
├── requirements.txt
│
└── README.md
```

---

# Objetivo do Projeto

Este projeto tem como objetivo analisar o **impacto econômico das enchentes de 2024 no Rio Grande do Sul** utilizando datasets públicos e ferramentas de análise de dados como Python, Pandas e Apache Spark.

A análise será baseada em indicadores econômicos como:

* Emprego (CAGED)
* Exportações (ComexStat)
* Produção agrícola (IBGE PAM)

O objetivo é comparar **indicadores econômicos antes e depois do desastre**, além de comparar o Rio Grande do Sul com outros estados da região sul do Brasil.

---

# Explicação dos Diretórios

## `data/raw`

Contém os **datasets brutos exatamente como foram baixados** das fontes oficiais.

Esses arquivos **não devem ser modificados**.

Exemplo de estrutura:

```text
data/raw/caged/
data/raw/exportacoes/
data/raw/agro/
```

Finalidade:

* preservar os dados originais
* permitir reprodutibilidade
* evitar perda do dataset original

---

## `data/processed`

Contém **datasets limpos e transformados**, prontos para análise.

Operações comuns realizadas aqui:

* filtragem por estado
* remoção de colunas desnecessárias
* padronização de formatos
* junção de datasets

Exemplo:

```text
data/processed/emprego_rs.csv
data/processed/exportacoes_rs.csv
data/processed/agro_rs.csv
```

---

## `notebooks`

Ambiente de análise exploratória.

Utilizado para:

* exploração inicial dos dados
* testes rápidos
* criação de visualizações preliminares

Exemplo:

```text
notebooks/explore_caged.ipynb
notebooks/explore_exportacoes.ipynb
notebooks/analise_economia_rs.ipynb
```

---

## `src`

Contém o código principal do projeto.

### `src/ingestion`

Responsável por **carregar os datasets**.

Exemplos:

```text
load_caged.py
load_exportacoes.py
load_agro.py
```

Funções comuns:

* leitura de arquivos CSV
* leitura de arquivos XLS/XLSX
* carregamento inicial dos dados

---

### `src/processing`

Responsável pela **limpeza e transformação dos dados**.

Exemplos:

```text
clean_caged.py
clean_exportacoes.py
merge_datasets.py
```

Tarefas comuns:

* filtragem
* agregações
* junção de tabelas
* normalização de dados

---

### `src/analysis`

Contém scripts responsáveis pela **análise final dos dados**.

Exemplo:

```text
economia_rs_analysis.py
```

Possíveis análises:

* comparação de emprego antes vs depois da enchente
* comparação de exportações entre estados
* mudanças na produção agrícola

---

## `outputs`

Armazena os **resultados gerados pela análise**.

### Tabelas

```text
outputs/tables/emprego_por_estado.csv
outputs/tables/exportacoes_rs.csv
```

### Gráficos

```text
outputs/charts/emprego_rs.png
outputs/charts/exportacoes_rs.png
```

---

## `docs`

Documentação do projeto.

Possíveis arquivos:

```text
docs/metodologia.md
docs/datasets.md
```

Esses documentos podem explicar:

* origem dos datasets
* metodologia de processamento
* explicação da análise

---

## `requirements.txt`

Lista das dependências Python utilizadas no projeto.

Exemplo:

```text
pandas
numpy
matplotlib
pyspark
jupyter
```

---

# Pipeline de Dados

Fluxo esperado do projeto:

```text
Datasets públicos
      ↓
Download
      ↓
data/raw
      ↓
Limpeza e transformação dos dados
      ↓
data/processed
      ↓
Análise de dados (Pandas / Spark)
      ↓
outputs (tabelas e gráficos)
      ↓
Relatório final
```

---

# Ferramentas Utilizadas

Principais tecnologias envolvidas no projeto:

* Python
* Pandas
* Apache Spark
* Jupyter Notebook / Google Colab
* Datasets em formato CSV

Essas ferramentas serão utilizadas para processamento, análise e visualização de dados.

---

# Resultado Esperado

O projeto deverá gerar:

* datasets processados
* scripts de análise
* visualizações (gráficos e tabelas)
* conclusões sobre o impacto econômico das enchentes no Rio Grande do Sul
