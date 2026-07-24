from __future__ import annotations

from courseground.indexing import CourseIndexer
from courseground.models import Chunk


def test_index_signature_tracks_embedding_and_chunk_settings(store, embedder) -> None:
    indexer = CourseIndexer(store, embedder, chunk_size=500, chunk_overlap=80)
    chunk = Chunk("cs-1", "Regularization limits complexity.", {"course": "CS4780"})

    store.replace_course("CS4780", [chunk], embedder.embed([chunk.text]), indexer.index_signature())

    assert store.course_index_matches("CS4780", indexer.index_signature())
    assert not store.course_index_matches(
        "CS4780", {**indexer.index_signature(), "chunk_size": 900}
    )
