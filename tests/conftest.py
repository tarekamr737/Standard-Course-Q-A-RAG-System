from __future__ import annotations

from pathlib import Path

import pytest

from courseground.embeddings import HashedEmbeddingClient
from courseground.vector_store import LocalVectorStore


@pytest.fixture
def store(tmp_path: Path) -> LocalVectorStore:
    return LocalVectorStore(tmp_path / "vectors.json")


@pytest.fixture
def embedder() -> HashedEmbeddingClient:
    return HashedEmbeddingClient()
