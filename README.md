# CourseGround

CourseGround is an evidence-first Streamlit application for asking grounded questions about course materials. It ingests PDF, CSV, DOCX, and TXT files, retrieves only from the selected course, and presents the supporting evidence beside every answer.

## Highlights

- Course-scoped retrieval with citations, excerpts, and source locations.
- Create courses, upload materials, and build indexes directly from the sidebar.
- OpenRouter embeddings via `nvidia/nemotron-3-embed-1b:free` and grounded generation via `google/gemma-4-26b-a4b-it:free`.
- Safe fallbacks for insufficient evidence and temporary provider availability issues.
- Support for PDF, CSV, DOCX, and TXT with page, section, row, file, course, and chunk metadata.
- A local vector store and deterministic preview mode for development without an API key.

## Public sample data and privacy

The repository includes three public sample courses:

- CS 4780: Machine Learning
- HIST 202: Modern History
- BIO 305: Molecular Biology

The real AI-Based Programming PDFs remain local on `D:` and are excluded from Git. Upload private or licensed materials only when you are authorized to process them with your selected AI provider.

## Architecture

```text
Streamlit UI
  ├── Course management and file upload
  ├── CourseIndexer
  │   ├── PDF, CSV, DOCX, and TXT loaders
  │   ├── Text cleaning and configurable chunking
  │   ├── OpenRouter embeddings or local fallback embeddings
  │   └── JSON-backed vector store
  └── GroundedAnswerer
      ├── Course-filtered similarity search
      ├── Source-only prompt construction
      └── Answer, citations, evidence preview, or safe fallback
```

## Local setup

Developed and tested with Python 3.11 on Windows. All local runtime data stays on `D:`.

```powershell
cd 'D:\INSTANT TRAINING\4th Sprint\2nd project'
$env:PIP_CACHE_DIR = "$PWD\.cache\pip"
$env:TEMP = "$PWD\.cache\tmp"
$env:TMP = $env:TEMP
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `OPENROUTER_API_KEY` in `.env`. Never commit this file.

Generate the binary sample documents and launch the application:

```powershell
.\.venv\Scripts\python.exe scripts\generate_sample_assets.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open http://127.0.0.1:8501.

## Using the application

### Add or update a course

1. Open **Create course** in the sidebar.
2. Enter a course code and name. The new course is selected automatically.
3. Open **Upload materials** and save PDF, CSV, DOCX, or TXT files.
4. Select **Index course materials** or **Rebuild course index**.
5. Ask questions from the persistent composer at the bottom of the page.

Custom courses, uploads, and indexes are local runtime data. They are stored under `data/` and excluded from Git.

### Re-indexing rules

Rebuild a course index after changing any of the following:

- `OPENROUTER_EMBEDDING_MODEL`
- `COURSEGROUND_CHUNK_SIZE`
- `COURSEGROUND_CHUNK_OVERLAP`

Changing the chat model or fallback models requires an app restart, but not a new embedding index.

## Configuration

Copy `.env.example` to `.env` for local development. The most relevant variables are:

| Variable | Purpose | Default |
| --- | --- | --- |
| `OPENROUTER_API_KEY` | Enables OpenRouter requests | Unset, local preview mode |
| `OPENROUTER_EMBEDDING_MODEL` | Embedding model | `nvidia/nemotron-3-embed-1b:free` |
| `OPENROUTER_CHAT_MODEL` | Primary answer model | `google/gemma-4-26b-a4b-it:free` |
| `OPENROUTER_FALLBACK_MODELS` | Comma-separated failover models | Unset |
| `COURSEGROUND_TOP_K` | Retrieved passages | `4` |
| `COURSEGROUND_CHUNK_SIZE` | Chunk size in characters | `900` |
| `COURSEGROUND_CHUNK_OVERLAP` | Chunk overlap in characters | `160` |
| `COURSEGROUND_MIN_RELEVANCE` | Minimum similarity threshold | `0.18` |

OpenRouter rate limits can affect free models. Configure compatible fallback models to enable documented OpenRouter failover.

## Testing

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The suite covers supported and malformed files, chunking, embedding requests, catalog creation, course isolation, prompt-injection resistance, citations, relevance fallbacks, and model-failure evidence previews.

Evaluation prompts live in `data/evaluation/questions.json`.

## Publish to GitHub

Before publishing, review the staged files carefully. `.env`, Streamlit secrets, generated indexes, uploads, custom-course data, and the real AI-Based Programming PDFs are ignored.

```powershell
git status
git add .
git diff --cached
git commit -m "Prepare CourseGround for deployment"
git remote add origin https://github.com/YOUR-ACCOUNT/YOUR-REPOSITORY.git
git push -u origin main
```

## Deploy on Streamlit Community Cloud

1. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) and connect the GitHub account that owns the repository.
2. Select **Create app**, choose the repository and `main` branch, then set `app.py` as the entrypoint.
3. In **Advanced settings**, select Python 3.11 to match the tested environment.
4. Paste a completed version of `.streamlit/secrets.toml.example` into the **Secrets** field. Replace the placeholder API key with your real key.
5. Deploy, then upload any non-public course materials in the app and build their indexes.

Community Cloud installs dependencies from the root `requirements.txt` and loads Streamlit configuration from `.streamlit/config.toml`. Keep all secrets in Community Cloud settings, never in Git.
