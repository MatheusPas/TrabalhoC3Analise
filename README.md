# Hackathon — Analisando Dados de Preços de Casas nos EUA

**Instituição:** FAESA Centro Universitário  
**Professor:** Howard Roatti  
**Disciplina:** Data Analysis and Machine Learning  
**Entrega:** 16/06 via GitHub | Apresentação: 17/06 ou 18/06

---

## Sobre o Projeto

Análise completa do dataset de preços de casas nos Estados Unidos disponível no Kaggle, cobrindo desde a exploração dos dados até a construção de modelos de aprendizagem supervisionada e não supervisionada.

**Dataset:** [House Prices - Advanced Regression Techniques](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data)  
**Registros:** 1.460 casas  
**Objetivo:** Prever o preço de venda de casas com base em suas características.

---

## Equipe

| Membro | Usuário GitHub | Responsabilidade |
|----------|----------|----------|
| Matheus | MatheusPas | EDA + Visualização + Infra |
| Gessiele | - | Feature Engineering |
| Eduardo | - | Regressão Linear |
| Lucas | - | PCA + GitHub |
| João | - | Classificação + Clusterização + Outlier/Associação |

---

## Estrutura do Repositório

```text
TrabalhoC3Analise/
│
├── README.md
│
├── docs/
│   ├── api-documentation.md
│   └── divisao-tarefas.md
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_regressao.ipynb
│   ├── 04_classificacao.ipynb
│   ├── 05_clusterizacao.ipynb
│   ├── 06_dimensionalidade.ipynb
│   ├── 07_associacao_outlier.ipynb
│   └── 08_storytelling_final.ipynb
│
├── data/
│   └── train.csv
│
└── api/
    ├── main.py
    ├── models.py
    ├── database.py
    ├── auth.py
    └── routes/
```

---

## Infraestrutura

| Componente | Detalhe |
|------------|---------|
| Servidor | Ubuntu Server 24.04 LTS |
| Banco de Dados | PostgreSQL 16 |
| API | FastAPI |
| Acesso Remoto | Radmin VPN |
| IP da API | 26.246.114.225:8000 |
| Docs da API | http://26.246.114.225:8000/docs |

---

## Como Conectar à API

```python
import requests
import pandas as pd

# Login
response = requests.post(
    "http://26.246.114.225:8000/auth/login",
    json={
        "username": "seu_usuario",
        "password": "sua_senha"
    }
)

token = response.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}"
}

# Carregar dataset completo
df = pd.DataFrame(
    requests.get(
        "http://26.246.114.225:8000/api/v1/houses?limit=1460",
        headers=headers
    ).json()
)

print(df.head())
```

---

## Etapas do Projeto

### 1. Análise Exploratória de Dados (EDA)

- Estatísticas descritivas
- Distribuição dos preços
- Correlação entre variáveis
- Valores ausentes
- Visualizações gráficas
- Identificação de padrões

### 2. Engenharia de Atributos

- Tratamento de dados faltantes
- Encoding de variáveis categóricas
- Normalização e padronização
- Criação de novas features
- Seleção de atributos relevantes

### 3. Aprendizagem Supervisionada

#### Regressão Linear

Objetivo: prever o valor de venda das casas.

Métricas:

- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- R² Score

### 4. Classificação

Transformar o preço em categorias:

| Categoria | Faixa de Preço |
|------------|------------|
| Baixo | Até Q1 |
| Médio | Entre Q1 e Q3 |
| Alto | Acima de Q3 |

Possíveis algoritmos:

- Decision Tree
- Random Forest
- KNN
- Logistic Regression

Métricas:

- Accuracy
- Precision
- Recall
- F1-Score

### 5. Clusterização

Objetivo:

Agrupar casas com características semelhantes sem utilizar o preço como variável alvo.

Algoritmos:

- K-Means
- Hierarchical Clustering

Métricas:

- Silhouette Score
- Inertia

### 6. Redução de Dimensionalidade

Técnica:

- PCA (Principal Component Analysis)

Objetivos:

- Reduzir número de variáveis
- Facilitar visualizações
- Melhorar desempenho computacional

### 7. Regras de Associação

Aplicação:

Descobrir relações frequentes entre características dos imóveis.

Exemplos:

- Casas com garagem para 3 carros tendem a possuir área construída maior.
- Casas com acabamento premium possuem maior valor médio.

Algoritmos:

- Apriori
- FP-Growth

### 8. Detecção de Outliers

Métodos:

- IQR
- Z-Score
- Isolation Forest

Objetivos:

- Identificar imóveis atípicos
- Avaliar impacto nos modelos

### 9. Storytelling com Dados

Entregáveis:

- Dashboard
- Relatório executivo
- Principais insights
- Recomendações de negócio

---

## Critérios de Avaliação

| Critério | Peso |
|-----------|------|
| Organização do GitHub | 2 |
| Qualidade da Análise | 3 |
| Aplicação dos Algoritmos | 3 |
| Storytelling e Apresentação | 2 |

---

## Tecnologias Utilizadas

- Python 3.12+
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn
- FastAPI
- PostgreSQL
- Jupyter Notebook
- Git
- GitHub

---

## Como Executar

```bash
git clone https://github.com/seuusuario/TrabalhoC3Analise.git

cd TrabalhoC3Analise

pip install -r requirements.txt

jupyter notebook
```

---

## Cronograma

| Data | Atividade |
|--------|--------|
| 09/06 | Organização do projeto |
| 10/06 a 13/06 | Desenvolvimento individual |
| 14/06 | Integração dos notebooks |
| 15/06 | Storytelling e revisão |
| 16/06 | Entrega no GitHub |
| 17/06 ou 18/06 | Apresentação |

---

## Licença

Projeto desenvolvido exclusivamente para fins acadêmicos na disciplina de Data Analysis and Machine Learning da FAESA Centro Universitário.