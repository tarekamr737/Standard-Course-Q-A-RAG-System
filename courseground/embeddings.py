"""Embedding clients for OpenRouter and an offline deterministic fallback."""

from __future__ import annotations

import hashlib
import math
import re
from collections import Counter

from openai import OpenAI

from .config import Settings


def openrouter_headers(settings: Settings) -> dict[str, str]:
    """Apply OpenRouter's optional application-attribution headers."""
    return {
        "HTTP-Referer": settings.openrouter_site_url,
        "X-OpenRouter-Title": settings.openrouter_app_name,
    }


class HashedEmbeddingClient:
    """Local fallback that keeps the demo usable without an API key."""

    # A wider feature space keeps the offline preview's exact-term matches from
    # being drowned out by hash collisions in small course collections.
    dimension = 2048

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            vector = [0.0] * self.dimension
            for token, count in Counter(re.findall(r"[a-z0-9]+", text.lower())).items():
                index = int(hashlib.sha256(token.encode()).hexdigest(), 16) % self.dimension
                vector[index] += float(count)
            magnitude = math.sqrt(sum(item * item for item in vector)) or 1.0
            embeddings.append([item / magnitude for item in vector])
        return embeddings


class OpenRouterEmbeddingClient:
    batch_size = 32

    def __init__(self, settings: Settings) -> None:
        self.model = settings.embedding_model
        self.client = OpenAI(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key,
            default_headers=openrouter_headers(settings),
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        # The OpenAI SDK may default to base64 output; Nvidia's OpenRouter
        # embedding endpoint accepts float vectors only.
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            response = self.client.embeddings.create(
                model=self.model,
                input=texts[start : start + self.batch_size],
                encoding_format="float",
            )
            vectors.extend(list(item.embedding) for item in response.data)
        if len(vectors) != len(texts):
            raise ValueError("OpenRouter returned an unexpected number of embedding vectors.")
        return vectors


def embedding_client(settings: Settings) -> OpenRouterEmbeddingClient | HashedEmbeddingClient:
    return OpenRouterEmbeddingClient(settings) if settings.openrouter_api_key else HashedEmbeddingClient()
