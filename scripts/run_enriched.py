# scripts/run_enriched.py
"""
Exécute le prototype RAG enrichi avec le Tool SQL sur le jeu de questions
et sauvegarde les réponses au format JSONL pour évaluation RAGAS.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from sportsee.config import settings
from sportsee.logging_config import configure_observability
from sportsee.rag.agent_enriched import EnrichedRAGAgent
from sportsee.rag.chunking import chunk_document
from sportsee.rag.clean import clean_document
from sportsee.evaluation.dataset import load_cases
from sportsee.schemas import RAGResponse, SourceDocument


def load_reddit_documents() -> list[SourceDocument]:
    """
    Même fonction que dans run_baseline.py.
    À harmoniser avec ton vrai pipeline d'ingestion.
    """
    documents: list[SourceDocument] = []

    # Exemple factif à remplacer par ton vrai chargement PDF / texte
    documents.append(
        SourceDocument(
            document_id="dummy-reddit-1",
            source="reddit",
            text=(
                "Match de basket entre les Lakers et les Celtics. "
                "Les Lakers ont gagné 98-95. LeBron James a marqué 30 points "
                "et pris 8 rebonds. Jayson Tatum a inscrit 25 points."
            ),
            metadata={"file": "dummy"},
        )
    )

    return documents


def build_chunks_from_docs(
    documents: list[SourceDocument],
    chunk_size: int = 800,
    overlap: int = 120,
) -> list[tuple[str, str]]:
    all_chunks: list[tuple[str, str]] = []

    for doc in documents:
        cleaned = clean_document(doc)
        chunks = chunk_document(
            cleaned,
            chunk_size=chunk_size,
            overlap=overlap,
        )
        all_chunks.extend([(c.chunk_id, c.text) for c in chunks])

    return all_chunks


def run_enriched(
    cases_path: str,
    output_path: str,
    chunk_size: int = 800,
    overlap: int = 120,
    top_k: int = 3,
) -> None:
    # 1. Charger les documents textuels (Reddit, etc.)
    documents = load_reddit_documents()

    # 2. Construire les chunks
    chunks = build_chunks_from_docs(
        documents,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    # 3. Initialiser l'agent RAG enrichi (texte + SQL)
    db_path = settings.DATABASE_URL.replace("sqlite:///", "data/")
    
    print(f"\n[DEBUG] URL d'origine : {settings.DATABASE_URL}")
    print(f"[DEBUG] Chemin calculé : {db_path}")
    print(f"[DEBUG] Le fichier existe-t-il ? -> {Path(db_path).exists()}\n")
    agent = EnrichedRAGAgent(
        chunks=chunks,
        top_k=top_k,
        database_path=db_path,    
    )

    # 4. Charger les cas de test (questions)
    cases = load_cases(cases_path)

    # 5. Exécuter le RAG enrichi sur chaque question
    results: list[dict[str, Any]] = []

    for case in cases:
        start = time.time()
        response: RAGResponse = agent.ask(
            question=case.question,
            question_id=case.question_id,
        )
        latency_ms = (time.time() - start) * 1000

        response = response.model_copy(update={"latency_ms": latency_ms})

        results.append(response.model_dump())

    # 6. Sauvegarder les réponses en JSONL
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Exécute le prototype RAG enrichi (texte + SQL)."
    )
    parser.add_argument(
        "--cases",
        required=True,
        help="Chemin vers le fichier JSONL des questions (data/evaluation/questions.jsonl).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Chemin de sortie pour les réponses (data/evaluation/answers_after.jsonl).",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=800,
        help="Taille des chunks en caractères.",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=120,
        help="Recouvrement entre chunks en caractères.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Nombre de chunks récupérés par question.",
    )

    args = parser.parse_args()

    # Configuration de l'observabilité (Logfire, Pydantic, etc.)
    configure_observability()

    run_enriched(
        cases_path=args.cases,
        output_path=args.output,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        top_k=args.top_k,
    )


if __name__ == "__main__":
    main()