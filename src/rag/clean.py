import re

from sportsee.schemas import SourceDocument


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[ \t]+([,.;:!?])", r"\1", text)
    return text.strip()


def clean_document(document: SourceDocument) -> SourceDocument:
    return document.model_copy(update={"text": clean_text(document.text)})