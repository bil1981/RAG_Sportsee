# src/sportsee/evaluation/dataset.py
"""
Chargement du jeu de questions (JSONL) pour l'évaluation.
"""
from __future__ import annotations

from sportsee.schemas import EvaluationCase


def load_cases(path: str) -> list[EvaluationCase]:
    cases: list[EvaluationCase] = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cases.append(EvaluationCase.model_validate_json(line))

    return cases