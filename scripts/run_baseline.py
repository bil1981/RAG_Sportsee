# scripts/run_baseline.py
"""
Exécute le prototype RAG de base (texte seul) sur le jeu de questions
et sauvegarde les réponses au format JSONL pour évaluation RAGAS.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any
import pypdf  # ← à importer ici

from sportsee.config import settings
from sportsee.logging_config import configure_observability
from sportsee.rag.agent import SimpleRAGAgent
from sportsee.rag.chunking import chunk_document
from sportsee.rag.clean import clean_document
from sportsee.evaluation.dataset import load_cases
from sportsee.schemas import RAGResponse, SourceDocument

"""
Exécute le prototype RAG de base (texte seul) sur le jeu de questions
et sauvegarde les réponses au format JSONL pour évaluation RAGAS.
"""

def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extrait le texte d'un fichier PDF.
    Utilise pypdf ; à adapter si tu utilises une autre librairie.
    """
    reader = pypdf.PdfReader(str(pdf_path))
    text_parts = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_parts.append(text)

    return "\n".join(text_parts)

def load_reddit_documents() -> list[SourceDocument]:
    """
    Charge les commentaires de matchs (PDF Reddit 1–4) et les retourne
    comme une liste de SourceDocument.

    À adapter selon ton vrai pipeline d'ingestion (lecture PDF, parsing, etc.).
    Ici, on met un squelette à compléter.
    """
    documents: list[SourceDocument] = []

    # Exemple de structure attendue :
    # - data/raw/reddit/Reddit 1 (1).pdf
    # - data/raw/reddit/Reddit 2 (1).pdf
    # - ...
    # Pseudo-code à remplacer par ton vrai chargement :
    for pdf_path in Path("./inputs").glob("Reddit*.pdf"):
        print(f"[INFO0] Loading PDF: {pdf_path}")
        text = extract_text_from_pdf(pdf_path)  # à implémenter
        documents.append(
            SourceDocument(
                document_id=pdf_path.stem,
                source="reddit",
                text=text,
                metadata={"file": str(pdf_path)},
            )
        )

    # Si aucun document n’est trouvé, on peut soit lever une erreur,
    # soit utiliser un document factice pour tester le pipeline.
    if not documents:
        print ("[WARNING] Aucun document Reddit trouvé. Utilisation d'un document factice pour test.")
        # Option 1 : document factice pour que le script tourne en test
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
    """
    Nettoie et découpe une liste de documents en chunks.
    Retourne une liste de (chunk_id, text).
    """
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


def run_baseline(
    cases_path: str,
    output_path: str,
    chunk_size: int = 800,
    overlap: int = 120,
    top_k: int = 3,
) -> None:
    # 1. Charger les documents textuels (Reddit, etc.)
    documents = load_reddit_documents()
    print(f"[INFO1] Loaded {len(documents)} document(s).")
    print(f"[INFO2] Documents: {documents}")

    # 2. Construire les chunks
    chunks = build_chunks_from_docs(
        documents,
        chunk_size=chunk_size,
        overlap=overlap,
    )
    print(f"[INFO3] Built {len(chunks)} chunk(s).")

    if not chunks:
        raise RuntimeError(
            "Aucun chunk disponible pour le RAG. "
            "Vérifie load_reddit_documents() et le dossier ./inputs."
        )

    # 3. Initialiser l'agent RAG de base
    agent = SimpleRAGAgent(
        chunks=chunks,
        top_k=top_k,
    )

    # 4. Charger les cas de test (questions)
    cases = load_cases(cases_path)
    print(f"[INFO4] Loaded {len(cases)} question(s).")

    # 5. Exécuter le RAG sur chaque question et collecter les réponses
    results: list[dict[str, Any]] = []

    for i, case in enumerate(cases):
        question = case.question
        question_id = getattr(case, "id", None) or getattr(case, "question_id", f"case_{i}")

        print(f"[{i+1}/{len(cases)}] case_id={question_id}")
        print(f"  question={question!r}")

        if not question or not question.strip():
            print(f"  SKIP: question vide")
            continue

        start = time.time()
        response: RAGResponse = agent.ask(
            question=question,
            question_id=str(question_id),
        )
        latency_ms = (time.time() - start) * 1000

        response = response.model_copy(update={"latency_ms": latency_ms})

        results.append(response.model_dump())
        print(f"  OK: len(answer)={len(response.answer)}")

    # 6. Sauvegarder les réponses en JSONL
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"[INFO5] Saved {len(results)} response(s) to {output_path}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Exécute le prototype RAG de base (texte seul)."
    )
    parser.add_argument(
        "--cases",
        required=True,
        help="Chemin vers le fichier JSONL des questions (data/evaluation/questions.jsonl).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Chemin de sortie pour les réponses (data/evaluation/answers_before.jsonl).",
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

    run_baseline(
        cases_path=args.cases,
        output_path=args.output,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        top_k=args.top_k,
    )


if __name__ == "__main__":
    main()