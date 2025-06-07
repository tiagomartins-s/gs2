# 🌊 Monitor de Enchentes com Inteligência Artificial

## 💡 Sobre o Projeto

Este projeto foi desenvolvido como parte do desafio da **Global Solutions 2025.1** da FIAP, cujo tema é:

> "Prever, monitorar ou mitigar os impactos de eventos naturais extremos utilizando dados reais e inteligência artificial."

Com base nessa proposta, nosso grupo escolheu focar em **enchentes**, um dos desastres naturais mais recorrentes, segundo a última carta publicada no site [https://disasterscharter.org](https://disasterscharter.org). Nela, foi destacado que **34% dos desastres monitorados globalmente são relacionados a enchentes**, o que demonstra sua gravidade e frequência.

## 📍 Contexto Pessoal e Social

Sou natural do **Rio Grande do Sul**, estado que foi duramente atingido por uma das maiores enchentes da sua história no ano passado. Viver de perto os impactos desse tipo de desastre — desde perdas materiais até a desorganização social — reforçou a importância de respostas rápidas, eficientes e baseadas em informação confiável.

Foi a partir dessa vivência que surgiu a ideia deste projeto: um **aplicativo que monitora e classifica relatos de enchentes no Twitter (X)** em tempo real, usando **inteligência artificial** para diferenciar comentários genéricos de **relatos reais e geograficamente úteis**.

## 🧠 Como funciona

A aplicação foi desenvolvida com **Python** e utiliza:

- 📡 A API do **X (Twitter)** para buscar tweets contendo a palavra “enchente”.
- 🤖 A API da **OpenAI (ChatGPT)** para classificar o conteúdo dos tweets.
- 📊 **Pandas e Streamlit** para estruturar, armazenar e exibir os dados em tempo real.

O sistema é composto por:

1. Um **coletor automático de tweets** com a palavra-chave "enchente".
2. Um **classificador de intenção** que determina se o tweet é:
   - Um **relato real de enchente** (com local),
   - Ou apenas um **comentário genérico**.
3. Um painel visual interativo com duas abas:
   - **Locais com Enchente Detectada**, mostrando número de relatos por cidade e data.
   - **Itens Importados**, com todos os tweets processados.

## 📲 Motivação e Inovação

Hoje, as redes sociais são fontes vivas de informação descentralizada e em tempo real. Muitas vezes, o poder público e órgãos oficiais só conseguem reagir após esses sinais já estarem circulando entre as pessoas.

Com o **uso de inteligência artificial**, é possível **estruturar esse fluxo espontâneo de informações** e extrair conhecimento valioso — inclusive para tomadas de decisão emergenciais, mapeamento de risco e comunicação com a população.

## 🛠 Tecnologias Utilizadas

- `Python 3.10+`
- `Streamlit`
- `OpenAI API (ChatGPT 4-o)`
- `Twitter API v2 (X)`
- `Pandas`
- `Requests`

## 🔧 Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   - `OPENAI_API_KEY`: sua chave da OpenAI.
   - `BEARER_TOKEN`: seu token do Twitter (X).

5. Rode o app:
   ```bash
   streamlit run app.py
   ```

## 📌 Requisitos (requirements.txt)

```txt
streamlit>=1.20.0
pandas>=1.3.0
openai==0.28.1
requests>=2.25.0
```

## 📢 Considerações Finais

Esta é uma solução funcional, baseada em dados reais, que demonstra como **inteligência artificial + redes sociais** podem ser utilizadas para salvar vidas, antecipar crises e apoiar comunidades afetadas por desastres naturais.

