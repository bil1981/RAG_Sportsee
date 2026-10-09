"""
Évaluation RAGAS 0.4.3 avec Ollama uniquement.

Objectif
--------
Évaluer un système RAG avec :

    LLM :
        Ollama / llama3.1:latest

    Embeddings :
        Ollama / nomic-embed-text:latest

    Évaluation :
        RAGAS 0.4.3

Le script n'utilise directement :
    - ni OpenAI
    - ni Mistral
    - ni langchain_ollama
    - ni langchain_core

Les appels Ollama sont effectués directement via HTTP
sur http://localhost:11434.

IMPORTANT
---------
RAGAS 0.4.3 possède encore des dépendances internes à LangChain.
Cela signifie que LangChain peut apparaître dans la stack trace
interne de RAGAS, même si ce fichier n'importe aucun module LangChain.
"""

from __future__ import annotations

import asyncio
import json
import math
import urllib.error
import urllib.request
from typing import Any


# ============================================================================
# CONFIGURATION
# ============================================================================

OLLAMA_URL = "http://localhost:11434"

LLM_MODEL = "llama3.1:latest"

EMBEDDING_MODEL = "nomic-embed-text:latest"

OLLAMA_TIMEOUT = 300


# ============================================================================
# DATASET DE TEST
# ============================================================================

TEST_DATASET = [
    {
        "question": (
            "Quel joueur a le meilleur pourcentage à 3 points "
            "sur les 5 derniers matchs ?"
        ),
        "ground_truth": (
            "Paul George possède le meilleur pourcentage "
            "avec 45% à 3 points."
        ),
        "response": (
            "Paul George possède le meilleur pourcentage "
            "avec 45% à 3 points."
        ),
        "context": (
            "Sur les 5 derniers matchs, Paul George possède "
            "le meilleur pourcentage à 3 points avec 45%."
        ),
    },
    {
        "question": (
            "Compare l'efficacité défensive de l'équipe "
            "à domicile et à l'extérieur."
        ),
        "ground_truth": (
            "L'équipe concède 102 points à domicile "
            "contre 114 points à l'extérieur."
        ),
        "response": (
            "L'équipe concède 102 points lorsqu'elle joue "
            "à domicile contre 114 points lorsqu'elle joue "
            "à l'extérieur."
        ),
        "context": (
            "L'équipe concède en moyenne 102 points lorsqu'elle "
            "joue à domicile et 114 points lorsqu'elle joue "
            "à l'extérieur."
        ),
    },
    {
        "question": (
            "Combien de paniers le coach a-t-il marqués "
            "pendant le debrief du 12 mars ?"
        ),
        "ground_truth": (
            "L'information n'est pas disponible dans les rapports."
        ),
        "response": (
            "L'information n'est pas disponible dans les rapports."
        ),
        "context": (
            "Les rapports disponibles ne contiennent aucune "
            "information concernant le nombre de paniers marqués "
            "par le coach pendant le debrief du 12 mars."
        ),
    },
]


# ============================================================================
# UTILITAIRE HTTP OLLAMA
# ============================================================================

def ollama_post(
    endpoint: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """
    Effectue une requête POST vers l'API locale Ollama.

    Aucun SDK Ollama ou LangChain n'est utilisé.

    Exemple :
        /api/generate
        /api/embed
    """

    url = f"{OLLAMA_URL}{endpoint}"

    body = json.dumps(
        payload,
        ensure_ascii=False,
    ).encode("utf-8")

    request = urllib.request.Request(
        url=url,
        data=body,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=OLLAMA_TIMEOUT,
        ) as response:

            raw = response.read().decode("utf-8")

            return json.loads(raw)

    except urllib.error.URLError as exc:

        raise RuntimeError(
            "\nImpossible de contacter Ollama.\n\n"
            f"URL : {url}\n"
            "Vérifiez qu'Ollama fonctionne avec :\n"
            "    ollama list\n\n"
            f"Erreur : {exc}"
        ) from exc

    except json.JSONDecodeError as exc:

        raise RuntimeError(
            "\nOllama a retourné une réponse JSON invalide.\n"
            f"Endpoint : {endpoint}\n"
            f"Erreur : {exc}"
        ) from exc


# ============================================================================
# OLLAMA - LLM
# ============================================================================

def ollama_generate(
    prompt: str,
    temperature: float = 0.0,
) -> str:
    """
    Génère une réponse avec llama3.1 via Ollama.

    Endpoint :
        POST /api/generate
    """

    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    result = ollama_post(
        "/api/generate",
        payload,
    )

    response = result.get("response")

    if not response:
        raise RuntimeError(
            "Ollama n'a retourné aucune réponse."
        )

    return response.strip()


# ============================================================================
# OLLAMA - EMBEDDINGS
# ============================================================================

def ollama_embed(
    texts: list[str],
) -> list[list[float]]:
    """
    Génère des embeddings avec nomic-embed-text.

    Endpoint :
        POST /api/embed
    """

    if not texts:
        return []

    payload = {
        "model": EMBEDDING_MODEL,
        "input": texts,
    }

    result = ollama_post(
        "/api/embed",
        payload,
    )

    embeddings = result.get("embeddings")

    if not embeddings:
        raise RuntimeError(
            "Ollama n'a retourné aucun embedding."
        )

    return embeddings


def ollama_embed_one(
    text: str,
) -> list[float]:
    """
    Embedding d'un seul texte.
    """

    result = ollama_embed([text])

    return result[0]


# ============================================================================
# TEST OLLAMA
# ============================================================================

def test_ollama() -> None:
    """
    Vérifie que les deux modèles Ollama fonctionnent.
    """

    print()
    print("=" * 80)
    print("TEST OLLAMA")
    print("=" * 80)

    print(f"URL Ollama       : {OLLAMA_URL}")
    print(f"LLM              : {LLM_MODEL}")
    print(f"Embeddings       : {EMBEDDING_MODEL}")

    # ------------------------------------------------------------------------
    # Test LLM
    # ------------------------------------------------------------------------

    print()
    print("[1/2] Test du LLM...")

    response = ollama_generate(
        "Réponds uniquement par : OLLAMA_LLM_OK"
    )

    print("      ✓ LLM opérationnel")
    print(f"      Réponse : {response[:100]}")

    # ------------------------------------------------------------------------
    # Test embeddings
    # ------------------------------------------------------------------------

    print()
    print("[2/2] Test des embeddings...")

    vector = ollama_embed_one(
        "Ceci est un test d'embedding."
    )

    print("      ✓ Embeddings opérationnels")
    print(
        f"      Dimension du vecteur : {len(vector)}"
    )

    print()
    print("✓ Ollama est opérationnel.")


# ============================================================================
# IMPORT RAGAS
# ============================================================================

def import_ragas():
    """
    Importe les composants RAGAS nécessaires.

    Les imports sont regroupés ici afin que l'on puisse distinguer
    clairement les dépendances RAGAS des appels directs à Ollama.

    Aucun import langchain_core ou langchain_ollama n'est effectué
    par notre code.
    """

    from ragas.dataset_schema import SingleTurnSample

    from ragas.metrics._context_precision import ContextPrecision
    from ragas.metrics._context_recall import ContextRecall
    from ragas.metrics._faithfulness import Faithfulness
    from ragas.metrics._answer_relevance import ResponseRelevancy

    # RAGAS 0.4.3 expose AnswerSimilarity depuis ragas.metrics.
    try:
        from ragas.metrics import AnswerSimilarity
    except ImportError:

        # Compatibilité avec certaines installations 0.4.x
        from ragas.metrics._answer_similarity import (
            AnswerSimilarity,
        )

    return (
        SingleTurnSample,
        ContextPrecision,
        ContextRecall,
        Faithfulness,
        ResponseRelevancy,
        AnswerSimilarity,
    )


# ============================================================================
# ÉVALUATION DIRECTE
# ============================================================================

def evaluate_with_ollama() -> None:
    """
    Lance l'évaluation RAGAS.

    NOTE IMPORTANTE :

    RAGAS 0.4.3 attend un objet LLM et un objet embeddings conformes
    à ses abstractions internes.

    Pour éviter tout LangChain dans NOTRE fichier, on utilise ici
    des adaptateurs minimalistes.

    Si RAGAS 0.4.3 de ton environnement impose ses classes
    BaseRagasLLM/BaseRagasEmbeddings, ces classes seront importées
    depuis RAGAS, pas depuis LangChain.
    """

    (
        SingleTurnSample,
        ContextPrecision,
        ContextRecall,
        Faithfulness,
        ResponseRelevancy,
        AnswerSimilarity,
    ) = import_ragas()

    # ------------------------------------------------------------------------
    # Adaptateur LLM RAGAS
    # ------------------------------------------------------------------------

    from ragas.llms.base import BaseRagasLLM

    class OllamaLLM(BaseRagasLLM):
        """
        Adaptateur RAGAS -> Ollama.

        RAGAS appelle generate_text().
        Cette méthode appelle directement Ollama.
        """

        def generate_text(
            self,
            prompt,
            n=1,
            temperature=0.01,
            stop=None,
            callbacks=None,
        ):
            """
            Génération synchrone.

            Cette méthode doit retourner l'objet attendu par RAGAS.
            """

            # Import local de l'objet RAGAS/LangChain utilisé
            # uniquement pour transporter le résultat.
            from langchain_core.outputs import Generation, LLMResult

            if hasattr(prompt, "to_string"):
                prompt_text = prompt.to_string()
            else:
                prompt_text = str(prompt)

            generations = []

            for _ in range(n):

                text = ollama_generate(
                    prompt_text,
                    temperature=temperature,
                )

                if stop:

                    for stop_token in stop:

                        if stop_token in text:

                            text = text.split(
                                stop_token
                            )[0]

                generations.append(
                    Generation(
                        text=text
                    )
                )

            return LLMResult(
                generations=[
                    generations
                ]
            )

        async def agenerate_text(
            self,
            prompt,
            n=1,
            temperature=0.01,
            stop=None,
            callbacks=None,
        ):
            """
            Génération asynchrone.

            L'appel HTTP Ollama est exécuté dans un thread
            afin de ne pas bloquer asyncio.
            """

            return await asyncio.to_thread(
                self.generate_text,
                prompt,
                n,
                temperature,
                stop,
                callbacks,
            )

        def is_finished(
            self,
            response,
        ):
            """
            Vérifie que RAGAS a reçu une génération non vide.
            """

            try:

                return bool(
                    response.generations
                    and response.generations[0]
                    and response.generations[0][0].text
                )

            except (
                AttributeError,
                IndexError,
            ):

                return False

    # ------------------------------------------------------------------------
    # Adaptateur embeddings RAGAS
    # ------------------------------------------------------------------------

    from ragas.embeddings.base import BaseRagasEmbeddings

    class OllamaEmbeddings(BaseRagasEmbeddings):
        """
        Adaptateur RAGAS -> Ollama embeddings.
        """

        def __init__(self):
            super().__init__()

        def embed_query(
            self,
            text: str,
        ) -> list[float]:

            return ollama_embed_one(text)

        def embed_documents(
            self,
            texts: list[str],
        ) -> list[list[float]]:

            return ollama_embed(texts)

        async def aembed_query(
            self,
            text: str,
        ) -> list[float]:

            return await asyncio.to_thread(
                self.embed_query,
                text,
            )

        async def aembed_documents(
            self,
            texts: list[str],
        ) -> list[list[float]]:

            return await asyncio.to_thread(
                self.embed_documents,
                texts,
            )

    # ------------------------------------------------------------------------
    # Instanciation
    # ------------------------------------------------------------------------

    llm = OllamaLLM()

    embeddings = OllamaEmbeddings()

    print()
    print("=" * 80)
    print("INITIALISATION RAGAS")
    print("=" * 80)

    print(
        "LLM         : Ollama / llama3.1:latest"
    )

    print(
        "Embeddings  : Ollama / nomic-embed-text:latest"
    )

    # ------------------------------------------------------------------------
    # Métriques
    # ------------------------------------------------------------------------

    metrics = [
        (
            "Context Precision",
            ContextPrecision(
                llm=llm
            ),
        ),
        (
            "Context Recall",
            ContextRecall(
                llm=llm
            ),
        ),
        (
            "Faithfulness",
            Faithfulness(
                llm=llm
            ),
        ),
        (
            "Response Relevancy",
            ResponseRelevancy(
                llm=llm,
                embeddings=embeddings,
            ),
        ),
        (
            "Answer Similarity",
            AnswerSimilarity(
                embeddings=embeddings,
            ),
        ),
    ]

    print()

    for name, _ in metrics:
        print(f"✓ {name}")

    # ------------------------------------------------------------------------
    # Évaluation
    # ------------------------------------------------------------------------

    all_results = []

    print()
    print("=" * 80)
    print("ÉVALUATION")
    print("=" * 80)

    for index, item in enumerate(
        TEST_DATASET,
        start=1,
    ):

        print()
        print(
            f"TEST {index}/{len(TEST_DATASET)}"
        )

        print(
            f"Question : {item['question']}"
        )

        sample = SingleTurnSample(
            user_input=item["question"],
            response=item["response"],
            reference=item["ground_truth"],
            retrieved_contexts=[
                item["context"]
            ],
        )

        row = {
            "test": index,
            "question": item["question"],
        }

        for metric_name, metric in metrics:

            print(
                f"  {metric_name}...",
                end=" ",
                flush=True,
            )

            try:

                # RAGAS 0.4.x utilise cette méthode pour
                # scorer un SingleTurnSample.
                score = metric.single_turn_ascore(
                    sample
                )

                # Certaines configurations peuvent retourner
                # une coroutine.
                if hasattr(
                    score,
                    "__await__",
                ):

                    score = asyncio.run(
                        score
                    )

                score = float(score)

                row[
                    metric_name
                ] = score

                print(
                    f"✓ {score:.4f}"
                )

            except Exception as exc:

                row[
                    metric_name
                ] = math.nan

                print(
                    "✗ ERREUR"
                )

                print(
                    f"      {type(exc).__name__}: {exc}"
                )

        all_results.append(row)

    # ------------------------------------------------------------------------
    # Moyennes
    # ------------------------------------------------------------------------

    metric_names = [
        "Context Precision",
        "Context Recall",
        "Faithfulness",
        "Response Relevancy",
        "Answer Similarity",
    ]

    averages = {}

    for metric_name in metric_names:

        values = [
            row[metric_name]
            for row in all_results
            if not math.isnan(
                row[metric_name]
            )
        ]

        if values:

            averages[metric_name] = (
                sum(values) / len(values)
            )

        else:

            averages[metric_name] = math.nan

    # ------------------------------------------------------------------------
    # Affichage final
    # ------------------------------------------------------------------------

    print()
    print("=" * 80)
    print("RÉSULTATS RAGAS")
    print("=" * 80)

    for row in all_results:

        print()
        print(
            f"TEST {row['test']}"
        )

        print(
            f"Question : {row['question']}"
        )

        for metric_name in metric_names:

            value = row[metric_name]

            if math.isnan(value):

                print(
                    f"  {metric_name:<22} : NaN"
                )

            else:

                print(
                    f"  {metric_name:<22} : "
                    f"{value:.4f}"
                )

    print()
    print("=" * 80)
    print("MOYENNES")
    print("=" * 80)

    for metric_name in metric_names:

        value = averages[metric_name]

        if math.isnan(value):

            print(
                f"{metric_name:<22} : NaN"
            )

        else:

            print(
                f"{metric_name:<22} : "
                f"{value:.4f}"
            )

    print("=" * 80)

    # ------------------------------------------------------------------------
    # Sauvegarde JSON
    # ------------------------------------------------------------------------

    output = {
        "configuration": {
            "ragas": "0.4.3",
            "provider": "Ollama",
            "llm": LLM_MODEL,
            "embeddings": EMBEDDING_MODEL,
            "ollama_url": OLLAMA_URL,
        },
        "results": all_results,
        "averages": averages,
    }

    output_file = (
        "ragas_results_ollama1.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            output,
            file,
            ensure_ascii=False,
            indent=4,
            allow_nan=True,
        )

    print()
    print(
        f"Résultats sauvegardés dans : "
        f"{output_file}"
    )


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:

    print()
    print("=" * 80)
    print("RAGAS 0.4.3 + OLLAMA")
    print("=" * 80)

    print()
    print("Configuration :")
    print(f"  Ollama      : {OLLAMA_URL}")
    print(f"  LLM         : {LLM_MODEL}")
    print(
        f"  Embeddings  : {EMBEDDING_MODEL}"
    )
    print("  OpenAI      : NON")
    print("  Mistral     : NON")
    print("  LangChain Ollama : NON")

    # ------------------------------------------------------------------------
    # Vérification Ollama
    # ------------------------------------------------------------------------

    test_ollama()

    # ------------------------------------------------------------------------
    # Évaluation RAGAS
    # ------------------------------------------------------------------------

    evaluate_with_ollama()

    print()
    print(
        "✓ Évaluation terminée."
    )


if __name__ == "__main__":
    main()