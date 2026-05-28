![rs-impact](/docs/assets/banner.png)
# Economia RS Impact — Projeto de Análise de Dados

**Tema**: Estudo da resiliência econômica do Rio Grande do Sul pós-desastre de 2024, cruzando dados de emprego do CAGED com índices de chuva do INMET.

## Objetivo do Projeto

Analisar o impacto socioeconômico das enchentes históricas no Rio Grande do Sul (ocorridas em maio de 2024) por meio da resiliência do mercado de trabalho formal.

O projeto busca correlacionar índices pluviométricos extremos com a flutuação de empregos (admissões e desligamentos), estabelecendo uma linha do tempo (2023 como base, 2024 como evento e 2025 como recuperação) para identificar o *Lag Time* (tempo de resposta) e os setores econômicos mais afetados pela catástrofe.

## Estrutura do Projeto

**Plaintext**

```
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
├── docs/                   # Documentação detalhada, metadados e artigo final
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```

## Pipeline de Dados (Fluxo de Execução)

O projeto segue um fluxo clássico de ETL e análise de Big Data:

1. **Ingestão:** Coleta dos microdados do CAGED e relatórios pluviométricos.
2. **Transformação (Limpeza):** Filtragem geográfica (isolando o RS) e padronização das colunas temporais e setoriais.
3. **Agregação:** Concatenação dos dados de 2023, 2024 e 2025 em uma base unificada temporal.
4. **Enriquecimento:** Join dos dados econômicos com as métricas de chuva (mm acima da média).
5. **Análise e Visualização:** Extração de correlações estatísticas e geração dos artefatos visuais.

## Ferramentas e Tecnologias

* **Python 3:** Linguagem base do projeto.
* **Pandas / Numpy:** Manipulação e limpeza de dados tabulares em memória.
* **Apache Spark / PySpark:** Processamento distribuído para os volumes massivos de dados, se necessário.
* **Jupyter Notebook:** Ambiente de desenvolvimento interativo para exploração inicial.
* **Matplotlib / Seaborn:** Criação das visualizações e gráficos comparativos.
* **Openpyxl / Xlrd:** Leitura e conversão de formatos legados e modernos do Excel.

## Desenvolvimento e Produtibilidade (Uso de IA)

Este projeto adota práticas modernas de desenvolvimento de software, utilizando Inteligência Artificial Generativa (LLMs) como ferramenta de suporte e aumento de produtibilidade. 

O uso da tecnologia concentrou-se em:
* **Engenharia de Dados & Infraestrutura:** Auxílio na refatoração e otimização dos scripts de processamento distribuído (`PySpark`) e automações Python na camada de ETL.
* **Qualidade de Código:** Validação de padrões de clean code e apoio na organização arquitetural dos diretórios (`data/raw`, `data/processed`, `src/`).
* **Documentação:** Revisão técnica da documentação do pipeline e das especificações contidas nos arquivos de relatório.

A lógica de negócio, a arquitetura do pipeline de ingestão do INMET/CAGED, a execução dos modelos analíticos de correlação (*Lag Time*) e a tomada de decisões estatísticas basearam-se inteiramente nos requisitos e no desenvolvimento técnico dos autores humanos.

## Documentação Adicional

Para detalhes técnicos profundos e acesso à fundamentação teórica, consulte o diretório `/docs`:

* [`docs/datasets.md`](/docs/datasets.md): Dicionário de dados, mapeamento de colunas do CAGED e descritivo das fontes originais.
* [`docs/metodologia.md`](/docs/metodologia.md): Detalhamento estatístico, justificativas metodológicas e decisões de arquitetura do pipeline de dados.
* [`docs/resultados_consolidados.md`](/docs/resultados_consolidados.md): Síntese dos achados analíticos finais, abordando as correlações setoriais e o comportamento de  *lag time* .
* [`docs/trabalho_academico_rs_impact.pdf`](/docs/trabalho_academico_rs_impact.pdf): Documento consolidado da pesquisa acadêmica formatado conforme as normas da ABNT.

## Contribuidores

Este projeto foi desenvolvido como trabalho acadêmico para a disciplina de Big Data e Análise de Dados no Centro Universitário Estácio, Campus Aracaju (2026).

- Lucas Paiva Santos de Oliveira — @lucaspaiva-lp
- Rodrigo Moraes dos Santos — @RodrigoDevBack

### Orientação

- Prof. Max Castor Rodrigues Junior
