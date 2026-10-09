import os
import logging

import pandas as pd
from datasets import Dataset
from dotenv import load_dotenv

# Imports LangChain pour Ollama
from langchain_ollama import ChatOllama, OllamaEmbeddings

# Wrapper Ragas pour LangChain
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

# Importation des métriques
from ragas.metrics._context_precision import ContextPrecision
from ragas.metrics._context_recall import ContextRecall
from ragas.metrics._faithfulness import Faithfulness
from ragas.metrics._answer_relevance import ResponseRelevancy
from ragas.metrics import _AnswerSimilarity

import logfire

logfire.configure(send_to_logfire=False)

# ============================================================================
# 1. CONFIGURATION LOGS & ENV
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

load_dotenv()

print("\n=== INITIALISATION OLLAMA / RAGAS ===")

# ============================================================================
# 2. CLIENTS OLLAMA (LLM ET EMBEDDINGS LOCAL)
# ============================================================================

# Modèle de jugement (LLM) avec temperature=0 pour des réponses déterministes
ollama_llm = ChatOllama(
    model="llama3.1",  # Utilise le nom exact retourné par 'ollama list'
    temperature=0
)

# Modèle d'embeddings local
ollama_embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Enveloppement pour Ragas
ragas_llm = LangchainLLMWrapper(ollama_llm)
ragas_embeddings = LangchainEmbeddingsWrapper(ollama_embeddings)

print("LLM RAGAS      : Ollama (llama3.1:8b)")
print("Embeddings     : Ollama (nomic-embed-text)")


# ============================================================================
# 3. DATASET DE TEST
# ============================================================================

TEST_DATASET = [
    {
        "id": "TC1",
        "category": "Simple",
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
        "id": "TC2",
        "category": "Complexe",
        "question": (
            "Compare l'efficacité défensive de l'équipe "
            "à domicile et à l'extérieur."
        ),
        "ground_truth": (
            "L'équipe concède 102 points à domicile "
            "contre 114 points à l'extérieur."
        ),
        "response": (
            "L'équipe concède 102 points à domicile "
            "contre 114 points à l'extérieur."
        ),
        "context": (
            "L'équipe concède en moyenne 102 points lorsqu'elle "
            "joue à domicile et 114 points lorsqu'elle joue "
            "à l'extérieur."
        ),
    },
    {
        "id": "TC3",
        "category": "Bruité",
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
# 4. CONSTRUCTION DU DATASET RAGAS
# ============================================================================

dataset_dict = {
    "user_input": [item["question"] for item in TEST_DATASET],
    "reference": [item["ground_truth"] for item in TEST_DATASET],
    "response": [item["response"] for item in TEST_DATASET],
    "retrieved_contexts": [[item["context"]] for item in TEST_DATASET],
}

eval_dataset = Dataset.from_dict(dataset_dict)

print("\n=== DATASET ===")
print(f"Nombre de cas de test : {len(eval_dataset)}")


# ============================================================================
# 5. INITIALISATION DES METRIQUES (100% OLLAMA)
# ============================================================================

print("\n=== INITIALISATION DES METRIQUES ===")

metrics = [
    ContextPrecision(llm=ragas_llm),
    ContextRecall(llm=ragas_llm),
    Faithfulness(llm=ragas_llm),
    ResponseRelevancy(llm=ragas_llm, embeddings=ragas_embeddings),
    _AnswerSimilarity(embeddings=ragas_embeddings),
]

print("Métriques configurées avec Ollama :")
print("- Context Precision")
print("- Context Recall")
print("- Faithfulness")
print("- Response Relevancy")
print("- Answer Similarity")


# ============================================================================
# 6. EVALUATION RAGAS
# ============================================================================

print("\n=== DEBUT DE L'EVALUATION RAGAS (LOCAL OLLAMA) ===")

try:
    score = evaluate(
        dataset=eval_dataset,
        metrics=metrics,
    )

    print("\nÉvaluation RAGAS terminée avec succès.")

except Exception as error:
    print("\nERREUR PENDANT L'EVALUATION RAGAS")
    print("----------------------------------")
    print(f"Type d'erreur : {type(error).__name__}")
    print(f"Détail        : {error}")
    raise


# ============================================================================
# 7. EXPORT & RESULTATS
# ============================================================================

df = score.to_pandas()

print("\n" + "=" * 100)
print("RESULTATS DES METRIQUES RAGAS")
print("=" * 100)

result_columns = [
    "user_input",
    "context_precision",
    "context_recall",
    "faithfulness",
    "answer_relevance",
    "answer_similarity",
]

available_columns = [col for col in result_columns if col in df.columns]
print(df[available_columns].to_string(index=False))

output_file = "ragas_results.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"\nRésultats sauvegardés dans : {output_file}")