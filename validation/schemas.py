#### Définition des Schémas de Données avec Pydantic

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

# Schema pour un document brut avant traitement
class RawDocument(BaseModel):
    doc_id: str = Field(..., description="Identifiant unique du document")
    content: str = Field(..., min_length=10, description="Contenu brut du rapport ou commentaire")
    source: str = Field(..., description="Origine du fichier (ex: match_1_commentaires.txt)")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Schema pour un Chunk validé
class ProcessedChunk(BaseModel):
    chunk_id: str = Field(..., description="ID unique du chunk (ex: doc_id_chunk_0)")
    doc_id: str
    text: str = Field(..., min_length=5, description="Texte nettoyé et chunké")
    chunk_index: int = Field(ge=0)
    token_count: int = Field(gt=0, description="Nombre de tokens dans le chunk")
    embedding: Optional[List[float]] = Field(default=None, description="Vecteur d'embedding")

# Schema pour le contrôle d'entrée de l'agent RAGAS / Pydantic AI
class QueryInput(BaseModel):
    question: str = Field(..., min_length=3, description="Question posée par le coach")
    user_role: str = Field(default="coach", description="Rôle utilisateur pour contrôle d'accès")

# Schema pour la réponse structurée RAG / Pydantic AI
class RAGOutput(BaseModel):
    answer: str = Field(..., description="Réponse synthétisée générée par le modèle")
    source_chunks: List[str] = Field(default_factory=list, description="IDs des chunks utilisés")
    confidence_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)