# Dicionário de Dados

**Fonte:** Kaggle - Campeonato BR 2007-2024 Financeiro (Wil Moreira), licença CC BY-SA 4.0
**Link:** https://www.kaggle.com/datasets/wilgomoreira/campeonato-br-2007-2024-financeiro
**Arquivo bruto:** `data/raw/dataset_campeonato_br_2007_2024_v2.xlsx`
**Arquivos tratados:** `data/processed/brasileirao_tratado.parquet` e `data/processed/brasileirao_tratado.csv.gz`
**Granularidade:** cada linha é um clube em uma temporada (302 linhas, de 2007 a 2024, com 16 a 18 clubes por ano)

## Colunas que vieram da base original

| Coluna | Nome original | Tipo | Formato / unidade | Significado |
|---|---|---|---|---|
| ano | Ano | inteiro | AAAA | Ano da temporada |
| posicao | Posição | inteiro | 1 a 20 | Posição final na tabela |
| clube | Clube | texto | - | Nome do clube |
| vitorias | Vitorias | inteiro | partidas | Número de vitórias |
| empates | Empates | inteiro | partidas | Número de empates |
| derrotas | Derrotas | inteiro | partidas | Número de derrotas |
| gols_feitos | Gols_feitos | inteiro | gols | Gols marcados |
| gols_sofridos | Gols_sofridos | inteiro | gols | Gols sofridos |
| saldo_gols | Saldo | inteiro | gols | Gols feitos menos gols sofridos |
| pontos | Pontos | inteiro | pontos | Pontuação final (com punições) |
| receita | Receita_anual | decimal | R$ milhões | Receita bruta do clube no ano (valor nominal, sem correção pela inflação) |
| resultado_financeiro | Deficit_ou_Superavit | decimal | R$ milhões | Resultado do ano. Negativo = déficit, positivo = superávit |
| qtd_jogadores | Qtd_Jogadores | inteiro | jogadores | Quantidade de jogadores no elenco |
| idade_media | Idade_Media | decimal | anos | Idade média do elenco |
| estrangeiros | Estrangeiros | inteiro | jogadores | Quantidade de estrangeiros no elenco |
| valor_medio_jogador | Media_plantel | decimal | € milhões | Valor de mercado médio por jogador |
| valor_elenco | Valor_plantel | decimal | € milhões | Valor de mercado total do elenco (Transfermarkt) |
| campeao | Campeao | booleano | True/False | Se o clube foi campeão naquele ano |

## Colunas criadas no tratamento (`src/etl.py`)

| Coluna | Tipo | Como é calculada | Significado |
|---|---|---|---|
| jogos | inteiro | vitorias + empates + derrotas | Partidas disputadas |
| jogos_diferente_de_38 | booleano | jogos != 38 | Marca Atlético-MG e Chapecoense em 2016, que jogaram 37 partidas (jogo cancelado após o acidente da Chapecoense) |
| pontos_nao_batem | booleano | pontos != 3 x vitorias + empates | Marca o Flamengo de 2013, que perdeu 4 pontos no STJD |
| aproveitamento | decimal | pontos / (jogos x 3) x 100 | Percentual de pontos ganhos |
| receita_relativa | decimal | receita / mediana da receita no ano | Quantas vezes a receita do clube é maior que a do clube "do meio" naquele ano. Serve para comparar anos diferentes sem precisar corrigir a inflação |
| ranking_receita | inteiro | posição da receita dentro do ano | 1 = clube com maior receita no ano |
| teve_superavit | booleano | resultado_financeiro > 0 | Se o clube fechou o ano no azul |
| margem_financeira | decimal | resultado_financeiro / receita x 100 | Resultado como percentual da receita |
| faixa_receita | texto | quartis da receita dentro de cada ano | "1 - menor" a "4 - maior" |
| superavit_ano_anterior | booleano (pode ser vazio) | teve_superavit do mesmo clube no ano anterior | Vazio quando o clube não estava na base no ano anterior |
| aproveitamento_ano_anterior | decimal (pode ser vazio) | aproveitamento do ano anterior | Idem |
| variacao_aproveitamento | decimal (pode ser vazio) | aproveitamento - aproveitamento_ano_anterior | Quanto o clube melhorou ou piorou de um ano para o outro |

## Observações sobre a qualidade dos dados

- A base não tem valores nulos nem linhas duplicadas. Mesmo assim, o script remove linhas sem ano, clube ou pontos e preenche receita ou valor do elenco vazios com a mediana do ano.
- Os casos fora da regra (37 jogos em 2016 e a punição do Flamengo em 2013) são reais. Por isso eles foram mantidos e apenas marcados em colunas próprias.
- Nem todos os 20 clubes de cada ano estão na base (faltam de 2 a 4 por temporada).
