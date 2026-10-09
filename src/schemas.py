# src/sportsee/schemas.py
"""Schémas de données pour l'évaluation RAG."""

from pydantic import BaseModel, Field
from typing import Optional, List


class EvaluationCase(BaseModel):
    """Cas d'évaluation pour tester le RAG."""
    
    question_id: Optional[str] = Field(None, description="Identifiant unique de la question")
    question: str = Field(..., description="La question posée")
    contexts: Optional[List[str]] = Field(None, description="Contextes récupérés")
    ground_truth: Optional[str] = Field(None, description="Réponse de référence (ground truth)")
    category: Optional[str] = Field(None, description="Catégorie de la question")


class RAGResponse(BaseModel):
    """Réponse générée par le système RAG."""
    
    question_id: Optional[str] = Field(None, description="Identifiant unique de la question")
    question: str = Field(..., description="La question posée")
    answer: str = Field(..., description="Réponse générée par le LLM")
    contexts: Optional[List[str]] = Field(None, description="Contextes utilisés pour générer la réponse")
    retrieval_query: Optional[str] = Field(None, description="Requête de retrieval utilisée")


class SourceDocument(BaseModel):
    """Document source pour le RAG."""
      
    document_id: str = Field(..., description="Identifiant unique du document")
    text: Optional[str] = Field(None, description="Contenu du document")
    source: Optional[str] = Field(None, description="Source du document")
    metadata: Optional[dict] = Field(None, description="Métadonnées")

class TextChunk(BaseModel):
    """Chunk de texte pour le RAG."""
    
    chunk_id: str = Field(..., description="Identifiant unique du chunk")
    text: str = Field(..., description="Contenu du chunk")
    document_id: Optional[str] = Field(None, description="ID du document source")
    start: Optional[int] = Field(None, description="Index de début dans le document")
    end: Optional[int] = Field(None, description="Index de fin dans le document")
    metadata: Optional[dict] = Field(None, description="Métadonnées du chunk")