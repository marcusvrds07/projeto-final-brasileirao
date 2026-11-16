# Receita e desempenho dos clubes no Brasileirão (2007-2024)

![Python](https://img.shields.io/badge/python-3.13-blue)
![pandas](https://img.shields.io/badge/pandas-3.1.1-purple)
![Licença](https://img.shields.io/badge/licença-MIT-green)
![Dados](https://img.shields.io/badge/dados-CC%20BY--SA%204.0-lightgrey)

**Autores:** Marcus Vinicius Rodrigues da Silva e Marcus Filipe dos Santos Mendes  
**Instituição:** Unilasalle RJ  
**Curso:** Bacharelado em Sistemas de Informação - 6º Período  
**Disciplina:** Linguagem de Programação  
**Professor:** Alexandre Louzada  

**Artigo publicado:** https://marcusvrds07.github.io/projeto-final-brasileirao/

## Resumo

Neste projeto analisamos se os clubes com mais dinheiro têm desempenho melhor no Campeonato Brasileiro Série A. Usamos uma base do Kaggle com 302 registros (um por clube em cada temporada, de 2007 a 2024), com receita, resultado financeiro, valor do elenco e estatísticas de campo.

Principais resultados:

- A receita tem correlação de 0,59 com o aproveitamento. Os clubes da faixa de maior receita ganharam 11 dos 18 títulos, e os da menor faixa não ganharam nenhum.
- Ter superávit no ano não fez diferença no desempenho do ano seguinte.

**Palavras-chave:** futebol; Brasileirão; finanças de clubes; análise de dados; Python; FAIR.

## Fonte dos dados

MOREIRA, Wil. *Campeonato BR 2007-2024 Financeiro*. Kaggle, 2025.
https://www.kaggle.com/datasets/wilgomoreira/campeonato-br-2007-2024-financeiro

## Estrutura do projeto

```
projeto-final-brasileirao/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/                  -> planilha original do Kaggle
│   ├── processed/            -> dados tratados (.parquet e .csv.gz)
│   └── data_dictionary.md    -> explicação de cada coluna
├── notebooks/
│   └── analise_exploratoria.ipynb
├── src/
│   ├── __init__.py
│   └── etl.py                -> carga, limpeza e criação das métricas
└── docs/
    ├── index.html            -> artigo
    └── assets/               -> gráficos
```

## Como executar

```bash
git clone https://github.com/marcusvrds07/projeto-final-brasileirao.git
cd projeto-final-brasileirao
python -m venv .venv
```

Ative o ambiente virtual. No Windows use `.venv\Scripts\activate`; no Linux/Mac use `source .venv/bin/activate`.

```bash
pip install -r requirements.txt
python -m src.etl
```

Esse comando gera os arquivos em `data/processed/`. Se a planilha de `data/raw/` não existir, o script baixa ela do Kaggle (não precisa de login).

Para refazer a análise e os gráficos, abra o notebook `notebooks/analise_exploratoria.ipynb` no Jupyter ou VS Code e execute todas as células.

## Princípios FAIR

- **Findable:** este README tem resumo, palavras-chave, autores e o link da fonte dos dados.
- **Accessible:** o repositório é público e os dados podem ser baixados sem login.
- **Interoperable:** os dados tratados estão em Parquet e CSV.gz, e todas as colunas estão explicadas em `data/data_dictionary.md`.
- **Reusable:** tem licença aberta e as versões das bibliotecas estão fixadas em `requirements.txt`.

## Licença

- Código: MIT (arquivo `LICENSE`)
- Texto do artigo: CC BY 4.0
- Dados: CC BY-SA 4.0. Mantivemos a licença da base original porque ela exige que os dados derivados usem a mesma licença.
