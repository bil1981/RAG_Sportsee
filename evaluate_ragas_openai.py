import os
import logging

import pandas as pd
from datasets import Dataset
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI

from ragas import evaluate
from ragas.embeddings import OpenAIEmbeddings
from ragas.llms import llm_factory

from ragas.metrics._context_precision import ContextPrecision
from ragas.metrics._context_recall import ContextRecall
from ragas.metrics._faithfulness import Faithfulness
from ragas.metrics._answer_relevance import ResponseRelevancy
from ragas.metrics import _AnswerSimilarity

# Importe Logfire.
# Logfire permet d'observer et d'enregistrer l'exécution du programme.
import logfire

# Configure Logfire.
# send_to_logfire=False signifie que les traces ne sont pas envoyées
# au service distant Logfire.
# Elles peuvent toutefois rester disponibles localement selon la configuration.
logfire.configure(send_to_logfire=False)


# ============================================================================
# 1. CONFIGURATION
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY est introuvable dans votre fichier .env"
    )


print("\n=== INITIALISATION RAGAS ===")

openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)

async_openai_client = AsyncOpenAI(
    api_key=OPENAI_API_KEY
)

ragas_llm = llm_factory(
    model="gpt-4o-mini",
    client=openai_client,
)

ragas_embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    client=async_openai_client,
)

print("Client OpenAI : OK")
print("Client AsyncOpenAI : OK")
print("LLM RAGAS      : gpt-4o-mini")
print("Embeddings     : text-embedding-3-small")


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
    "user_input": [
        item["question"]
        for item in TEST_DATASET
    ],
    "reference": [
        item["ground_truth"]
        for item in TEST_DATASET
    ],
    "response": [
        item["response"]
        for item in TEST_DATASET
    ],
    "retrieved_contexts": [
        [item["context"]]
        for item in TEST_DATASET
    ],
}

eval_dataset = Dataset.from_dict(dataset_dict)


print("\n=== DATASET ===")
print(f"Nombre de cas de test : {len(eval_dataset)}")

for i, item in enumerate(TEST_DATASET, start=1):
    print(
        f"TC{i} - {item['category']} : "
        f"{item['question']}"
    )


# ============================================================================
# 5. INITIALISATION DES METRIQUES
# ============================================================================

print("\n=== INITIALISATION DES METRIQUES ===")

metrics = [
    ContextPrecision(llm=ragas_llm),
    ContextRecall(llm=ragas_llm),
    Faithfulness(llm=ragas_llm),
# Si vous souhaitez réactiver les autres métriques :
    # ResponseRelevancy(
    #     llm=ragas_llm,
    #     embeddings=ragas_embeddings,
    # ),
    # _AnswerSimilarity(
    #     embeddings=ragas_embeddings
    # ),
]

print("Metriques configurees :")
print("- Context Precision")
print("- Context Recall")
print("- Faithfulness")
# print("- Response Relevancy")
# print("- Answer Similarity")


# ============================================================================
# 6. EVALUATION RAGAS
# ============================================================================

print("\n=== DEBUT DE L'EVALUATION RAGAS ===")

try:

    score = evaluate(
        dataset=eval_dataset,
        metrics=metrics,
    )

    print("\nEvaluation RAGAS terminee.")

except Exception as error:

    print("\nERREUR PENDANT L'EVALUATION RAGAS")
    print("----------------------------------")
    print(f"Type d'erreur : {type(error).__name__}")
    print(f"Detail        : {error}")

    print("\nVerifiez notamment :")
    print("1. La validite de OPENAI_API_KEY")
    print("2. Les credits/quota disponibles sur OpenAI")
    print("3. La configuration des embeddings")
    print("4. La connexion Internet")

    raise


# ============================================================================
# 7. CONVERSION DES RESULTATS
# ============================================================================

df = score.to_pandas()


# ============================================================================
# 8. AFFICHAGE DES RESULTATS
# ============================================================================

print("\n")
print("=" * 100)
print("RESULTATS DES METRIQUES RAGAS")
print("=" * 100)

result_columns = [
    "user_input",
    "context_precision",
    "context_recall",
    "faithfulness",
    "answer_relevancy",
    "answer_similarity",
]

available_columns = [
    column
    for column in result_columns
    if column in df.columns
]

print(
    df[available_columns].to_string(index=False)
)


# ============================================================================
# 9. STATISTIQUES MOYENNES
# ============================================================================

metric_columns = [
    "context_precision",
    "context_recall",
    "faithfulness",
    "answer_relevancy",
    "answer_similarity",
]

print("\n")
print("=" * 100)
print("MOYENNES DES METRIQUES")
print("=" * 100)

for metric in metric_columns:

    if metric not in df.columns:
        print(f"{metric:25s}: COLONNE ABSENTE")
        continue

    values = pd.to_numeric(
        df[metric],
        errors="coerce"
    )

    mean_value = values.mean()

    if pd.isna(mean_value):
        print(f"{metric:25s}: NON DISPONIBLE")
    else:
        print(
            f"{metric:25s}: "
            f"{mean_value:.4f}"
        )


# ============================================================================
# 10. SAUVEGARDE CSV
# ============================================================================

output_file = "ragas_results.csv"

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig",
)

# Le décorateur @logfire.instrument demande à Logfire
# d'observer l'exécution de cette fonction.
# Le nom "Run RAG Pipeline" sera utilisé pour identifier cette trace.
@logfire.instrument("Run RAG Pipeline")
def query_rag_prototype(
    vector_store: VectorStoreManager,
    question: str,
):
    """
    Exécute une question dans le système RAG.

    Paramètres :
    - vector_store : objet qui permet de rechercher des documents ;
    - question : question posée au système RAG.
    """

print("\n")
print("=" * 100)
print("SAUVEGARDE")
print("=" * 100)

print(
    f"Resultats sauvegardes dans : {output_file}"
)

print("\nEvaluation RAGAS terminee.")
