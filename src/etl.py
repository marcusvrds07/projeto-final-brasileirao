import io
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

PASTA = Path(__file__).resolve().parents[1]
ARQUIVO_BRUTO = PASTA / "data" / "raw" / "dataset_campeonato_br_2007_2024_v2.xlsx"
PASTA_PROCESSADOS = PASTA / "data" / "processed"
URL_DOWNLOAD = "https://www.kaggle.com/api/v1/datasets/download/wilgomoreira/campeonato-br-2007-2024-financeiro"

NOVOS_NOMES = {
    "Ano": "ano",
    "Posição": "posicao",
    "Clube": "clube",
    "Vitorias": "vitorias",
    "Empates": "empates",
    "Derrotas": "derrotas",
    "Gols_feitos": "gols_feitos",
    "Gols_sofridos": "gols_sofridos",
    "Saldo": "saldo_gols",
    "Pontos": "pontos",
    "Receita_anual": "receita",
    "Deficit_ou_Superavit": "resultado_financeiro",
    "Qtd_Jogadores": "qtd_jogadores",
    "Idade_Media": "idade_media",
    "Estrangeiros": "estrangeiros",
    "Media_plantel": "valor_medio_jogador",
    "Valor_plantel": "valor_elenco",
    "Campeao": "campeao",
}


def baixar_dados():
    if ARQUIVO_BRUTO.exists():
        return
    ARQUIVO_BRUTO.parent.mkdir(parents=True, exist_ok=True)
    resposta = urllib.request.urlopen(URL_DOWNLOAD)
    with zipfile.ZipFile(io.BytesIO(resposta.read())) as arquivo_zip:
        ARQUIVO_BRUTO.write_bytes(arquivo_zip.read(arquivo_zip.namelist()[0]))


def carregar_dados():
    baixar_dados()
    return pd.read_excel(ARQUIVO_BRUTO)


def limpar_dados(df):
    df = df.rename(columns=NOVOS_NOMES)
    df["clube"] = df["clube"].str.strip()

    colunas_inteiras = ["ano", "posicao", "vitorias", "empates", "derrotas", "gols_feitos",
                        "gols_sofridos", "saldo_gols", "pontos", "qtd_jogadores", "estrangeiros"]
    colunas_decimais = ["receita", "resultado_financeiro", "idade_media", "valor_medio_jogador", "valor_elenco"]
    df[colunas_inteiras] = df[colunas_inteiras].apply(pd.to_numeric, errors="coerce").astype("Int64")
    df[colunas_decimais] = df[colunas_decimais].apply(pd.to_numeric, errors="coerce")
    df["campeao"] = df["campeao"] == 1

    print("Valores nulos por coluna:", df.isna().sum().sum())
    print("Linhas duplicadas:", df.duplicated(subset=["ano", "clube"]).sum())

    df = df.dropna(subset=["ano", "clube", "pontos"])
    df = df.drop_duplicates(subset=["ano", "clube"])

    for coluna in ["receita", "valor_elenco"]:
        df[coluna] = df[coluna].fillna(df.groupby("ano")[coluna].transform("median"))

    return df


def verificar_inconsistencias(df):
    df["jogos"] = df["vitorias"] + df["empates"] + df["derrotas"]
    df["jogos_diferente_de_38"] = df["jogos"] != 38
    df["pontos_nao_batem"] = df["pontos"] != 3 * df["vitorias"] + df["empates"]

    print("Clubes com número de jogos diferente de 38:")
    print(df.loc[df["jogos_diferente_de_38"], ["ano", "clube", "jogos"]])
    print("Clubes com pontuação diferente de 3V + E:")
    print(df.loc[df["pontos_nao_batem"], ["ano", "clube", "vitorias", "empates", "pontos"]])
    return df


def criar_metricas(df):
    df["aproveitamento"] = (df["pontos"] / (df["jogos"] * 3) * 100).round(1)
    df["receita_relativa"] = (df["receita"] / df.groupby("ano")["receita"].transform("median")).round(2)
    df["ranking_receita"] = df.groupby("ano")["receita"].rank(ascending=False, method="min").astype(int)
    df["teve_superavit"] = df["resultado_financeiro"] > 0
    df["margem_financeira"] = (df["resultado_financeiro"] / df["receita"] * 100).round(1)
    df["faixa_receita"] = df.groupby("ano")["receita"].transform(
        lambda receitas: pd.qcut(receitas.rank(method="first"), 4, labels=["1 - menor", "2", "3", "4 - maior"])
    )

    df = df.sort_values(["clube", "ano"])
    mesmo_clube = df.groupby("clube")
    ano_seguido = mesmo_clube["ano"].diff() == 1
    df["superavit_ano_anterior"] = mesmo_clube["teve_superavit"].shift(1).where(ano_seguido)
    df["aproveitamento_ano_anterior"] = mesmo_clube["aproveitamento"].shift(1).where(ano_seguido)
    df["variacao_aproveitamento"] = df["aproveitamento"] - df["aproveitamento_ano_anterior"]

    return df.sort_values(["ano", "posicao"]).reset_index(drop=True)


def salvar_dados(df):
    PASTA_PROCESSADOS.mkdir(parents=True, exist_ok=True)
    df["faixa_receita"] = df["faixa_receita"].astype(str)
    df.to_parquet(PASTA_PROCESSADOS / "brasileirao_tratado.parquet", index=False)
    df.to_csv(PASTA_PROCESSADOS / "brasileirao_tratado.csv.gz", index=False, compression="gzip")


def executar():
    df = carregar_dados()
    print("Linhas e colunas do arquivo original:", df.shape)
    df = limpar_dados(df)
    df = verificar_inconsistencias(df)
    df = criar_metricas(df)
    salvar_dados(df)
    print("Arquivo tratado salvo com", df.shape[0], "linhas e", df.shape[1], "colunas")
    return df


if __name__ == "__main__":
    executar()
