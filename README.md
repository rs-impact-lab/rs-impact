# Economia RS Impact — Projeto de Análise de Dados

Tema: Estudo da resiliência econômica do Rio Grande do Sul pós-desastre de 2024, cruzando dados de emprego do CAGED com índices de chuva do INMET.

## Objetivo do Projeto

Analisar o impacto socioeconômico das enchentes históricas no Rio Grande do Sul (ocorridas em maio de 2024) por meio da resiliência do mercado de trabalho formal. 

O projeto busca correlacionar índices pluviométricos extremos com a flutuação de empregos (admissões e desligamentos), estabelecendo uma linha do tempo (2023 como base, 2024 como evento e 2025 como recuperação) para identificar o *Lag Time* (tempo de resposta) e os setores econômicos mais afetados pela catástrofe.

---

## Estrutura do Projeto

```text
rs-impact/
├── data/
│   ├── raw/                # Dados originais não modificados (CAGED, INMET, DEE-RS)
│   └── processed/          # Dados limpos e padronizados gerados pelos scripts
│
├── src/                    # Código-fonte principal
│   ├── ingestion/          # Scripts de download ou extração automatizada
│   ├── processing/         # Scripts de limpeza e conversão (ex: converter.py)
│   ├── analysis/           # Scripts de análise estatística e agregação
│   └── mapreduce_engine/   # Scripts de processamento distribuído (MRJob)
│
├── notebooks/              # Jupyter Notebooks para exploração e testes rápidos
│
├── outputs/                # Resultados gerados pela análise
│   ├── charts/             # Gráficos (PNG, PDF)
│   └── reports/            # Relatórios em texto e sumarizações (TXT, CSV finais)
│
├── docs/                   # Documentação detalhada e metadados
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```
---

## Pipeline de Dados (Fluxo de Execução)

O projeto segue um fluxo clássico de ETL e análise de Big Data:

1. **Ingestão:** Coleta dos microdados do CAGED e relatórios pluviométricos.
2. **Transformação (Limpeza):** Filtragem geográfica (isolando o RS) e padronização das colunas temporais e setoriais.
3. **Agregação:** Concatenação dos dados de 2023, 2024 e 2025 em uma base unificada temporal.
4. **Enriquecimento:** Join dos dados econômicos com as métricas de chuva (mm acima da média).
5. **Análise e Visualização:** Extração de correlações estatísticas e geração dos artefatos visuais.

---

## Ferramentas e Tecnologias

* **Python 3:** Linguagem base do projeto.
* **Pandas / Numpy:** Manipulação e limpeza de dados tabulares em memória.
* **Apache Spark / PySpark:** Processamento distribuído para os volumes massivos de dados, se necessário.
* **Jupyter Notebook:** Ambiente de desenvolvimento interativo para exploração inicial.
* **Matplotlib / Seaborn:** Criação das visualizações e gráficos comparativos.
* **Openpyxl / Xlrd:** Leitura e conversão de formatos legados e modernos do Excel.

---

## Resultados Esperados

O projeto deverá gerar, ao final do fluxo:

* Datasets unificados, limpos e otimizados prontos para consultas.
* Scripts automatizados e reutilizáveis para análise de séries temporais.
* Visualizações gráficas que comprovem ou refutem a correlação direta entre o volume de chuvas e a queda de postos de trabalho em setores específicos.

---

## Documentação Adicional

Para detalhes técnicos profundos, consulte o diretório `/docs`:

* [`docs/datasets.md`](/docs/datasets.md): Dicionário de dados, mapeamento de colunas do CAGED e fontes originais.
* [`docs/metodologia.md`](/docs/metodologia.md): Detalhamento estatístico e decisões de arquitetura do código.
