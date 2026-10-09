"""
Évaluation RAGAS 0.4.3 avec Ollama uniquement.

Architecture :

    Dataset de test
          │
          ├── question
          ├── réponse attendue
          ├── réponse générée
          └── contexte récupéré
                  │
                  ▼
              RAGAS 0.4.3
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
  Ollama LLM          Ollama Embeddings
  llama3.1:latest     nomic-embed-text:latest
        │                   │
        └─────────┬─────────┘
                  ▼
             5 métriques
                  │
                  ▼
          Résultats + moyenne

IMPORTANT :
- Aucun appel OpenAI.
- Aucun appel Mistral.
- Aucun ChatOllama / OllamaEmbeddings de LangChain.
- Appels directs à l'API locale Ollama.
"""

from __future__ import annotations

import asyncio
import json
import math
import urllib.error
import urllib.request
from typing import Any, Optional

from langchain_core.outputs import Generation, LLMResult
from langchain_core.prompt_values import PromptValue

from ragas.dataset_schema import SingleTurnSample
from ragas.embeddings.base import BaseRagasEmbeddings
from ragas.llms.base import BaseRagasLLM
from ragas.metrics._answer_relevance import ResponseRelevancy
from ragas.metrics._answer_similarity import AnswerSimilarity
from ragas.metrics._context_precision import ContextPrecision
from ragas.metrics._context_recall import ContextRecall
from ragas.metrics._faithfulness import Faithfulness
from ragas.run_config import RunConfig


# ============================================================================
# 1. CONFIGURATION OLLAMA
# ============================================================================

OLLAMA_BASE_URL = "http://localhost:11434"

# Modèle utilisé comme "juge" par RAGAS.
OLLAMA_LLM_MODEL = "llama3.1:latest"

# Modèle utilisé pour les calculs de similarité sémantique.
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text:latest"

# Timeout HTTP en secondes.
OLLAMA_TIMEOUT = 300

# Température volontairement faible pour rendre l'évaluation
# aussi déterministe que possible.
OLLAMA_TEMPERATURE = 0.0


# ============================================================================
# 2. FONCTION GÉNÉRIQUE D'APPEL À OLLAMA
# ============================================================================

def ollama_request(
    endpoint: str,
    payload: dict[str, Any],
    timeout: int = OLLAMA_TIMEOUT,
) -> dict[str, Any]:
    """
    Envoie une requête HTTP POST à l'API locale Ollama.

    Exemple :
        POST http://localhost:11434/api/generate

    ou :
        POST http://localhost:11434/api/embed
    """

    url = f"{OLLAMA_BASE_URL}{endpoint}"

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        url=url,
        data=data,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:

            response_data = response.read().decode("utf-8")

            return json.loads(response_data)

    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"\nImpossible de contacter Ollama.\n"
            f"URL : {url}\n"
            f"Vérifiez que Ollama fonctionne avec : ollama list\n"
            f"Erreur : {exc}"
        ) from exc

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"\nOllama a retourné une réponse JSON invalide.\n"
            f"Endpoint : {url}\n"
            f"Erreur : {exc}"
        ) from exc


# ============================================================================
# 3. LLM RAGAS BASÉ SUR OLLAMA
# ============================================================================

class OllamaRagasLLM(BaseRagasLLM):
    """
    Adaptateur permettant à RAGAS d'utiliser Ollama comme LLM.

    RAGAS demande à un LLM de réaliser différents jugements :
    - fidélité de la réponse ;
    - précision du contexte ;
    - rappel du contexte ;
    - pertinence de la réponse.

    Au lieu de passer par LangChain/Ollama, nous appelons directement
    l'API locale Ollama.
    """

    model: str = OLLAMA_LLM_MODEL

    def __init__(
        self,
        model: str = OLLAMA_LLM_MODEL,
        run_config: Optional[RunConfig] = None,
    ):
        super().__init__(
            run_config=run_config or RunConfig(
                timeout=OLLAMA_TIMEOUT,
                max_retries=2,
            )
        )

        self.model = model

    # ------------------------------------------------------------------------
    # Conversion d'un PromptValue RAGAS vers du texte
    # ------------------------------------------------------------------------

    @staticmethod
    def _prompt_to_text(prompt: Any) -> str:
        """
        RAGAS peut fournir différents types de PromptValue.

        Cette fonction transforme le prompt en texte exploitable par Ollama.
        """

        if hasattr(prompt, "to_string"):
            return prompt.to_string()

        if isinstance(prompt, str):
            return prompt

        return str(prompt)

    # ------------------------------------------------------------------------
    # Appel synchrone
    # ------------------------------------------------------------------------

    def _generate(
        self,
        prompt: Any,
        temperature: float = OLLAMA_TEMPERATURE,
    ) -> str:
        """
        Appel direct à /api/generate.
        """

        prompt_text = self._prompt_to_text(prompt)

        payload = {
            "model": self.model,
            "prompt": prompt_text,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        result = ollama_request(
            endpoint="/api/generate",
            payload=payload,
        )

        if "response" not in result:
            raise RuntimeError(
                "Réponse Ollama invalide : champ 'response' absent."
            )

        return result["response"]

    # ------------------------------------------------------------------------
    # Méthode attendue par BaseRagasLLM
    # ------------------------------------------------------------------------

    def generate_text(
        self,
        prompt: PromptValue,
        n: int = 1,
        temperature: float = OLLAMA_TEMPERATURE,
        stop: Optional[list[str]] = None,
        callbacks: Any = None,
    ) -> LLMResult:
        """
        Génération synchrone compatible RAGAS.

        RAGAS attend un LLMResult contenant des Generation.
        """

        generations = []

        for _ in range(n):

            text = self._generate(
                prompt=prompt,
                temperature=temperature,
            )

            # Gestion simple des éventuels stop tokens.
            if stop:
                for stop_token in stop:
                    if stop_token in text:
                        text = text.split(stop_token)[0]

            generations.append(
                Generation(text=text)
            )

        return LLMResult(
            generations=[generations]
        )

    # ------------------------------------------------------------------------
    # Méthode asynchrone
    # ------------------------------------------------------------------------

    async def agenerate_text(
        self,
        prompt: PromptValue,
        n: int = 1,
        temperature: Optional[float] = OLLAMA_TEMPERATURE,
        stop: Optional[list[str]] = None,
        callbacks: Any = None,
    ) -> LLMResult:
        """
        Version asynchrone.

        L'appel HTTP étant local, on utilise asyncio.to_thread()
        afin de ne pas bloquer la boucle asyncio.
        """

        temperature = (
            OLLAMA_TEMPERATURE
            if temperature is None
            else temperature
        )

        tasks = [
            asyncio.to_thread(
                self._generate,
                prompt,
                temperature,
            )
            for _ in range(n)
        ]

        responses = await asyncio.gather(*tasks)

        generations = []

        for text in responses:

            if stop:
                for stop_token in stop:
                    if stop_token in text:
                        text = text.split(stop_token)[0]

            generations.append(
                Generation(text=text)
            )

        return LLMResult(
            generations=[generations]
        )

    # ------------------------------------------------------------------------
    # Vérification de fin de génération
    # ------------------------------------------------------------------------

    def is_finished(
        self,
        response: LLMResult,
    ) -> bool:
        """
        Ollama retourne ici une génération complète car stream=False.

        On considère donc la génération terminée si elle contient
        au moins un texte.
        """

        try:
            return bool(
                response.generations
                and response.generations[0]
                and response.generations[0][0].text
            )
        except (AttributeError, IndexError):
            return False


# ============================================================================
# 4. EMBEDDINGS RAGAS BASÉS SUR OLLAMA
# ============================================================================

class OllamaRagasEmbeddings(BaseRagasEmbeddings):
    """
    Adaptateur permettant à RAGAS d'utiliser
    nomic-embed-text via l'API Ollama.

    Endpoint :
        POST /api/embed
    """

    def __init__(
        self,
        model: str = OLLAMA_EMBEDDING_MODEL,
    ):
        super().__init__()

        self.model = model

    # ------------------------------------------------------------------------
    # Embedding d'un texte
    # ------------------------------------------------------------------------

    def _embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Appelle Ollama /api/embed pour un texte.
        """

        payload = {
            "model": self.model,
            "input": text,
        }

        result = ollama_request(
            endpoint="/api/embed",
            payload=payload,
        )

        embeddings = result.get("embeddings")

        if not embeddings:
            raise RuntimeError(
                "Réponse Ollama invalide : "
                "champ 'embeddings' absent ou vide."
            )

        return embeddings[0]

    # ------------------------------------------------------------------------
    # API RAGAS - requête unique
    # ------------------------------------------------------------------------

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        """
        Embedding d'une question.
        """

        return self._embed_text(text)

    # ------------------------------------------------------------------------
    # API RAGAS - documents
    # ------------------------------------------------------------------------

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Embedding de plusieurs textes.

        Ollama accepte directement une liste avec /api/embed.
        """

        if not texts:
            return []

        payload = {
            "model": self.model,
            "input": texts,
        }

        result = ollama_request(
            endpoint="/api/embed",
            payload=payload,
        )

        embeddings = result.get("embeddings")

        if not embeddings:
            raise RuntimeError(
                "Réponse Ollama invalide : "
                "champ 'embeddings' absent ou vide."
            )

        return embeddings

    # ------------------------------------------------------------------------
    # Version asynchrone - requête
    # ------------------------------------------------------------------------

    async def aembed_query(
        self,
        text: str,
    ) -> list[float]:
        """
        Version asynchrone de embed_query().
        """

        return await asyncio.to_thread(
            self.embed_query,
            text,
        )

    # ------------------------------------------------------------------------
    # Version asynchrone - documents
    # ------------------------------------------------------------------------

    async def aembed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Version asynchrone de embed_documents().
        """

        return await asyncio.to_thread(
            self.embed_documents,
            texts,
        )


# ============================================================================
# 5. DATASET DE TEST
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
# 6. TEST DE CONNEXION OLLAMA
# ============================================================================

def test_ollama() -> None:
    """
    Vérifie les deux composants Ollama avant de lancer RAGAS :

    1. LLM llama3.1
    2. Embeddings nomic-embed-text
    """

    print("=" * 80)
    print("TEST DE CONNEXION OLLAMA")
    print("=" * 80)

    print(f"\nLLM        : {OLLAMA_LLM_MODEL}")
    print(f"Embeddings : {OLLAMA_EMBEDDING_MODEL}")
    print(f"URL        : {OLLAMA_BASE_URL}")

    # ------------------------------------------------------------------------
    # Test LLM
    # ------------------------------------------------------------------------

    print("\n[1/2] Test du LLM Ollama...")

    llm = OllamaRagasLLM()

    response = llm._generate(
        "Réponds simplement : OLLAMA_TEST_OK"
    )

    if not response:
        raise RuntimeError(
            "Ollama a retourné une réponse vide."
        )

    print("      OK")
    print(f"      Réponse : {response[:150]!r}")

    # ------------------------------------------------------------------------
    # Test embeddings
    # ------------------------------------------------------------------------

    print("\n[2/2] Test des embeddings Ollama...")

    embeddings = OllamaRagasEmbeddings()

    vector = embeddings.embed_query(
        "Ceci est un test d'embedding."
    )

    if not vector:
        raise RuntimeError(
            "Ollama n'a pas retourné de vecteur."
        )

    print("      OK")
    print(f"      Dimension du vecteur : {len(vector)}")

    print("\nOllama est opérationnel.\n")


# ============================================================================
# 7. CRÉATION DES MÉTRIQUES RAGAS
# ============================================================================

def create_metrics():
    """
    Crée les cinq métriques RAGAS.

    Toutes les métriques utilisant un LLM utilisent llama3.1.

    La pertinence et la similarité sémantique utilisent également
    nomic-embed-text.
    """

    llm = OllamaRagasLLM(
        model=OLLAMA_LLM_MODEL,
        run_config=RunConfig(
            timeout=OLLAMA_TIMEOUT,
            max_retries=2,
        ),
    )

    embeddings = OllamaRagasEmbeddings(
        model=OLLAMA_EMBEDDING_MODEL,
    )

    metrics = {
        "context_precision": ContextPrecision(
            llm=llm,
        ),
        "context_recall": ContextRecall(
            llm=llm,
        ),
        "faithfulness": Faithfulness(
            llm=llm,
        ),
        "response_relevancy": ResponseRelevancy(
            llm=llm,
            embeddings=embeddings,
        ),
        "answer_similarity": AnswerSimilarity(
            embeddings=embeddings,
        ),
    }

    return metrics


# ============================================================================
# 8. ÉVALUATION D'UN ÉCHANTILLON
# ============================================================================

def evaluate_sample(
    sample_data: dict[str, Any],
    metrics: dict[str, Any],
) -> dict[str, Any]:
    """
    Évalue une ligne du dataset avec les cinq métriques.

    Nous utilisons SingleTurnSample, qui correspond au format
    attendu par les métriques legacy de RAGAS 0.4.3.
    """

    sample = SingleTurnSample(
        user_input=sample_data["question"],
        response=sample_data["response"],
        reference=sample_data["ground_truth"],
        retrieved_contexts=[
            sample_data["context"]
        ],
    )

    result = {
        "question": sample_data["question"],
    }

    for metric_name, metric in metrics.items():

        print(
            f"      → {metric_name}...",
            end=" ",
            flush=True,
        )

        try:

            # single_turn_ascore() est la méthode adaptée
            # aux métriques legacy de RAGAS.
            score = metric.single_turn_ascore(sample)

            # Certaines versions renvoient directement le float,
            # d'autres peuvent renvoyer une valeur convertible.
            if hasattr(score, "__await__"):
                score = asyncio.run(score)

            if hasattr(score, "value"):
                score = score.value

            result[metric_name] = float(score)

            print(
                f"OK ({result[metric_name]:.4f})"
            )

        except Exception as exc:

            print(
                f"ERREUR : {type(exc).__name__}: {exc}"
            )

            result[metric_name] = math.nan

    return result


# ============================================================================
# 9. CALCUL DES MOYENNES
# ============================================================================

def calculate_averages(
    results: list[dict[str, Any]],
) -> dict[str, float]:
    """
    Calcule la moyenne de chaque métrique en ignorant les NaN.
    """

    metric_names = [
        "context_precision",
        "context_recall",
        "faithfulness",
        "response_relevancy",
        "answer_similarity",
    ]

    averages = {}

    for metric_name in metric_names:

        values = [
            row[metric_name]
            for row in results
            if not math.isnan(row[metric_name])
        ]

        if values:
            averages[metric_name] = sum(values) / len(values)
        else:
            averages[metric_name] = math.nan

    return averages


# ============================================================================
# 10. AFFICHAGE DES RÉSULTATS
# ============================================================================

def print_results(
    results: list[dict[str, Any]],
    averages: dict[str, float],
) -> None:
    """
    Affiche les résultats sous une forme lisible pour une capture d'écran.
    """

    print("\n")
    print("=" * 80)
    print("RÉSULTATS RAGAS")
    print("=" * 80)

    for index, row in enumerate(results, start=1):

        print(f"\nTEST {index}")
        print("-" * 80)

        print(
            f"Question : {row['question']}"
        )

        print(
            f"Context Precision : "
            f"{row['context_precision']:.4f}"
        )

        print(
            f"Context Recall    : "
            f"{row['context_recall']:.4f}"
        )

        print(
            f"Faithfulness      : "
            f"{row['faithfulness']:.4f}"
        )

        print(
            f"Response Relevancy: "
            f"{row['response_relevancy']:.4f}"
        )

        print(
            f"Answer Similarity : "
            f"{row['answer_similarity']:.4f}"
        )

    print("\n")
    print("=" * 80)
    print("MOYENNES")
    print("=" * 80)

    for metric_name, value in averages.items():

        if math.isnan(value):
            print(
                f"{metric_name:<22} : NaN"
            )
        else:
            print(
                f"{metric_name:<22} : {value:.4f}"
            )

    print("=" * 80)


# ============================================================================
# 11. SAUVEGARDE JSON
# ============================================================================

def save_results(
    results: list[dict[str, Any]],
    averages: dict[str, float],
    filename: str = "ragas_results_ollama.json",
) -> None:
    """
    Sauvegarde les résultats pour conserver une trace de l'évaluation.
    """

    output = {
        "configuration": {
            "ragas": "0.4.3",
            "llm_provider": "Ollama",
            "llm_model": OLLAMA_LLM_MODEL,
            "embedding_provider": "Ollama",
            "embedding_model": OLLAMA_EMBEDDING_MODEL,
            "ollama_url": OLLAMA_BASE_URL,
        },
        "results": results,
        "averages": averages,
    }

    with open(
        filename,
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

    print(
        f"\nRésultats sauvegardés dans : {filename}"
    )


# ============================================================================
# 12. PROGRAMME PRINCIPAL
# ============================================================================

def main() -> None:
    """
    Point d'entrée principal.
    """

    print("\n")
    print("=" * 80)
    print("ÉVALUATION RAGAS 0.4.3 + OLLAMA")
    print("=" * 80)

    print(
        "\nConfiguration :"
        f"\n  RAGAS       : 0.4.3"
        f"\n  LLM         : {OLLAMA_LLM_MODEL}"
        f"\n  Embeddings  : {OLLAMA_EMBEDDING_MODEL}"
        f"\n  Ollama      : {OLLAMA_BASE_URL}"
    )

    # ------------------------------------------------------------------------
    # Étape 1 : vérifier Ollama
    # ------------------------------------------------------------------------

    test_ollama()

    # ------------------------------------------------------------------------
    # Étape 2 : créer les métriques
    # ------------------------------------------------------------------------

    print("=" * 80)
    print("INITIALISATION DES MÉTRIQUES RAGAS")
    print("=" * 80)

    metrics = create_metrics()

    for name in metrics:
        print(f"  ✓ {name}")

    # ------------------------------------------------------------------------
    # Étape 3 : évaluation
    # ------------------------------------------------------------------------

    print("\n")
    print("=" * 80)
    print("ÉVALUATION DU DATASET")
    print("=" * 80)

    results = []

    for index, sample in enumerate(
        TEST_DATASET,
        start=1,
    ):

        print(
            f"\nTEST {index}/{len(TEST_DATASET)}"
        )

        result = evaluate_sample(
            sample_data=sample,
            metrics=metrics,
        )

        results.append(result)

    # ------------------------------------------------------------------------
    # Étape 4 : moyennes
    # ------------------------------------------------------------------------

    averages = calculate_averages(
        results
    )

    # ------------------------------------------------------------------------
    # Étape 5 : affichage
    # ------------------------------------------------------------------------

    print_results(
        results,
        averages,
    )

    # ------------------------------------------------------------------------
    # Étape 6 : sauvegarde
    # ------------------------------------------------------------------------

    save_results(
        results,
        averages,
    )

    print(
        "\nÉvaluation terminée."
    )

# ============================================================================
# 12. SAUVEGARDE CSV
# ============================================================================

def save_results_csv(
    results: list[dict[str, Any]],
    averages: dict[str, float],
    filename: str = "ragas_results_ollama2.csv",
) -> None:
    """
    Sauvegarde les résultats RAGAS dans un fichier CSV.

    Une ligne correspond à un test.
    Une dernière ligne contient les moyennes.
    """

    fieldnames = [
        "test",
        "question",
        "context_precision",
        "context_recall",
        "faithfulness",
        "response_relevancy",
        "answer_similarity",
    ]

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        # Résultats individuels
        for index, row in enumerate(results, start=1):

            writer.writerow(
                {
                    "test": f"TEST_{index}",
                    "question": row["question"],
                    "context_precision": row["context_precision"],
                    "context_recall": row["context_recall"],
                    "faithfulness": row["faithfulness"],
                    "response_relevancy": row["response_relevancy"],
                    "answer_similarity": row["answer_similarity"],
                }
            )

        # Moyennes
        writer.writerow(
            {
                "test": "MOYENNE",
                "question": "",
                "context_precision": averages["context_precision"],
                "context_recall": averages["context_recall"],
                "faithfulness": averages["faithfulness"],
                "response_relevancy": averages["response_relevancy"],
                "answer_similarity": averages["answer_similarity"],
            }
        )

    print(
        f"Résultats CSV sauvegardés dans : {filename}"
    )
# ============================================================================
# 13. LANCEMENT
# ============================================================================

if __name__ == "__main__":
    main()