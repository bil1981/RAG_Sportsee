###Pipeline de Traitement (Chunking + Embedding + Logfire)

import logfire
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from schemas import RawDocument, ProcessedChunk

logfire.configure()

class DataPrepPipeline:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        # Utilisation des embeddings locaux Ollama
        self.embeddings_model = OllamaEmbeddings(
            model="nomic-embed-text"
        )

    @logfire.instrument("Clean Raw Text")
    def clean_text(self, text: str) -> str:
        return " ".join(text.split())

    @logfire.instrument("Process Document to Chunks")
    def process_document(self, raw_doc: RawDocument) -> List[ProcessedChunk]:
        cleaned_content = self.clean_text(raw_doc.content)
        raw_chunks = self.splitter.split_text(cleaned_content)
        
        processed_chunks = []
        for idx, chunk_text in enumerate(raw_chunks):
            chunk = ProcessedChunk(
                chunk_id=f"{raw_doc.doc_id}_chunk_{idx}",
                doc_id=raw_doc.doc_id,
                text=chunk_text,
                chunk_index=idx,
                token_count=len(chunk_text.split())
            )
            processed_chunks.append(chunk)
            
        return processed_chunks

    @logfire.instrument("Generate Ollama Embeddings")
    def generate_embeddings(self, chunks: List[ProcessedChunk]) -> List[ProcessedChunk]:
        texts = [c.text for c in chunks]
        vectors = self.embeddings_model.embed_documents(texts)
        
        for chunk, vector in zip(chunks, vectors):
            chunk.embedding = vector
            
        return chunks