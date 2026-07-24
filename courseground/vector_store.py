"""Small persisted vector store with deterministic course-scoped cosine search."""

from __future__ import annotations

import json
import math
from pathlib import Path

from .models import Chunk, SearchResult


class LocalVectorStore:
    def __init__(self, index_path: Path) -> None:
        self.index_path = index_path
        self.metadata_path = index_path.with_name(f"{index_path.stem}-metadata.json")
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self._records = self._load()
        self._index_metadata = self._load_metadata()

    def _load(self) -> list[dict]:
        if not self.index_path.exists():
            return []
        try:
            return json.loads(self.index_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

    def _save(self) -> None:
        temporary = self.index_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(self._records, ensure_ascii=False), encoding="utf-8")
        temporary.replace(self.index_path)

    def _load_metadata(self) -> dict[str, dict]:
        if not self.metadata_path.exists():
            return {}
        try:
            payload = json.loads(self.metadata_path.read_text(encoding="utf-8"))
            return payload if isinstance(payload, dict) else {}
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_metadata(self) -> None:
        temporary = self.metadata_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(self._index_metadata, ensure_ascii=False), encoding="utf-8")
        temporary.replace(self.metadata_path)

    def replace_course(
        self,
        course: str,
        chunks: list[Chunk],
        vectors: list[list[float]],
        index_metadata: dict | None = None,
    ) -> int:
        if len(chunks) != len(vectors):
            raise ValueError("Each chunk must have exactly one embedding.")
        self._records = [record for record in self._records if record["metadata"].get("course") != course]
        self._records.extend(
            {"id": chunk.id, "text": chunk.text, "metadata": chunk.metadata, "vector": vector}
            for chunk, vector in zip(chunks, vectors, strict=True)
        )
        self._save()
        if index_metadata is not None:
            self._index_metadata[course] = index_metadata
            self._save_metadata()
        return len(chunks)

    def course_count(self, course: str) -> int:
        return sum(record["metadata"].get("course") == course for record in self._records)

    def course_index_matches(self, course: str, expected_metadata: dict) -> bool:
        return self.course_count(course) > 0 and self._index_metadata.get(course) == expected_metadata

    def search(self, query_vector: list[float], course: str, top_k: int) -> list[SearchResult]:
        candidates = []
        query_magnitude = math.sqrt(sum(value * value for value in query_vector)) or 1.0
        for record in self._records:
            if record["metadata"].get("course") != course:
                continue
            vector = record["vector"]
            if len(vector) != len(query_vector):
                continue
            magnitude = math.sqrt(sum(value * value for value in vector)) or 1.0
            score = sum(a * b for a, b in zip(query_vector, vector, strict=True)) / (query_magnitude * magnitude)
            candidates.append(
                SearchResult(Chunk(record["id"], record["text"], record["metadata"]), score)
            )
        return sorted(candidates, key=lambda result: result.score, reverse=True)[:top_k]
