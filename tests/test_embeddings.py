from __future__ import annotations

from courseground.config import Settings
from courseground.embeddings import OpenRouterEmbeddingClient, openrouter_headers


def test_openrouter_embeddings_request_float_vectors(monkeypatch) -> None:
    settings = Settings("test-key", "https://example.test/v1", "embed-model", "chat-model", 4, 900, 160, 0.18)
    client = OpenRouterEmbeddingClient(settings)
    calls = {}

    class Response:
        data = [type("Embedding", (), {"embedding": [0.25, 0.75]})()]

    def create(**kwargs):
        calls.update(kwargs)
        return Response()

    monkeypatch.setattr(client.client.embeddings, "create", create)

    assert client.embed(["course passage"]) == [[0.25, 0.75]]
    assert calls == {
        "model": "embed-model",
        "input": ["course passage"],
        "encoding_format": "float",
    }


def test_openrouter_embeddings_are_batched(monkeypatch) -> None:
    settings = Settings("test-key", "https://example.test/v1", "embed-model", "chat-model", 4, 900, 160, 0.18)
    client = OpenRouterEmbeddingClient(settings)
    requests = []

    def create(**kwargs):
        requests.append(kwargs)
        data = [type("Embedding", (), {"embedding": [float(index)]})() for index, _ in enumerate(kwargs["input"])]
        return type("Response", (), {"data": data})()

    monkeypatch.setattr(client.client.embeddings, "create", create)

    vectors = client.embed([f"passage {index}" for index in range(33)])

    assert len(vectors) == 33
    assert [len(request["input"]) for request in requests] == [32, 1]
    assert all(request["encoding_format"] == "float" for request in requests)


def test_openrouter_attribution_headers_are_configurable() -> None:
    settings = Settings(
        "test-key", "https://example.test/v1", "embed-model", "chat-model", 4, 900, 160, 0.18,
        openrouter_site_url="https://courseground.example",
        openrouter_app_name="CourseGround QA",
    )

    assert openrouter_headers(settings) == {
        "HTTP-Referer": "https://courseground.example",
        "X-OpenRouter-Title": "CourseGround QA",
    }
