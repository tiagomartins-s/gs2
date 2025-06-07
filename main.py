import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import openai
import requests

# ======================== CONFIGURAÇÃO DO APP ========================
st.set_page_config(page_title="Monitor de Enchentes", page_icon="🌊", layout="wide")

openai.api_key = os.getenv("OPENAI_API_KEY")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

ITENS_CSV = "itens_importados.csv"
LOCAIS_CSV = "locais_enchentes.csv"

# ======================== FUNÇÕES AUXILIARES ========================
def init_csvs():
    if not os.path.exists(ITENS_CSV):
        pd.DataFrame(columns=["user", "message", "date", "classification", "location"]).to_csv(ITENS_CSV, index=False)
    if not os.path.exists(LOCAIS_CSV):
        pd.DataFrame(columns=["location", "date", "report_count"]).to_csv(LOCAIS_CSV, index=False)

def cria_url():
    query = "enchente -is:retweet lang:pt"
    max_results = 10
    tweet_fields = "tweet.fields=created_at,author_id"
    return f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results={max_results}&{tweet_fields}"

def bearer_oauth(request):
    if not BEARER_TOKEN:
        raise RuntimeError("Variável BEARER_TOKEN não encontrada.")
    request.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    request.headers["User-Agent"] = "v2RecentSearchPython"
    return request

def conecta_endpoint(url):
    response = requests.get(url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")
    return response.json()

def buscar_tweets():
    url = cria_url()
    dados = conecta_endpoint(url)
    tweets = dados.get("data", [])
    novos = []
    for t in tweets:
        novos.append({
            "user": str(t["author_id"]),
            "message": t["text"].replace("\n", " "),
            "date": t["created_at"],
            "classification": "",
            "location": ""
        })
    return pd.DataFrame(novos)

# ======================== CLASSIFICAÇÃO COM OPENAI < 1.0.0 ========================
def classificar_e_atualizar(itens_df, locais_df):
    atualizou = False
    itens_df["classification"] = itens_df["classification"].astype(str)

    unclassified = itens_df[
        itens_df["classification"].isna()
        | (itens_df["classification"].str.strip() == "")
        | (itens_df["classification"] == "nan")
    ]

    if unclassified.empty:
        return itens_df, locais_df, 0

    for idx, row in unclassified.iterrows():
        user, message, date = row["user"], row["message"], row["date"]
        prompt = f"""
Classifique a seguinte mensagem de usuário de Twitter:

Usuário: {user}
Mensagem: "{message}"
Data: {date}

Responda apenas com JSON no formato:
{{
  "classification": "report" ou "comment",
  "location": "nome do local se for report, ou vazia se comment"
}}
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um assistente que classifica relatos de enchentes em tweets."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            content = response.choices[0].message.content.strip()
            parsed = json.loads(content)
            classification = parsed.get("classification", "comment").lower().strip()
            location = parsed.get("location", "").strip()

            itens_df.at[idx, "classification"] = classification
            itens_df.at[idx, "location"] = location
            atualizou = True

            if classification == "report" and location:
                try:
                    date_str = pd.to_datetime(date).date().isoformat()
                except:
                    date_str = date

                mask = (locais_df["location"] == location) & (locais_df["date"] == date_str)
                if mask.any():
                    locais_df.loc[mask, "report_count"] += 1
                else:
                    novos_dados = pd.DataFrame([{"location": location, "date": date_str, "report_count": 1}])
                    locais_df = pd.concat([locais_df, novos_dados], ignore_index=True)

        except Exception as e:
            print("❌ Erro ao classificar tweet:")
            print(f"Mensagem: {message}")
            print(f"Erro: {e}")
            continue

    if atualizou:
        itens_df.to_csv(ITENS_CSV, index=False)
        locais_df.to_csv(LOCAIS_CSV, index=False)

    return itens_df, locais_df, len(unclassified)

# ======================== INÍCIO DO APP ========================
init_csvs()
itens_df = pd.read_csv(ITENS_CSV, dtype={"user": str})
locais_df = pd.read_csv(LOCAIS_CSV)

st.title("🌊 Monitor de Enchentes via Twitter")
st.markdown("Este app monitora automaticamente tweets que mencionam **enchentes**, classifica o conteúdo e identifica locais afetados.")

tabs = st.tabs(["📍 Locais com Enchente Detectada", "📋 Itens Importados"])

# ======================== ABA 1: LOCAIS ========================
with tabs[0]:
    st.header("📍 Locais com Enchente Detectada")

    if locais_df.empty:
        st.info("Nenhum local detectado ainda.")
    else:
        st.dataframe(locais_df.sort_values(by=["date", "report_count"], ascending=[False, False]))

# ======================== ABA 2: ITENS IMPORTADOS ========================
with tabs[1]:
    st.header("📋 Itens Importados e Classificados")

    if st.button("🔍 Buscar Tweets do X"):
        try:
            novos_df = buscar_tweets()
            if not novos_df.empty:
                itens_df = pd.concat([itens_df, novos_df], ignore_index=True).drop_duplicates(subset=["user", "message", "date"])
                itens_df.to_csv(ITENS_CSV, index=False)
                st.success(f"{len(novos_df)} tweets adicionados.")
            else:
                st.info("Nenhum tweet novo encontrado.")
        except Exception as e:
            st.error(f"Erro ao buscar tweets: {e}")
            print("❌ Erro na busca de tweets:", e)

    if st.button("⚙️ Analisar e Classificar Itens"):
        with st.spinner("Classificando tweets..."):
            try:
                itens_df, locais_df, total_classificados = classificar_e_atualizar(itens_df, locais_df)
                if total_classificados > 0:
                    st.success(f"{total_classificados} itens classificados com sucesso!")
                else:
                    st.info("Nenhum item novo para classificar.")
            except Exception as e:
                st.error("Erro inesperado na classificação.")
                print("❌ Erro geral ao classificar:", e)

    st.markdown("### Lista de todos os tweets importados:")
    st.dataframe(itens_df)
