from __future__ import annotations

from courseground.chunking import chunk_document
from courseground.models import Document


def test_chunking_retains_metadata_and_overlap() -> None:
    text = " ".join(f"sentence {number}." for number in range(80))
    document = Document(text, {"course": "BIO305", "file_name": "notes.txt", "section": 4})

    chunks = chunk_document(document, size=140, overlap=30)

    assert len(chunks) > 2
    assert all(chunk.metadata["course"] == "BIO305" for chunk in chunks)
    assert all(chunk.metadata["section"] == 4 for chunk in chunks)
    assert len({chunk.id for chunk in chunks}) == len(chunks)
    assert any(token in chunks[1].text for token in chunks[0].text.split()[-6:])
