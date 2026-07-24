from __future__ import annotations

from courseground.models import Chunk


def test_retrieval_never_crosses_course_boundary(store, embedder) -> None:
    cs_chunk = Chunk("cs-1", "Regularization limits model complexity.", {"course": "CS4780", "file_name": "cs.txt", "file_type": "TXT"})
    history_chunk = Chunk("hist-1", "Coal powered British industrialization.", {"course": "HIST202", "file_name": "history.txt", "file_type": "TXT"})
    store.replace_course("CS4780", [cs_chunk], embedder.embed([cs_chunk.text]))
    store.replace_course("HIST202", [history_chunk], embedder.embed([history_chunk.text]))

    results = store.search(embedder.embed(["coal industrialization"])[0], "CS4780", top_k=4)

    assert results
    assert all(result.chunk.metadata["course"] == "CS4780" for result in results)
    assert results[0].chunk.id == "cs-1"
