# CourseGround

CourseGround is an evidence-first Streamlit application for asking grounded questions about course materials. It indexes PDF, CSV, DOCX, and TXT files, keeps retrieval scoped to one course at a time, and shows the retrieved source evidence beside every supported answer.

## What is included

- Four included courses: CS 4780 Machine Learning, HIST 202 Modern History, BIO 305 Molecular Biology, and AI-Based Programming (the primary real-material testing course).
- Loaders that preserve course, file name, format, page, section, row, and chunk ID metadata.
- Configurable text chunking, local persistent vector search, and strict course-level filtering.
- OpenRouter integrations for `nvidia/nemotron-3-embed-1b:free` embeddings and `google/gemma-4-31b-it:free` generation.
- A deterministic local embedding and answer preview mode when no API key is configured.
- Tests for supported/malformed files, chunking, source isolation, citations, fallbacks, and retrieved prompt injection.

## Setup on `D:`

The project is designed to keep its virtual environment, data, caches, uploads, and vector index on the project drive. From PowerShell:

```powershell
cd 'D:\INSTANT TRAINING\4th Sprint\2nd project'
$env:PIP_CACHE_DIR = "$PWD\.cache\pip"
$env:TEMP = "$PWD\.cache\tmp"
$env:TMP = $env:TEMP
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your `OPENROUTER_API_KEY` to `.env`. Do not place keys in Streamlit widgets or source code.

Generate the included binary sample materials, then start the application:

```powershell
.\.venv\Scripts\python.exe scripts\generate_sample_assets.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the app, select a course, and choose **Index course materials** from the sidebar. The local preview mode works without a key, but an OpenRouter key enables the configured embedding and generation models.

If you add or change the API key, embedding model, chunk size, or overlap after indexing, CourseGround will show **Re-index needed**. Rebuild that course before asking questions so retrieval and stored vectors use the same settings.

## Architecture

```text
Streamlit UI
  ├─ uploader + course selector
  ├─ CourseIndexer
  │   ├─ PDF / CSV / DOCX / TXT loaders
  │   ├─ normalizer + configurable chunker
  │   ├─ OpenRouter embedding client (or local fallback)
  │   └─ JSON-backed local vector store
  └─ GroundedAnswerer
      ├─ selected-course similarity search
      ├─ grounded OpenRouter prompt
      └─ answer + source citations / safe fallback
```

The index is saved at `data/index/courseground-vectors.json`; uploaded files are saved under `data/uploads/<course>/`. Both are local, ignored by Git, and stay on `D:`.

## Environment variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `OPENROUTER_API_KEY` | Enables OpenRouter requests | unset, local preview mode |
| `OPENROUTER_EMBEDDING_MODEL` | OpenRouter embedding model | `nvidia/nemotron-3-embed-1b:free` |
| `OPENROUTER_CHAT_MODEL` | OpenRouter chat model | `google/gemma-4-31b-it:free` |
| `OPENROUTER_FALLBACK_MODELS` | Comma-separated backup model IDs used by OpenRouter after a primary-model error | unset |
| `OPENROUTER_SITE_URL` | Optional OpenRouter application URL attribution | `http://localhost:8501` |
| `OPENROUTER_APP_NAME` | Optional OpenRouter application title attribution | `CourseGround` |
| `COURSEGROUND_TOP_K` | Retrieved passages | `4` |
| `COURSEGROUND_CHUNK_SIZE` | Character chunk size | `900` |
| `COURSEGROUND_CHUNK_OVERLAP` | Overlapping characters | `160` |
| `COURSEGROUND_MIN_RELEVANCE` | Minimum cosine score for an answer | `0.18` |

## Test and evaluation

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Evaluation prompts and expected answer terms are in `data/evaluation/questions.json`. Before a deployment, re-run the evaluation after changing chunk parameters, embedding models, or materials and manually inspect: retrieval relevance, groundedness, citation accuracy, no-answer behavior, and cross-course isolation.

CourseGround uses OpenRouter's documented OpenAI-compatible client, float-format embeddings, application attribution headers, and optional `models` fallback routing. Add one or more suitable backup model IDs to `OPENROUTER_FALLBACK_MODELS` if the primary provider is frequently rate-limited.

## Deployment

Use the included `.streamlit/config.toml` and deploy with `app.py` as the entry point. Set the environment variables through the host’s secret manager, not a committed `.env` file. Persistent indexing requires a deployment volume; otherwise rebuild the index after each ephemeral restart.
