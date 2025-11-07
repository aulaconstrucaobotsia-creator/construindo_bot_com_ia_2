import os
import streamlit as st
from dotenv import load_dotenv
from agent_factory import get_agent

# Carrega variáveis do .env (opcional em dev; no Render, use env vars do painel)
load_dotenv()

st.set_page_config(page_title="Bot de Atendimento (Agno)", page_icon="🤖", layout="centered")

st.title("🤖 Bot de Atendimento • Agno + Streamlit")
st.caption("Exemplo hospedado no Render • Python + Agno + DuckDuckGo")

# Mensagem inicial
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou um bot de atendimento. Pergunte algo 😊"}
    ]

# Mostra histórico
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Caixa de entrada
user_text = st.chat_input("Digite sua mensagem...")
if user_text:
    # Adiciona a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # Obtém (ou cria) o agente do Agno
    try:
        agent = get_agent()
    except Exception as e:
        err = f"Erro ao inicializar o agente: {e}"
        st.session_state.messages.append({"role": "assistant", "content": err})
        with st.chat_message("assistant"):
            st.error(err)
        st.stop()

    # Chama o agente
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Resposta simples (não-streaming)
                answer = agent.run(user_text)
            except Exception as e:
                answer = f"Desculpe, ocorreu um erro: {e}"

            st.markdown(answer)

    # Salva no histórico
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Rodapé/health
st.sidebar.header("⚙️ Configurações")
st.sidebar.write("**Modelo:** usa OpenAI via Agno")
st.sidebar.write("**Ferramentas:** DuckDuckGo (busca web)")
st.sidebar.divider()
st.sidebar.write("Defina `OPENAI_API_KEY` nas variáveis de ambiente.")