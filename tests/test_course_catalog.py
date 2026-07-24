from __future__ import annotations

import pytest

import courseground.config as config


def test_create_course_persists_catalog_and_directories(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(config, "COURSE_CATALOG_PATH", tmp_path / "course_catalog.json")
    monkeypatch.setattr(config, "MATERIALS_DIR", tmp_path / "materials")
    monkeypatch.setattr(config, "UPLOADS_DIR", tmp_path / "uploads")

    course = config.create_course(
        "CS501",
        "Applied Machine Learning",
        "Production ML systems.",
        "What makes an ML system reliable?",
    )

    courses = config.load_courses()
    assert course == "CS501"
    assert courses[course]["name"] == "Applied Machine Learning"
    assert courses[course]["sample_question"] == "What makes an ML system reliable?"
    assert (config.MATERIALS_DIR / course).is_dir()
    assert (config.UPLOADS_DIR / course).is_dir()


def test_create_course_rejects_unsafe_or_duplicate_codes(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(config, "COURSE_CATALOG_PATH", tmp_path / "course_catalog.json")
    monkeypatch.setattr(config, "MATERIALS_DIR", tmp_path / "materials")
    monkeypatch.setattr(config, "UPLOADS_DIR", tmp_path / "uploads")

    with pytest.raises(ValueError, match="letters, numbers"):
        config.create_course("../unsafe", "Unsafe")
    with pytest.raises(ValueError, match="already exists"):
        config.create_course("CS4780", "Duplicate")
