"""
Pipeline RAG sécurisé avec :

1. Nettoyage des documents
2. Chunking
3. Validation Pydantic des données
4. Génération des embeddings
5. Préparation pour FAISS
6. Validation des entrées/sorties avec Pydantic AI
7. Instrumentation Pydantic Logfire

Objectif :
Sécuriser les flux d'entrée et de sortie du pipeline RAG
et permettre d'observer son fonctionnement étape par étape.
"""

import os
import logging
from typing import List

import logfire

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# 1. CONFIGURATION DU LOGGING CLASSIQUE
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================================
# 2. CONFIGURATION PYDANTIC LOGFIRE
# ============================================================================

"""
Logfire permet de suivre l'exécution du pipeline.

Il permet notamment d'observer :

- les différentes étapes du pipeline ;
- les appels LLM ;
- les erreurs ;
- les temps d'exécution ;
- les données instrumentées ;
- les traces entre les différentes étapes.

Pour utiliser Logfire :

    logfire auth

puis créer/configurer un projet Logfire.

Pour un premier test local, on peut également utiliser :
"""

logfire.configure()

# Instrumentation automatique de Pydantic.
#
# Les validations Pydantic deviennent ainsi observables
# dans Logfire.
logfire.instrument_pydantic()


# ============================================================================
# 3. MODELES PYDANTIC : DOCUMENT
# ============================================================================

class DocumentInput(BaseModel):
    """
    Modèle représentant un document entrant dans le pipeline RAG.

    Pydantic vérifie ici que les données reçues ont le bon format.
    """

    document_id: str = Field(
        min_length=1,
        description="Identifiant unique du document",
    )

    text: str = Field(
        min_length=1,
        description="Texte du document",
    )

    source: str = Field(
        min_length=1,
        description="Source du document",
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        """
        Vérifie que le document contient réellement du texte.
        """

        value = value.strip()

        if not value:
            raise ValueError(
                "Le document ne peut pas être vide."
            )

        return value


# ============================================================================
# 4. MODELE PYDANTIC : CHUNK
# ============================================================================

class DocumentChunk(BaseModel):
    """
    Représente un chunk après découpage du document.

    Chaque chunk est validé avant de poursuivre vers
    l'étape d'embedding.
    """

    chunk_id: str = Field(
        min_length=1
    )

    document_id: str = Field(
        min_length=1
    )

    text: str = Field(
        min_length=1
    )

    source: str = Field(
        min_length=1
    )

    chunk_index: int = Field(
        ge=0
    )

    @field_validator("text")
    @classmethod
    def validate_chunk_text(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Un chunk ne peut pas être vide."
            )

        return value


# ============================================================================
# 5. MODELE PYDANTIC : ENTREE DU RAG
# ============================================================================

class RAGInput(BaseModel):
    """
    Données entrantes de la chaîne RAG.

    Cette validation empêche par exemple :
    - une question vide ;
    - une question trop longue ;
    - un format inattendu.
    """

    question: str = Field(
        min_length=3,
        max_length=2000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "La question ne peut pas être vide."
            )

        return value


# ============================================================================
# 6. MODELE PYDANTIC : SORTIE DU RAG
# ============================================================================

class RAGOutput(BaseModel):
    """
    Format attendu de la réponse finale.

    La réponse générée par le LLM est validée avant
    d'être retournée à l'utilisateur.
    """

    answer: str = Field(
        min_length=1,
        max_length=10000,
    )

    sources: List[str] = Field(
        default_factory=list
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "La réponse du LLM ne peut pas être vide."
            )

        return value


# ============================================================================
# 7. NETTOYAGE DU DOCUMENT
# ============================================================================

def clean_document(document: DocumentInput) -> DocumentInput:
    """
    Nettoyage du texte avant le chunking.

    Cette étape permet notamment de :
    - supprimer les espaces inutiles ;
    - normaliser les retours à la ligne ;
    - éviter d'envoyer du contenu vide au modèle d'embedding.
    """

    with logfire.span(
        "rag.clean_document",
        document_id=document.document_id,
    ):

        cleaned_text = " ".join(
            document.text.split()
        )

        logger.info(
            "Nettoyage du document : %s",
            document.document_id,
        )

        return DocumentInput(
            document_id=document.document_id,
            text=cleaned_text,
            source=document.source,
        )


# ============================================================================
# 8. CHUNKING
# ============================================================================

def create_chunks(
    document: DocumentInput,
    chunk_size: int = 500,
) -> List[DocumentChunk]:
    """
    Découpe le document en chunks.

    Chaque chunk est ensuite validé par Pydantic.
    """

    with logfire.span(
        "rag.chunking",
        document_id=document.document_id,
        chunk_size=chunk_size,
    ):

        words = document.text.split()

        chunks = []

        for index in range(
            0,
            len(words),
            chunk_size,
        ):

            chunk_text = " ".join(
                words[index:index + chunk_size]
            )

            chunk = DocumentChunk(
                chunk_id=(
                    f"{document.document_id}_"
                    f"{index // chunk_size}"
                ),
                document_id=document.document_id,
                text=chunk_text,
                source=document.source,
                chunk_index=index // chunk_size,
            )

            chunks.append(chunk)

        logger.info(
            "Document %s : %d chunks créés",
            document.document_id,
            len(chunks),
        )

        return chunks


# ============================================================================
# 9. PREPARATION POUR EMBEDDING
# ============================================================================

def prepare_embeddings(
    chunks: List[DocumentChunk],
) -> List[str]:
    """
    Prépare les textes qui seront transmis au modèle d'embedding.

    IMPORTANT :
    Les chunks ont déjà été validés par Pydantic.
    """

    with logfire.span(
        "rag.embedding_preparation",
        number_of_chunks=len(chunks),
    ):

        texts = [
            chunk.text
            for chunk in chunks
        ]

        logger.info(
            "%d chunks prêts pour embedding",
            len(texts),
        )

        return texts


# ============================================================================
# 10. VALIDATION DE L'ENTREE RAG
# ============================================================================

def validate_rag_input(
    question: str,
    top_k: int = 5,
) -> RAGInput:
    """
    Validation Pydantic de la requête utilisateur
    avant son entrée dans la chaîne RAG.
    """

    with logfire.span(
        "rag.validate_input"
    ):

        rag_input = RAGInput(
            question=question,
            top_k=top_k,
        )

        logger.info(
            "Entrée RAG validée."
        )

        return rag_input


# ============================================================================
# 11. VALIDATION DE LA SORTIE
# ============================================================================

def validate_rag_output(
    answer: str,
    sources: List[str],
    confidence: float,
) -> RAGOutput:
    """
    Validation de la réponse générée.

    Le résultat ne sort du pipeline que s'il respecte
    le contrat défini par Pydantic.
    """

    with logfire.span(
        "rag.validate_output"
    ):

        result = RAGOutput(
            answer=answer,
            sources=sources,
            confidence=confidence,
        )

        logger.info(
            "Sortie RAG validée."
        )

        return result


# ============================================================================
# 12. PIPELINE PRINCIPAL DE PREPARATION DES DONNEES
# ============================================================================

def prepare_document_for_rag(
    document_id: str,
    text: str,
    source: str,
):
    """
    Pipeline complet :

    Document
       ↓
    Pydantic
       ↓
    Nettoyage
       ↓
    Chunking
       ↓
    Validation Pydantic
       ↓
    Préparation embeddings
    """

    with logfire.span(
        "rag.document_pipeline",
        document_id=document_id,
    ):

        # ------------------------------------------------------------
        # ETAPE 1 : validation du document entrant
        # ------------------------------------------------------------

        document = DocumentInput(
            document_id=document_id,
            text=text,
            source=source,
        )

        # ------------------------------------------------------------
        # ETAPE 2 : nettoyage
        # ------------------------------------------------------------

        cleaned_document = clean_document(
            document
        )

        # ------------------------------------------------------------
        # ETAPE 3 : chunking
        # ------------------------------------------------------------

        chunks = create_chunks(
            cleaned_document
        )

        # ------------------------------------------------------------
        # ETAPE 4 : préparation des embeddings
        # ------------------------------------------------------------

        embedding_texts = prepare_embeddings(
            chunks
        )

        return {
            "document": cleaned_document,
            "chunks": chunks,
            "embedding_texts": embedding_texts,
        }


# ============================================================================
# 13. TEST DU PIPELINE
# ============================================================================

if __name__ == "__main__":

    print(
        "\n=== PIPELINE RAG SECURISE ==="
    )

    example_text = """
    Le système RAG permet de rechercher des informations
    dans une base documentaire avant de transmettre le contexte
    pertinent au modèle de langage.
    """

    result = prepare_document_for_rag(
        document_id="DOC001",
        text=example_text,
        source="document_test.txt",
    )

    print(
        f"\nDocument validé : "
        f"{result['document'].document_id}"
    )

    print(
        f"Nombre de chunks : "
        f"{len(result['chunks'])}"
    )

    print(
        "\nPipeline de préparation terminé."
    )