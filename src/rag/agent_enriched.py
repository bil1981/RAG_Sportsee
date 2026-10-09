# src/sportsee/rag/agent_enriched.py
"""
Agent RAG enrichi : retrieval texte + outil SQL (données NBA).
"""
from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Any

import numpy as np
from langchain_ollama import ChatOllama
from sentence_transformers import SentenceTransformer

from sportsee.config import settings
from sportsee.database.database import get_database_path, is_database_available
from sportsee.schemas import RAGResponse


# -----------------------------
# Détection simple "besoin SQL"
# -----------------------------

NUMERIC_KEYWORDS = [
    "pourcentage",
    "moyenne",
    "total",
    "somme",
    "nombre",
    "combien",
    "meilleur",
    "pire",
    "plus de",
    "moins de",
    "compar",
    "domicile",
    "extérieur",
    "rebond",
    "point",
    "passe",
    "interception",
    "contre",
    "3 points",
    "trois points",
    "lancers",
]


def looks_like_numeric_question(question: str) -> bool:
    """
    Heuristique simple pour détecter si la question nécessite probablement
    d'interroger la base de données (stats, scores, etc.).
    """
    q_lower = question.lower()

    # Présence de chiffres (ex. "5 derniers matchs")
    if re.search(r"\d+", q_lower):
        return True

    # Présence de mots-clés "numériques"
    if any(kw in q_lower for kw in NUMERIC_KEYWORDS):
        return True

    return False


# -----------------------------
# Outil SQL minimal (squelette)
# -----------------------------


def execute_sql_query(query: str) -> list[dict[str, Any]]:
    """
    Exécute une requête SQL en lecture seule sur la base SQLite.

    Pour l'instant, on met un squelette sécurisé qui :
    - n'autorise que SELECT / WITH
    - rejette les écritures
    - limite le nombre de lignes retournées.

    À enrichir plus tard avec de vraies requêtes générées par un agent SQL.
    """
    import sqlite3

    db_path = get_database_path()

    if not db_path.exists():
        raise FileNotFoundError(f"Base de données introuvable : {db_path}")

    query = query.strip()

    # Sécurité basique : uniquement SELECT / WITH
    if not re.match(r"^(select|with)\b", query, re.IGNORECASE):
        raise ValueError("Seules les requêtes SELECT ou WITH sont autorisées.")

    forbidden = re.compile(
        r"\b(insert|update|delete|drop|alter|create|attach|pragma|replace|vacuum)\b",
        re.IGNORECASE,
    )
    if forbidden.search(query):
        raise ValueError("Instruction SQL interdite.")

    # Une seule requête
    if ";" in query.rstrip(";"):
        raise ValueError("Une seule requête est autorisée.")

    max_rows = 50

    with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.execute(query)
        rows = cursor.fetchmany(max_rows)

    return [dict(row) for row in rows]


def get_sql_answer_for_question(question: str) -> tuple[str | None, str | None]:
    """
    Pour une question donnée, essaie de générer une réponse via SQL.

    Retourne :
      - sql_query: la requête SQL exécutée (ou None si pas de SQL)
      - sql_result_text: une représentation textuelle du résultat (ou None)

    Ici, on met une logique très basique / extensible :
    - si la question ressemble à "meilleur % à 3 points" → requête dédiée
    - sinon, on ne fait rien (None, None)

    À enrichir avec un vrai générateur NL→SQL ou un agent LangChain SQL.
    """

    q_lower = question.lower()

    # Exemple 1 : meilleur pourcentage à 3 points (tous matchs)
    if "meilleur" in q_lower and ("3 points" in q_lower or "trois points" in q_lower):
        sql = """
            SELECT
                p.player_name,
                SUM(s.three_pm) * 100.0 / NULLIF(SUM(s.three_pa), 0)
                    AS three_point_pct
            FROM stats s
            JOIN players p ON p.player_id = s.player_id
            GROUP BY p.player_id, p.player_name
            HAVING SUM(s.three_pa) > 0
            ORDER BY three_point_pct DESC
            LIMIT 1
        """
        try:
            rows = execute_sql_query(sql)
        except Exception:
            # En cas d'erreur (schéma inexistant, etc.), on retourne None
            return None, None

        if not rows:
            return sql, "Aucun résultat trouvé."

        row = rows[0]
        text = (
            f"Meilleur pourcentage à 3 points : "
            f"{row['player_name']} avec {row['three_point_pct']:.2f} %."
        )
        return sql, text

    # Exemple 2 : comparaison rebonds domicile / extérieur
    if "rebond" in q_lower and ("domicile" in q_lower or "extérieur" in q_lower):
        sql = """
            SELECT
                is_home,
                AVG(rebounds) AS avg_rebounds,
                SUM(rebounds) AS total_rebounds
            FROM stats
            GROUP BY is_home
            ORDER BY is_home DESC
        """
        try:
            rows = execute_sql_query(sql)
        except Exception:
            return None, None

        if not rows:
            return sql, "Aucun résultat trouvé."

        lines = []
        for r in rows:
            location = "domicile" if r["is_home"] else "extérieur"
            lines.append(
                f"{location} : moyenne {r['avg_rebounds']:.2f}, total {r['total_rebounds']}"
            )

        return sql, " | ".join(lines)

    # Par défaut : on n'utilise pas SQL
    return None, None


# -----------------------------
# Agent enrichi
# -----------------------------


class EnrichedRAGAgent:
    def __init__(
        self,
        chunks: list[tuple[str, str]],  # (chunk_id, text)
        top_k: int = 3,
        database_path: str | None = None,
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

        # Vérification optionnelle de la DB
        self.db_available = is_database_available()

    def _retrieve(self, question: str) -> list[tuple[str, str]]:
        q_emb = self.embedder.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]

        scores = self.chunk_embeddings @ q_emb
        top_idx = np.argsort(scores)[-self.top_k :][::-1]

        return [self.chunks[i] for i in top_idx]

    def ask(self, question: str, question_id: str) -> RAGResponse:
        # 1. Détection : faut-il utiliser SQL ?
        use_sql = looks_like_numeric_question(question) and self.db_available

        sql_query: str | None = None
        sql_result_text: str | None = None

        if use_sql:
            sql_query, sql_result_text = get_sql_answer_for_question(question)
            if sql_query is None:
                use_sql = False

        # 2. Récupération des contextes texte
        contexts_docs = self._retrieve(question)
        contexts = [text for _, text in contexts_docs]

        # 3. Construction du prompt
        context_block = "\n\n".join(
            f"[{i+1}] {t}" for i, t in enumerate(contexts)
        )

        parts = []

        parts.append(
            "Tu es un assistant d'analyse de basketball. "
            "Tu dois répondre à la question en t'appuyant sur les contextes ci-dessous "
            "et, si disponibles, sur les données chiffrées fournies."
        )

        if context_block.strip():
            parts.append(f"Contextes :\n{context_block}")

        if sql_result_text:
            parts.append(f"Données chiffrées :\n{sql_result_text}")

        parts.append(f"Question : {question}")
        parts.append("Réponse :")

        prompt = "\n\n".join(parts)

        # 4. Appel au LLM
        start = time.time()
        response = self.llm.invoke(prompt)
        latency_ms = (time.time() - start) * 1000

        return RAGResponse(
            question_id=question_id,
            question=question,
            answer=response.content,
            contexts=contexts,
            latency_ms=latency_ms,
            used_sql=use_sql,
            sql_query=sql_query,
            error=None,
        )