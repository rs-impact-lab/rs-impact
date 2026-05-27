# Metodologia e Arquitetura do Projeto

Este documento descreve as decisões técnicas, a arquitetura de software e os procedimentos estatísticos utilizados para analisar o impacto socioeconômico das enchentes históricas no Rio Grande do Sul sobre a resiliência do mercado de trabalho formal^^.

## 1. Decisões de Arquitetura

### 1.1. Estrutura de Diretórios (Modularização)

A arquitetura do projeto opera sobre um pipeline ETL (Extract, Transform, Load) segmentado para garantir reprodutibilidade e escalabilidade^^:

* **`data/raw/` vs `data/processed/`:** Princípio da imutabilidade. Os dados originais brutos não são alterados; o processamento gera arquivos consolidados nos formatos CSV e Apache Parquet^^.
* **`src/processing/` e `src/analysis/`:** Separação entre os scripts de ingestão/transformação e os scripts responsáveis pela análise estatística e geração de gráficos^^.

### 1.2. Stack Tecnológica

* **Python 3.12:** Linguagem base utilizada para o desenvolvimento do pipeline de processamento e das análises^^. O ambiente foi executado e homologado em sistemas Linux (Arch Linux/EndeavourOS).
* **Pandas e SciPy:** Bibliotecas utilizadas para a manipulação dos microdados e para a implementação das análises de correlação matemática^^.
* **Apache Parquet:** Formato de armazenamento adotado para a otimização de leitura dos dados consolidados^^.

## 2. Metodologia Estatística

O recorte temporal abrange o período de agosto de 2023 a dezembro de 2025, totalizando **$n=25$** observações mensais^^. A análise estruturou-se em três fases:

### 2.1. Análise de Sazonalidade (Baseline)

* **2023:** Estabelecido como linha de base de normalidade sazonal do estado^^.
* **2024:** Definido como o período crítico, com ênfase analítica no mês de maio^^.
* **2025:** Monitorado como a fase de recuperação observada do mercado^^.

### 2.2. Cálculo de Correlação (Chuva vs. Emprego)

A relação entre precipitação mensal (variável independente) e saldo de empregos (variável dependente) foi mensurada matematicamente^^:

* Foram utilizados os coeficientes de correlação de Pearson e Spearman^^.
* O limiar de significância estatística adotado foi **$p<0,05$** para rejeição da hipótese nula, com indicação de tendência marginal para **$p<0,10$**^^.

### 2.3. Identificação do *Lag Time* (Tempo de Resposta)

Para capturar a dinâmica não instantânea do mercado de trabalho, a análise econométrica aplicou defasagens temporais:

* Foram testadas análises contemporâneas (sem defasagem) e com defasagens de um, dois e três meses^^.
* A maior correlação estatística foi identificada com a defasagem de três meses (**$r=+0,3772$**; **$p=0,0836$**), configurando uma tendência marginal^^.

## 3. Fluxo de Processamento (Pipeline ETL)

O tratamento dos dados seguiu as seguintes etapas de consolidação^^:

* **Extração:** Captura dos arquivos XLSX mensais do Cadastro Geral de Empregados e Desempregados (CAGED) e dos arquivos CSV do Instituto Nacional de Meteorologia (INMET)^^.
* **Transformação e Padronização:** Filtragem exclusiva para o estado do Rio Grande do Sul (código UF 43) e agregação mensal da precipitação pluviométrica por estação meteorológica^^.
* **Consolidação:** Geração de dois arquivos analíticos principais: `caged_vs_clima_rs.csv` (série agregada) e `caged_setorial_rs.csv` (decomposição por setor econômico)^^.

## 4. Limitações Conhecidas

* **Restrição Amostral:** O tamanho reduzido da série temporal (**$n=25$** meses) limita o poder estatístico das análises de correlação, impedindo a rejeição formal da hipótese nula em determinados cenários^^.
* **Subnotificação:** O CAGED registra apenas as movimentações do mercado formal. O impacto sobre trabalhadores informais e autônomos não é mensurado por este conjunto de dados.
* **Disponibilidade e Continuidade:** Eventuais falhas de manutenção ou avarias em estações meteorológicas durante eventos extremos podem gerar lacunas na coleta contínua de índices pluviométricos.
