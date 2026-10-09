import pytest

from sportsee.rag.clean import clean_text, clean_document
from sportsee.rag.chunking import chunk_document
from sportsee.schemas import SourceDocument, TextChunk


# ---------------------------
# Tests pour clean_text
# ---------------------------


def test_clean_text_removes_extra_spaces():
    text = "  Match   de   basket  "
    assert clean_text(text) == "Match de basket"


def test_clean_text_removes_non_breaking_spaces():
    text = "Match\xa0de\xa0basket"
    assert clean_text(text) == "Match de basket"


def test_clean_text_removes_tabs_and_newlines():
    text = "Match\tde\nbasket\r\n"
    assert clean_text(text) == "Match de basket"


def test_clean_text_fixes_space_before_punctuation():
    text = "Match de basket , score : 98 - 95 !"
    assert clean_text(text) == "Match de basket, score : 98 - 95!"


def test_clean_text_strips_result():
    text = "   Match de basket   "
    assert clean_text(text) == "Match de basket"


def test_clean_text_empty_or_whitespace_only_raises():
    # On s’attend à ce que clean_text renvoie "" pour un texte vide,
    # mais que clean_document lève une erreur via Pydantic.
    assert clean_text("") == ""
    assert clean_text("   ") == ""
    assert clean_text("\t\n") == ""


# ---------------------------
# Tests pour clean_document
# ---------------------------


def test_clean_document_normalizes_text():
    doc = SourceDocument(
        document_id="doc-1",
        source="test",
        text="  Match   de   basket  ",
    )
    cleaned = clean_document(doc)
    assert cleaned.text == "Match de basket"
    assert cleaned.document_id == "doc-1"
    assert cleaned.source == "test"


def test_clean_document_preserves_metadata():
    doc = SourceDocument(
        document_id="doc-1",
        source="test",
        text="  Match   de   basket  ",
        metadata={"match_id": 123, "season": "2023-24"},
    )
    cleaned = clean_document(doc)
    assert cleaned.metadata == {"match_id": 123, "season": "2023-24"}


def test_clean_document_empty_text_is_allowed_at_clean_level():
    # clean_text renvoie "" ; c’est au niveau du schéma / pipeline
    # de refuser un document vide si c’est voulu.
    doc = SourceDocument(
        document_id="doc-1",
        source="test",
        text="   ",
    )
    cleaned = clean_document(doc)
    assert cleaned.text == ""


# ---------------------------
# Tests pour chunk_document
# ---------------------------


def test_chunking_creates_overlapping_chunks():
    document = SourceDocument(
        document_id="doc-1",
        source="test",
        text="A" * 2000,
    )

    chunks = chunk_document(document, chunk_size=500, overlap=50)

    assert len(chunks) > 1

    # Vérifier que le recouvrement est bien de 50 caractères
    # chunks[0]: [0, 500)
    # chunks[1]: [450, 950)
    assert chunks[0].metadata["start"] == 0
    assert chunks[0].metadata["end"] == 500
    assert chunks[1].metadata["start"] == 450
    assert chunks[1].metadata["end"] == 950

    # Vérifier la propriété demandée dans l’énoncé
    assert chunks[0].metadata["end"] - chunks[1].metadata["start"] == 50


def test_chunking_rejects_invalid_overlap():
    document = SourceDocument(
        document_id="doc-1",
        source="test",
        text="A" * 100,
    )

    with pytest.raises(ValueError, match="overlap doit être inférieur à chunk_size"):
        chunk_document(document, chunk_size=100, overlap=100)


def test_chunking_handles_short_text_single_chunk():
    document = SourceDocument(
        document_id="doc-1",
        source="test",
        text="Petit texte.",
    )

    chunks = chunk_document(document, chunk_size=500, overlap=50)

    assert len(chunks) == 1
    assert chunks[0].text == "Petit texte."
    assert chunks[0].metadata["start"] == 0
    assert chunks[0].metadata["end"] == len("Petit texte.")


def test_chunking_ids_are_sequential():
    document = SourceDocument(
        document_id="doc-42",
        source="test",
        text="A" * 2000,
    )

    chunks = chunk_document(document, chunk_size=500, overlap=50)

    for i, chunk in enumerate(chunks):
        assert chunk.chunk_id == f"doc-42_{i}"
        assert chunk.document_id == "doc-42"
        assert chunk.metadata["chunk_index"] == i


def test_chunking_text_is_stripped():
    # Le texte est découpé puis strip() appliqué sur chaque chunk
    document = SourceDocument(
        document_id="doc-1",
        source="test",
        text="  " + "A" * 600 + "  ",
    )

    chunks = chunk_document(document, chunk_size=500, overlap=50)

    # Le premier chunk ne doit pas commencer ni finir par des espaces
    assert chunks[0].text == chunks[0].text.strip()


def test_chunking_last_chunk_ends_at_text_length():
    text = "A" * 1237
    document = SourceDocument(
        document_id="doc-1",
        source="test",
        text=text,
    )

    chunks = chunk_document(document, chunk_size=500, overlap=50)

    assert chunks[-1].metadata["end"] == len(text)


# ---------------------------
# Tests d’intégration légère clean + chunk
# ---------------------------


def test_clean_then_chunk_pipeline():
    raw_text = "  Match   de   basket  \t avec   beaucoup   d’espaces  . "
    document = SourceDocument(
        document_id="doc-1",
        source="test",
        text=raw_text,
    )

    cleaned = clean_document(document)
    chunks = chunk_document(cleaned, chunk_size=50, overlap=10)

    assert len(chunks) >= 1
    # Aucun chunk ne doit contenir de doubles espaces
    for chunk in chunks:
        assert "  " not in chunk.text