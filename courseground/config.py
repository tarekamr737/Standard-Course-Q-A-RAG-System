"""Configuration and course catalogue for CourseGround."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
MATERIALS_DIR = DATA_DIR / "course_materials"
UPLOADS_DIR = DATA_DIR / "uploads"
INDEX_DIR = DATA_DIR / "index"


COURSES: dict[str, dict[str, str]] = {
    "CS4780": {
        "name": "CS 4780: Machine Learning",
        "short_name": "Machine Learning",
        "description": "Model behavior, optimization, and reliable evaluation.",
        "accent": "#0043AE",
        "sample_question": "How does regularization prevent overfitting?",
    },
    "HIST202": {
        "name": "HIST 202: Modern History",
        "short_name": "Modern History",
        "description": "Industrial change, political movements, and primary sources.",
        "accent": "#7A4B12",
        "sample_question": "What conditions helped industrialization begin in Britain?",
    },
    "BIO305": {
        "name": "BIO 305: Molecular Biology",
        "short_name": "Molecular Biology",
        "description": "Gene expression, cellular information, and experimental methods.",
        "accent": "#08745C",
        "sample_question": "How does transcription differ from translation?",
    },
    "AI based": {
        "name": "AI-Based Programming",
        "short_name": "AI-Based Programming",
        "description": "Reliable AI systems, data engineering, evaluation, and modern sequence models.",
        "accent": "#6D28D9",
        "sample_question": "Why is data engineering important for reliable AI systems?",
    },
}


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables, never from the UI."""

    openrouter_api_key: str | None
    openrouter_base_url: str
    embedding_model: str
    chat_model: str
    top_k: int
    chunk_size: int
    chunk_overlap: int
    min_relevance: float
    openrouter_site_url: str = "http://localhost:8501"
    openrouter_app_name: str = "CourseGround"
    fallback_models: tuple[str, ...] = ()

    @classmethod
    def load(cls) -> "Settings":
        load_dotenv(ROOT_DIR / ".env")
        return cls(
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY") or None,
            openrouter_base_url=os.getenv(
                "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
            ),
            embedding_model=os.getenv(
                "OPENROUTER_EMBEDDING_MODEL", "nvidia/nemotron-3-embed-1b:free"
            ),
            chat_model=os.getenv(
                "OPENROUTER_CHAT_MODEL", "google/gemma-4-31b-it:free"
            ),
            top_k=int(os.getenv("COURSEGROUND_TOP_K", "4")),
            chunk_size=int(os.getenv("COURSEGROUND_CHUNK_SIZE", "900")),
            chunk_overlap=int(os.getenv("COURSEGROUND_CHUNK_OVERLAP", "160")),
            min_relevance=float(os.getenv("COURSEGROUND_MIN_RELEVANCE", "0.18")),
            openrouter_site_url=os.getenv("OPENROUTER_SITE_URL", "http://localhost:8501"),
            openrouter_app_name=os.getenv("OPENROUTER_APP_NAME", "CourseGround"),
            fallback_models=tuple(
                model.strip()
                for model in os.getenv("OPENROUTER_FALLBACK_MODELS", "").split(",")
                if model.strip()
            ),
        )


def ensure_data_directories() -> None:
    """Create mutable application data on the project drive."""
    for directory in (MATERIALS_DIR, UPLOADS_DIR, INDEX_DIR):
        directory.mkdir(parents=True, exist_ok=True)
