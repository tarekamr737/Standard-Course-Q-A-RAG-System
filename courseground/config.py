"""Configuration and course catalogue for CourseGround."""

from __future__ import annotations

import os
import json
import re
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
MATERIALS_DIR = DATA_DIR / "course_materials"
UPLOADS_DIR = DATA_DIR / "uploads"
INDEX_DIR = DATA_DIR / "index"
COURSE_CATALOG_PATH = DATA_DIR / "course_catalog.json"
COURSE_CODE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9 _-]{0,47}")


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


def _custom_courses() -> dict[str, dict[str, str]]:
    """Read locally created courses without allowing a broken catalog to stop the app."""
    if not COURSE_CATALOG_PATH.exists():
        return {}
    try:
        payload = json.loads(COURSE_CATALOG_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(payload, dict):
        return {}
    courses: dict[str, dict[str, str]] = {}
    for code, details in payload.items():
        if not isinstance(code, str) or not COURSE_CODE_PATTERN.fullmatch(code):
            continue
        if not isinstance(details, dict) or not isinstance(details.get("name"), str):
            continue
        name = details["name"].strip()
        if not name:
            continue
        courses[code] = {
            "name": name,
            "short_name": str(details.get("short_name") or name).strip(),
            "description": str(details.get("description") or "Course materials ready for indexing.").strip(),
            "accent": str(details.get("accent") or "#0043AE"),
            "sample_question": str(details.get("sample_question") or "What are the most important concepts in the indexed material?").strip(),
        }
    return courses


def load_courses() -> dict[str, dict[str, str]]:
    """Return built-in courses plus locally created courses."""
    courses = {code: details.copy() for code, details in COURSES.items()}
    courses.update({code: details for code, details in _custom_courses().items() if code not in courses})
    return courses


def create_course(code: str, name: str, description: str = "", sample_question: str = "") -> str:
    """Persist a user-created course and initialize its D: storage directories."""
    code = code.strip()
    name = name.strip()
    if not COURSE_CODE_PATTERN.fullmatch(code):
        raise ValueError("Course code may use letters, numbers, spaces, hyphens, and underscores only.")
    if not name:
        raise ValueError("Course name is required.")
    if code in load_courses():
        raise ValueError(f"A course with code '{code}' already exists.")

    catalog = _custom_courses()
    catalog[code] = {
        "name": name,
        "short_name": name,
        "description": description.strip() or "Course materials ready for indexing.",
        "accent": "#0043AE",
        "sample_question": sample_question.strip() or "What are the most important concepts in the indexed material?",
    }
    COURSE_CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = COURSE_CATALOG_PATH.with_suffix(".tmp")
    temporary.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(COURSE_CATALOG_PATH)
    for directory in (MATERIALS_DIR / code, UPLOADS_DIR / code):
        directory.mkdir(parents=True, exist_ok=True)
    return code


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
                "OPENROUTER_CHAT_MODEL", "google/gemma-4-26b-a4b-it:free"
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
