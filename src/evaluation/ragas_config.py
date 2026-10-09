from openai import OpenAI
from ragas.llms import llm_factory


def get_ollama_llm_for_ragas(model: str = "llama3.1:8b"):
    client = OpenAI(
        api_key="ollama",  # clé fictive, Ollama n’en demande pas
        base_url="http://localhost:11434/v1",
    )
    return llm_factory(model=model, provider="openai", client=client)

from langchain_ollama import ChatOllama
from ragas.llms import LangchainLLMWrapper

from sportsee.config import settings


def get_ollama_llm_for_ragas_langchain():
    llm = ChatOllama(
        model=settings.OLLAMA_CHAT_MODEL,
        base_url=settings.OLLAMA_CHAT_BASE_URL,
        temperature=0,
        num_predict=1024,
    )
    return LangchainLLMWrapper(llm)