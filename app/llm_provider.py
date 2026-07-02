import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"
OPENROUTER_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"


def get_llm(temperature: float = 0.0):
    """
    Returns a chat model based on LLM_PROVIDER env var.
    Both paths expose the same LangChain interface, so graph/agent
    code never needs to know which provider is active.
    """
    provider = os.getenv("LLM_PROVIDER", "groq").lower()

    if provider == "groq":
        return ChatGroq(
            model=GROQ_MODEL,
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY"),
        )

    if provider == "openrouter":
        return ChatOpenAI(
            model=OPENROUTER_MODEL,
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            temperature=temperature,
        )

    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")