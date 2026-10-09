# Importe le module os.
# Il permet de manipuler des variables d'environnement,
# des fichiers et des chemins de dossiers.
# Dans ce script précis, os n'est pas utilisé directement.
import os


# Importe la bibliothèque pandas sous le nom court pd.
# pandas sert à manipuler des tableaux de données,
# notamment des tableaux semblables à des feuilles Excel.
import pandas as pd


# Importe List depuis le module typing.
# List permet d'indiquer qu'une variable doit contenir une liste.
# Dans ce script précis, List n'est pas utilisé directement.
from typing import List


# Importe BaseModel depuis Pydantic.
# BaseModel permet de créer des objets avec des champs obligatoires
# et une validation automatique de leurs types.
from pydantic import BaseModel


# Importe Dataset depuis la bibliothèque Hugging Face datasets.
# Dataset sert à stocker les données sous une forme adaptée
# à l'évaluation par RAGAS.
from datasets import Dataset


# Importe la fonction evaluate de RAGAS.
# Cette fonction lancera l'évaluation de votre système RAG.
from ragas import evaluate

import json     # Importe le module json.

# Importe plusieurs métriques d'évaluation fournies par RAGAS.
from ragas.metrics.collections import (
    answer_relevancy,   # Mesure si la réponse est pertinente par rapport à la question.
    # Mesure si les contextes pertinents apparaissent
    # suffisamment tôt dans les résultats récupérés.
    context_precision,
    # Mesure si les contextes récupérés contiennent
    # les informations nécessaires pour répondre.
    context_recall,
    # Mesure si la réponse est correctement justifiée
    # par les contextes récupérés.
    faithfulness,
    # Mesure si la réponse correspond correctement
    # à la réponse de référence.
    answer_correctness,
)


# Importe RunConfig.
# Cette classe permet de configurer les tentatives,
# le nombre de travailleurs et le temps d'attente de RAGAS.
from ragas.run_config import RunConfig


# Importe Logfire.
# Logfire permet d'observer et d'enregistrer l'exécution du programme.
import logfire


# Importe le modèle de conversation Mistral compatible avec LangChain.
# Il sera utilisé par RAGAS comme évaluateur automatique.
from langchain_mistralai import ChatMistralAI


# Importe le modèle d'embeddings Mistral.
# Les embeddings transforment des textes en vecteurs numériques
# afin de comparer leur sens.
from langchain_mistralai import MistralAIEmbeddings


# Importe votre classe personnalisée qui gère le vector store.
# Cette classe est probablement responsable de rechercher
# les documents pertinents pour une question.
from utils.vector_store import VectorStoreManager


# Importe deux paramètres depuis votre fichier de configuration :
# - MISTRAL_API_KEY : la clé secrète pour appeler Mistral ;
# - MODEL_NAME : le nom du modèle Mistral utilisé pour répondre.
from utils.config import MISTRAL_API_KEY, MODEL_NAME


# Importe l'ancien client Python de Mistral.
# Attention : selon la version installée du SDK Mistral,
# cette importation peut être obsolète.
from mistralai.client import MistralClient


# Importe l'exception levée lorsqu'un appel Mistral échoue.
# Le chemin d'importation peut également dépendre de la version
# du SDK Mistral installée.
from mistralai.exceptions import MistralAPIException


# Configure Logfire.
# send_to_logfire=False signifie que les traces ne sont pas envoyées
# au service distant Logfire.
# Elles peuvent toutefois rester disponibles localement selon la configuration.
logfire.configure(send_to_logfire=False)


# Crée un client Mistral.
# MISTRAL_API_KEY sert à authentifier les appels API.
# max_retries=3 signifie que le client peut réessayer
# jusqu'à trois fois en cas d'échec temporaire.
client = MistralClient(
    api_key=MISTRAL_API_KEY,
    max_retries=3,
)


# Définit le prompt principal envoyé au modèle de langage.
# Les triples guillemets permettent d'écrire une chaîne sur plusieurs lignes.
SYSTEM_PROMPT = """Tu es 'NBA Analyst AI', un assistant expert sur la ligue de basketball NBA.
Ta mission est de répondre aux questions des fans en animant le débat.


---
{context_str}
---


QUESTION DU FAN:
{question}


RÉPONSE DE L'ANALYSTE NBA:"""


# Définit une classe représentant un cas de test.
# Elle hérite de BaseModel, ce qui permet à Pydantic
# de vérifier automatiquement les types des champs.
class TestCase(BaseModel):

    # Identifiant unique du test, par exemple "TC1".
    id: str

    # Catégorie du test, par exemple "Simple", "Complexe" ou "Bruité".
    category: str

    # Question envoyée au système RAG.
    question: str

    # Réponse attendue ou réponse de référence.
    ground_truth: str


# Crée une liste de cas de test.
# Chaque élément de la liste est un objet TestCase.
TEST_DATASET = [

    # Premier cas de test.
    TestCase(
        # Identifiant du premier test.
        id="TC1",

        # Ce test correspond à une question simple.
        category="Simple",

        # Question posée au système.
        question=(
            "Quel joueur a le meilleur pourcentage à 3 points "
            "sur les 5 derniers matchs ?"
        ),

        # Réponse idéale attendue.
        ground_truth=(
            "Paul George possède le meilleur pourcentage "
            "avec 45% à 3 points."
        ),
    ),

    # Deuxième cas de test.
    TestCase(
        # Identifiant du deuxième test.
        id="TC2",

        # Ce test est considéré comme complexe.
        category="Complexe",

        # Question nécessitant une comparaison.
        question=(
            "Compare l'efficacité défensive de l'équipe "
            "à domicile et à l'extérieur."
        ),

        # Réponse idéale attendue.
        ground_truth=(
            "L'équipe concède 102 points à domicile "
            "contre 114 points à l'extérieur."
        ),
    ),

    # Troisième cas de test.
    TestCase(
        # Identifiant du troisième test.
        id="TC3",

        # Ce test contient une question probablement impossible à répondre.
        category="Bruité",

        # Question envoyée au système.
        question=(
            "Combien de paniers le coach a-t-il marqués "
            "pendant le debrief du 12 mars ?"
        ),

        # Réponse attendue si l'information n'existe pas.
        ground_truth=(
            "L'information n'est pas disponible dans les rapports."
        ),
    ),
]


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
score = evaluate(TEST_DATASET, metrics=[context_precision, context_recall, answer_relevancy, faithfulness, answer_correctness])
df=score.to_pandas()
df.to_csv("ragas_results.csv", index=False)