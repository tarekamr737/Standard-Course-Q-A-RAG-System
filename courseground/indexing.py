"""Index orchestration that joins loaders, chunking, embeddings, and storage."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chunking import chunk_documents
from .loaders import discover_course_files, load_file


@dataclass(frozen=True)
class IndexingSummary:
    files: int
    documents: int
    chunks: int
    errors: list[str]


class CourseIndexer:
    def __init__(self, store, embedder, chunk_size: int, chunk_overlap: int) -> None:
        self.store = store
        self.embedder = embedder
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def index_signature(self) -> dict:
        """Describe the retrieval settings that must match a persisted index."""
        return {
            "embedding_client": type(self.embedder).__name__,
            "embedding_model": getattr(self.embedder, "model", "hashed-local-2048"),
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
        }

    def index_course(self, course: str, directories: list[Path]) -> IndexingSummary:
        files = discover_course_files(course, directories)
        documents = []
        errors = []
        for path in files:
            try:
                documents.extend(load_file(path, course))
            except ValueError as error:
                errors.append(str(error))
        chunks = chunk_documents(documents, self.chunk_size, self.chunk_overlap)
        vectors = self.embedder.embed([chunk.text for chunk in chunks]) if chunks else []
        self.store.replace_course(course, chunks, vectors, self.index_signature())
        return IndexingSummary(len(files), len(documents), len(chunks), errors)
