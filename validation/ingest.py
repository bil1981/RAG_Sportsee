## Exécution et Ingestion avec Validation Intégrée

from schemas import RawDocument, QueryInput
from data_pipeline import DataPrepPipeline

def run_pipeline():
    pipeline = DataPrepPipeline()
    
    # 1. Validation de l'entrée brute
    doc_data = {
        "doc_id": "match_01_report",
        "content": "Rapport du Match 1 : Excellente défense au 3ème quart-temps...",
        "source": "Commentaires des matchs 1.txt"
    }
    raw_doc = RawDocument(**doc_data) # Lève une ValidationError si les types/champs manquent

    # 2. Chunking & Nettoyage
    chunks = pipeline.process_document(raw_doc)

    # 3. Embedding
    embedded_chunks = pipeline.generate_embeddings(chunks)

    # 4. Insertion dans la base vectorielle (Chroma, FAISS, Qdrant, etc.)
    # Ex: vector_store.add_texts(texts=[c.text for c in embedded_chunks], metadatas=[c.dict() ...])
    print(f"✅ {len(embedded_chunks)} chunks validés et vectorisés avec succès.")

if __name__ == "__main__":
    run_pipeline()