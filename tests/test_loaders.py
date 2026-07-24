from __future__ import annotations

import csv
from pathlib import Path

import pytest
from docx import Document as DocxDocument
from reportlab.pdfgen import canvas

from courseground.loaders import MalformedDocumentError, UnsupportedFormatError, load_file


@pytest.mark.parametrize("suffix", [".txt", ".csv", ".docx", ".pdf"])
def test_supported_formats_preserve_core_metadata(tmp_path: Path, suffix: str) -> None:
    path = tmp_path / f"material{suffix}"
    if suffix == ".txt":
        path.write_text("A clear course concept.", encoding="utf-8")
    elif suffix == ".csv":
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["topic", "note"])
            writer.writeheader()
            writer.writerow({"topic": "regularization", "note": "limits complexity"})
    elif suffix == ".docx":
        document = DocxDocument()
        document.add_paragraph("A readable DOCX paragraph.")
        document.save(path)
    else:
        pdf = canvas.Canvas(str(path))
        pdf.drawString(72, 720, "A readable PDF page.")
        pdf.save()

    documents = load_file(path, "CS4780")

    assert documents
    assert documents[0].metadata["course"] == "CS4780"
    assert documents[0].metadata["file_name"] == path.name
    assert documents[0].metadata["file_type"] == suffix[1:].upper()


def test_malformed_pdf_is_reported(tmp_path: Path) -> None:
    path = tmp_path / "broken.pdf"
    path.write_bytes(b"not a pdf")
    with pytest.raises(MalformedDocumentError):
        load_file(path, "CS4780")


def test_unsupported_file_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "notes.xlsx"
    path.write_text("data", encoding="utf-8")
    with pytest.raises(UnsupportedFormatError):
        load_file(path, "CS4780")
