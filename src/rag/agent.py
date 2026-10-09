# src/sportsee/rag/agent.py
"""
Agent RAG de base : retrieval + LLM (Ollama), sans SQL.
"""
from __future__ import annotations


import time
from typing import Any


import numpy as np
from langchain_ollama import ChatOllama
from sentence_transformers import SentenceTransformer


from sportsee.config import settings
from sportsee.schemas import RAGResponse


class SimpleRAGAgent:
    def __init__(
        self,
        chunks: list[tuple[str, str]],  # (chunk_id, text)
        top_k: int = 3,
    ):
        self.chunks = chunks
        self.top_k = top_k

        # LLM Ollama
        self.llm = ChatOllama(
            model=settings.OLLAMA_CHAT_MODEL,
            base_url=settings.OLLAMA_CHAT_BASE_URL,
            temperature=0,
            num_predict=1024,
        )

        # Embedding model
        self.embedder = SentenceTransformer(settings.EMBEDDING_MODEL)

        # Pré-calcul des embeddings des chunks
        self.chunk_texts = [text for _, text in chunks]
        self.chunk_embeddings = self.embedder.encode(
            self.chunk_texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        # Vérif rapide de la dimension
        if self.chunk_embeddings.ndim != 2 or self.chunk_embeddings.shape[1] == 0:
            raise RuntimeError(
                f"Embeddings des chunks invalides: shape={self.chunk_embeddings.shape}"
            )

    def _retrieve(self, question: str) -> list[tuple[str, str]]:
        """
        Retourne les top_k chunks les plus similaires à la question.
        """
        if not question or not question.strip():
            raise ValueError("Question vide ou None reçue dans _retrieve")

        q_emb = self.embedder.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]

        if q_emb.size == 0:
            raise RuntimeError(
                f"Embedding de la question vide: shape={q_emb.shape}, question={question!r}"
            )

        # Similarité cosinus (embeddings déjà normalisés)
        scores = self.chunk_embeddings @ q_emb
        top_idx = np.argsort(scores)[-self.top_k :][::-1]

        return [self.chunks[i] for i in top_idx]

    def ask(self, question: str, question_id: str) -> RAGResponse:
        if not question or not question.strip():
            raise ValueError("Question vide ou None reçue dans ask")

        contexts_docs = self._retrieve(question)
        contexts = [text for _, text in contexts_docs]

        context_block = "\n\n".join(
            f"[{i+1}] {t}" for i, t in enumerate(contexts)
        )

        prompt = f"""Tu es un assistant d'analyse de basketball.
Tu dois répondre à la question en t'appuyant sur les contextes ci-dessous.
Si les contextes ne permettent pas de répondre, indique-le clairement.


Contextes :
{context_block}


Question : {question}


Réponse :"""

        start = time.time()
        response = self.llm.invoke(prompt)
        latency_ms = (time.time() - start) * 1000

        return RAGResponse(
            question_id=question_id,
            answer=response.content,
            question=question,
            contexts=contexts,
            latency_ms=latency_ms,
            used_sql=False,
            sql_query=None,
            error=None,
        )