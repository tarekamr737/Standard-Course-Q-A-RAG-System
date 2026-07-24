"""Typed domain objects exchanged between CourseGround modules."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Document:
    text: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float


@dataclass(frozen=True)
class Citation:
    number: int
    file_name: str
    file_type: str
    location: str
    excerpt: str
    score: float


@dataclass(frozen=True)
class Answer:
    text: str
    citations: list[Citation]
    supported: bool
    mode: str

    def to_dict(self) -> dict[str, Any]:
        return {"text": self.text, "citations": [asdict(item) for item in self.citations], "supported": self.supported, "mode": self.mode}
