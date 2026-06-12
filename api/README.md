# Documentação da API — Hackathon House Prices

**Projeto:** Analisando Dados de Preços de Casas nos Estados Unidos  
**Professor:** Howard Roatti — FAESA Centro Universitário  
**Versão da API:** 2.0.0  
**Base URL Local:** `http://192.168.0.60:8000`  
**Base URL Remota (Radmin):** `http://26.246.114.225:8000`  
**Documentação Interativa:** `http://192.168.0.60:8000/docs`

---

## Como Funciona

A API foi construída com **FastAPI** e se conecta ao banco **PostgreSQL** que contém os 1.460 registros do dataset de preços de casas do Kaggle.

Todos os endpoints (exceto o login) exigem autenticação via **token JWT**. O fluxo é:

```
1. POST /auth/login        → enviar usuário e senha do Linux
2. Receber token JWT       → usar em todas as requisições seguintes
3. GET /api/v1/...         → passar o token no header Authorization
```

---

## Autenticação

### `POST /auth/login`

Autentica o usuário com suas credenciais do Linux e retorna um token JWT válido por 8 horas.

**Body:**
```json
{
  "username": "seu_user",
  "password": "sua_senha"
}
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "username": "seu_user"
}
```

**Como usar o token nas requisições seguintes:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Usuários disponíveis:**

| Usuário | Descrição |
|---|---|
| `matheus_root` | Administrador |
| `gessiele_dev` | Desenvolvedor |
| `eduardo_dev` | Desenvolvedor |
| `lucas_dev` | Desenvolvedor |
| `joao_dev` | Desenvolvedor |

---

## Como Usar no Jupyter Notebook

```python
import requests

# 1. Login
response = requests.post("http://26.246.114.225:8000/auth/login", json={
    "username": "seu_usuario",
    "password": "sua_senha"
})
token = response.json()["access_token"]

# 2. Header para todas as requisições
headers = {"Authorization": f"Bearer {token}"}

# 3. Buscar dados
response = requests.get("http://26.246.114.225:8000/api/v1/houses?limit=1460", headers=headers)
import pandas as pd
df = pd.DataFrame(response.json())
```

---

## Endpoints

### Casas — `/api/v1/houses`

#### `GET /api/v1/houses`
Lista todas as casas com paginação.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `skip` | int | 0 | Registros para pular |
| `limit` | int | 100 | Máximo de registros (use 1460 para todos) |

**Exemplo:**
```
GET /api/v1/houses?limit=1460
```

**Resposta:**
```json
[
  {
    "id": 1,
    "ms_subclass": 60,
    "ms_zoning": "RL",
    "lot_area": 8450,
    "neighborhood": "CollgCr",
    "overall_qual": 7,
    "overall_cond": 5,
    "year_built": 2003,
    "gr_liv_area": 1710,
    "full_bath": 2,
    "half_bath": 1,
    "bedroom_abvgr": 3,
    "garage_cars": 2.0,
    "garage_area": 548.0,
    "sale_price": 208500
  }
]
```

---

#### `GET /api/v1/houses/{id}`
Retorna os dados de uma casa específica pelo ID.

**Exemplo:**
```
GET /api/v1/houses/1
```

---

#### `GET /api/v1/houses/stats/summary`
Retorna estatísticas gerais do dataset.

**Resposta:**
```json
{
  "usuario": "matheus_root",
  "total_casas": 1460,
  "preco_medio": 180921.20,
  "preco_minimo": 34900,
  "preco_maximo": 755000,
  "area_media": 1515.46,
  "qualidade_media": 6.10
}
```

---

#### `GET /api/v1/houses/neighborhood/{neighborhood}`
Lista todas as casas de um bairro específico.

**Exemplo:**
```
GET /api/v1/houses/neighborhood/CollgCr
```

---

### EDA — `/api/v1/eda`

#### `GET /api/v1/eda/missing-values`
Retorna a quantidade e percentual de valores faltantes por coluna.

**Resposta:**
```json
{
  "usuario": "matheus_root",
  "total_registros": 1460,
  "missing_values": {
    "garage_cars": { "missing": 0, "missing_pct": 0.0 },
    "sale_price": { "missing": 0, "missing_pct": 0.0 }
  }
}
```

---

#### `GET /api/v1/eda/correlations`
Retorna a correlação de todas as variáveis numéricas com o preço de venda, ordenadas da maior para a menor.

**Resposta:**
```json
{
  "usuario": "matheus_root",
  "correlacao_com_preco": {
    "sale_price": 1.0,
    "overall_qual": 0.7910,
    "gr_liv_area": 0.7086,
    "garage_cars": 0.6404
  }
}
```

---

#### `GET /api/v1/eda/distribution`
Retorna a distribuição estatística do preço de venda (min, max, média, quartis).

**Resposta:**
```json
{
  "usuario": "matheus_root",
  "distribuicao_preco": {
    "min": 34900,
    "max": 755000,
    "media": 180921.20,
    "q1": 129975.0,
    "mediana": 163000.0,
    "q3": 214000.0
  }
}
```

---

### Feature Engineering — `/api/v1/features`

#### `GET /api/v1/features/new-features`
Cria e retorna novas features derivadas do dataset:
- `house_age` — idade da casa (2024 − year_built)
- `remod_age` — anos desde a reforma (2024 − year_remod_add)
- `total_bath` — total de banheiros (full_bath + 0.5 × half_bath)
- `area_per_room` — área média por cômodo

---

#### `GET /api/v1/features/normalize`
Normaliza as variáveis numéricas.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Opções |
|---|---|---|---|
| `method` | string | `minmax` | `minmax`, `standard` |

**Exemplo:**
```
GET /api/v1/features/normalize?method=standard
```

---

#### `GET /api/v1/features/encode`
Aplica Label Encoding nas variáveis categóricas (`ms_zoning`, `street`, `neighborhood`) e retorna o mapeamento.

---

### Regressão — `/api/v1/regression`

#### `GET /api/v1/regression/simple`
Treina uma Regressão Linear Simples usando `gr_liv_area` para prever `sale_price`.

**Resposta:**
```json
{
  "usuario": "eduardo_dev",
  "modelo": "Regressão Linear Simples",
  "variavel": "gr_liv_area",
  "coeficiente": 111.6944,
  "intercepto": 18569.0258,
  "metricas": {
    "RMSE": 56263.18,
    "MAE": 40941.55,
    "R2": 0.4939
  }
}
```

---

#### `GET /api/v1/regression/multiple`
Treina uma Regressão Linear Múltipla com todas as variáveis numéricas relevantes.

**Resposta:**
```json
{
  "usuario": "eduardo_dev",
  "modelo": "Regressão Linear Múltipla",
  "coeficientes": {
    "overall_qual": 18524.3,
    "gr_liv_area": 55.42
  },
  "metricas": {
    "RMSE": 43201.12,
    "MAE": 30512.44,
    "R2": 0.7023
  }
}
```

---

### Classificação — `/api/v1/classification`

#### `GET /api/v1/classification/knn`
Treina um modelo KNN para classificar casas como preço alto (1) ou baixo (0).

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `k` | int | 5 | Número de vizinhos |

**Resposta:**
```json
{
  "usuario": "joao_dev",
  "modelo": "KNN",
  "k": 5,
  "metricas": {
    "accuracy": 0.8356,
    "precision": 0.8412,
    "recall": 0.8290,
    "f1_score": 0.8350
  },
  "matriz_confusao": [[120, 22], [26, 124]]
}
```

---

#### `GET /api/v1/classification/random-forest`
Treina um modelo Random Forest com 100 árvores e retorna também a importância de cada feature.

---

### Clusterização — `/api/v1/clustering`

#### `GET /api/v1/clustering/kmeans`
Agrupa as casas em clusters usando K-Means. Também retorna o método Elbow para escolha do número ideal de clusters.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `n_clusters` | int | 3 | Número de clusters |

**Resposta:**
```json
{
  "usuario": "joao_dev",
  "n_clusters": 3,
  "elbow": { "2": 1200.5, "3": 850.2, "4": 710.1 },
  "perfil_clusters": {
    "0": { "sale_price": 120000, "overall_qual": 5.2 },
    "1": { "sale_price": 280000, "overall_qual": 7.8 }
  },
  "distribuicao": { "0": 612, "1": 498, "2": 350 }
}
```

---

#### `GET /api/v1/clustering/outliers`
Detecta casas atípicas usando o algoritmo Local Outlier Factor (LOF).

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `n_neighbors` | int | 20 | Número de vizinhos para o LOF |

---

### PCA & Associação — `/api/v1/pca`

#### `GET /api/v1/pca/run`
Aplica PCA ao dataset e retorna a variância explicada, variância acumulada e os loadings de cada componente.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `n_components` | int | 2 | Número de componentes principais |

**Resposta:**
```json
{
  "usuario": "lucas_dev",
  "n_components": 2,
  "variancia_explicada": [0.4123, 0.1856],
  "variancia_acumulada": [0.4123, 0.5979],
  "loadings": {
    "PC1": { "overall_qual": 0.4201, "gr_liv_area": 0.3987 }
  }
}
```

---

#### `GET /api/v1/pca/association`
Aplica análise de associação manual entre features binárias e o preço alto, retornando suporte, confiança e lift.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `min_support` | float | 0.1 | Suporte mínimo (0.0 a 1.0) |

---

## Campos do Dataset

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | int | Identificador único |
| `ms_subclass` | int | Tipo de habitação |
| `ms_zoning` | string | Classificação de zoneamento |
| `lot_area` | int | Área do terreno (sqft) |
| `street` | string | Tipo de acesso à rua |
| `neighborhood` | string | Bairro |
| `overall_qual` | int | Qualidade geral (1-10) |
| `overall_cond` | int | Condição geral (1-10) |
| `year_built` | int | Ano de construção |
| `year_remod_add` | int | Ano da última reforma |
| `gr_liv_area` | int | Área habitável (sqft) |
| `full_bath` | int | Banheiros completos |
| `half_bath` | int | Lavabos |
| `bedroom_abvgr` | int | Quartos acima do nível do solo |
| `kitchen_abvgr` | int | Cozinhas |
| `totrms_abvgrd` | int | Total de cômodos |
| `garage_cars` | float | Capacidade da garagem (carros) |
| `garage_area` | float | Área da garagem (sqft) |
| `sale_price` | int | Preço de venda (USD) |

---

## Infraestrutura

| Componente | Detalhe |
|---|---|
| Servidor | Ubuntu Server 24.04 LTS |
| IP Local | 192.168.0.60 |
| IP Remoto (Radmin) | 26.246.114.225 |
| Banco de Dados | PostgreSQL 16 |
| Framework | FastAPI 2.0 |
| Porta | 8000 |
| Autenticação | JWT (8h de validade) |