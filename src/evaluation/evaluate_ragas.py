# src/sportsee/evaluation/evaluate_ragas.py
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import AspectCritic

from sportsee.schemas import EvaluationCase, RAGResponse
from sportsee.evaluation.ragas_config import get_ollama_llm_for_ragas


def load_cases(path: str) -> list[EvaluationCase]:
    cases = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            if line.strip():
                cases.append(EvaluationCase.model_validate_json(line))
    return cases


def load_responses(path: str) -> list[RAGResponse]:
    responses = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            if line.strip():
                responses.append(RAGResponse.model_validate_json(line))
    return responses


def build_dataset(
    cases: list[EvaluationCase], responses: list[RAGResponse]
) -> Dataset:
    response_by_id = {item.question: item for item in responses}
    rows = []

    for case in cases:
        response = response_by_id[case.question]
        rows.append(
            {
                "question": case.question,
                "answer": response.answer,
                "contexts": response.contexts,
                "ground_truth": case.ground_truth,
                "category": case.category,
            }
        )

    return Dataset.from_list(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True)
    parser.add_argument("--responses", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    # Initialiser le LLM Ollama pour RAGAS
    llm = get_ollama_llm_for_ragas()

    cases = load_cases(args.cases)
    responses = load_responses(args.responses)
    dataset = build_dataset(cases, responses)

    # Utiliser AspectCritic (métrique officielle supportée)
    # On peut définir plusieurs critères si besoin
    metrics = [
        AspectCritic(
            name="faithfulness",
            llm=llm,
            definition=(
                "La réponse est fidèle aux contextes fournis : "
                "elle n'invente pas d'informations et s'appuie sur les contextes."
            ),
        ),
        AspectCritic(
            name="answer_relevancy",
            llm=llm,
            definition=(
                "La réponse est pertinente par rapport à la question posée : "
                "elle ne dévie pas du sujet et fournit des informations utiles."
            ),
        ),
        AspectCritic(
            name="context_precision",
            llm=llm,
            definition=(
                "La réponse utilise les contextes fournis : "
                "elle inclut les informations pertinentes des contextes."
            ),
        ),
        AspectCritic(
            name="ground_truth_consistency",
            llm=llm,
            definition=(
                "La réponse est cohérente avec la ground_truth : "
                "elle ne la contredit pas sur les faits principaux."
            ),
        ),
    ]

    result = evaluate(
        dataset,
        metrics=metrics,
        llm=llm,
    )

    result_df = result.to_pandas()
    result_df.to_csv(args.output, index=False)

    print(result)


if __name__ == "__main__":
    main()