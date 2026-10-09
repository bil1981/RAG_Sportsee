from sportsee.schemas import SourceDocument, TextChunk


def chunk_document(
    document: SourceDocument,
    chunk_size: int = 800,
    overlap: int = 120,
) -> list[TextChunk]:
    if overlap >= chunk_size:
        raise ValueError("overlap doit être inférieur à chunk_size")

    text = document.text
    chunks = []
    start = 0
    index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        content = text[start:end].strip()

        if content:
            chunks.append(
                TextChunk(
                    chunk_id=f"{document.document_id}_{index}",
                    document_id=document.document_id,
                    text=content,
                    metadata={
                        **document.metadata,
                        "chunk_index": index,
                        "start": start,
                        "end": end,
                    },
                )
            )

        if end == len(text):
            break

        start = end - overlap
        index += 1

    return chunks