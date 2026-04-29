# Metodologia e Arquitetura do Projeto

Este documento descreve as decisões técnicas, a arquitetura de software e os critérios estatísticos utilizados para analisar o impacto das chuvas no RS.

## 1. Decisões de Arquitetura

### 1.1. Estrutura de Diretórios (Modularização)

Optamos por uma estrutura separada por responsabilidades para garantir a escalabilidade:

* **`data/raw` vs `data/processed`:** Princípio da Imutabilidade. Os dados originais nunca são alterados. Toda limpeza gera um novo arquivo, evitando a corrupção da fonte primária.
* **`src/` vs `notebooks/`:** Notebooks são usados para  **descoberta e prototipagem** . Scripts Python em `src/` são usados para  **produção e automação** .

### 1.2. Stack Tecnológica

* **Pandas:** Escolhido pela eficiência em manipulação de matrizes e facilidade de filtros em séries temporais.
* **Python 3.12:** Utilização de *f-strings* e melhorias de performance em ambientes Linux (Arch Linux).
* **Ambiente Virtual (`.venv`):** Isolamento de dependências para evitar conflitos de versões (ex: `openpyxl` vs `pandas`).

---

## 2. Metodologia Estatística

Para medir o "impacto", não basta olhar para 2024. Utilizamos três abordagens:

### 2.1. Análise de Sazonalidade (Baseline)

O mercado de trabalho tem ciclos (ex: contratações de fim de ano). Usamos os dados de **2023** para estabelecer o comportamento "normal" do estado.

* **Cálculo:** `Média_Mensal_2023` vs `Mês_Real_2024`.

### 2.2. Cálculo de Correlação (Chuva vs Emprego)

Utilizaremos o Coeficiente de Correlação de Pearson para medir a força da relação entre:

* **Variável X:** Precipitação acumulada (mm) acima da média histórica.
* **Variável Y:** Saldo líquido de empregos (Admissões - Desligamentos).

### 2.3. Identificação do *Lag Time*

Hipótese de que o impacto no emprego não é instantâneo à queda da chuva, mas apresenta um atraso de 30 a 60 dias devido ao tempo de fechamento de folhas de pagamento e processos rescisórios.

---

## 3. Fluxo de Processamento (Pipeline Técnico)

1. **Normalização de Tipagem:** Conversão de colunas numéricas de `string` para `int64` para permitir cálculos matemáticos.
2. **Tratamento de Nulos:** Aplicação de `fillna(0)` em colunas de saldo para não enviesar a média.
3. **Filtragem de Outliers:** Identificação de municípios com movimentações atípicas que possam distorcer a visão estadual.
4. **Join Temporal:** União das bases de Clima e Emprego através da chave composta `[Ano, Mês]`.

---

## 4. Limitações Conhecidas

* **Subnotificação:** O CAGED registra apenas o mercado formal. Impactos no trabalho informal (autônomos) não são capturados nesta análise.
* **Dados Geográficos:** Algumas estações meteorológicas podem sofrer avarias durante enchentes, gerando lacunas que serão tratadas via interpolação linear.
* **Disponibilidade:** Advindo do tempo e da manuteção, alguns links encontra-se indisponivel. Sendo assim, alguns meses de alguns respectivos anos estão com falta de dados.
