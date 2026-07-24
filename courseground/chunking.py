"""Deterministic, configurable document chunking."""

from __future__ import annotations

import hashlib
import re

from .models import Chunk, Document


def chunk_document(document: Document, size: int, overlap: int) -> list[Chunk]:
    if size < 100:
        raise ValueError("Chunk size must be at least 100 characters.")
    if not 0 <= overlap < size:
        raise ValueError("Chunk overlap must be non-negative and smaller than chunk size.")

    text = document.text
    chunks: list[Chunk] = []
    start = 0
    chunk_number = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            sentence_break = max(text.rfind(". ", start, end), text.rfind("\n", start, end))
            if sentence_break > start + size // 2:
                end = sentence_break + 1
        part = text[start:end].strip()
        if part:
            fingerprint = f"{document.metadata.get('course')}|{document.metadata.get('file_name')}|{document.metadata.get('page', document.metadata.get('section', document.metadata.get('row', '')))}|{chunk_number}|{part}"
            chunk_id = hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[:20]
            metadata = {**document.metadata, "chunk_id": chunk_id, "chunk_number": chunk_number}
            chunks.append(Chunk(id=chunk_id, text=part, metadata=metadata))
            chunk_number += 1
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def chunk_documents(documents: list[Document], size: int, overlap: int) -> list[Chunk]:
    return [chunk for document in documents for chunk in chunk_document(document, size, overlap)]
