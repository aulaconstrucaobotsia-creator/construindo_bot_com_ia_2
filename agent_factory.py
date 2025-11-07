import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

# Use o ID de modelo que você preferir/tem acesso.
# Você usou "gpt-4-turbo" no seu script; mantenho por compatibilidade.
# Se necessário, troque por "gpt-4o" / "gpt-4.1" etc.
MODEL_ID = os.getenv("OPENAI_MODEL_ID", "gpt-4-turbo")

def get_agent() -> Agent:
    """
    Cria um agente Agno com modelo OpenAI e a ferramenta DuckDuckGo.
    Necessário: OPENAI_API_KEY definida no ambiente.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError("Defina a variável de ambiente OPENAI_API_KEY no Render.")

    # O Agno lê a OPENAI_API_KEY do ambiente.
    agent = Agent(
        model=OpenAIChat(id=MODEL_ID),
        tools=[DuckDuckGoTools()],
        markdown=True,
        # Você pode adicionar instruções iniciais do "perfil" de atendimento:
        instructions=[
            "Você é um bot de atendimento amigável.",
            "Se usar informações da web, cite a fonte na resposta.",
        ],
    )
    return agent