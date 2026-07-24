# TASKS.md

## 1. Project Setup
- [x] Initialize the Streamlit project and virtual environment.
- [x] Add configuration for OpenRouter API keys and model IDs.
- [x] Create the project structure for ingestion, retrieval, generation, UI, and tests.

## 2. Course Materials
- [x] Prepare materials for 3 courses using PDF, CSV, DOCX, and TXT files.
- [x] Organize files by course and validate supported formats.
- [x] Add sample questions and expected answers for evaluation.

## 3. Document Ingestion
- [x] Implement loaders for PDF, CSV, DOCX, and TXT.
- [x] Clean and normalize extracted text.
- [x] Preserve metadata: course, file name, page, section, and chunk ID.
- [x] Chunk documents using configurable size and overlap.

## 4. Embeddings and Vector Store
- [x] Generate embeddings with `nvidia/nemotron-3-embed-1b:free` through OpenRouter.
- [x] Store embeddings and metadata in a vector database.
- [x] Support indexing, re-indexing, and course-level filtering.

## 5. Retrieval and Generation
- [x] Build a similarity-based retriever with configurable `top_k`.
- [x] Restrict retrieval to the selected course.
- [x] Connect the retriever to `google/gemma-4-31b-it:free` through OpenRouter.
- [x] Add a grounded prompt that answers only from retrieved materials.
- [x] Return a clear fallback when the answer is not supported by the sources.
- [x] Include source attribution for every answer.

## 6. Streamlit App
- [x] Build the UI using the Impeccable skill.
- [x] Add course selection, file ingestion, indexing status, and chat interface.
- [x] Allow users to create a persistent new course from the sidebar.
- [x] Display answers, citations, retrieved excerpts, and source metadata.
- [x] Add loading, empty, success, warning, and error states.
- [x] Keep API keys outside the UI and source code.

## 7. Evaluation and Testing
- [x] Test all supported file formats and malformed files.
- [x] Evaluate retrieval relevance, groundedness, citation accuracy, and fallback behavior.
- [x] Test cross-course isolation and prompt-injection resistance.
- [x] Add unit and integration tests for loaders, chunking, embeddings, retrieval, and generation.
- [x] Evaluate the final UI and user flows using Chrome DevTools MCP.
- [x] Fix accessibility, responsiveness, performance, and console issues.

## 8. Delivery
- [x] Add setup instructions, environment variables, architecture, and usage examples to README.
- [x] Add `.env.example`, dependency file, and sample course data structure.
- [x] Verify a clean local run and prepare the Streamlit deployment configuration.
- [x] Prepare GitHub publication safeguards and Streamlit Community Cloud deployment guidance.

> Operational note: CourseGround now detects embedding or chunk-setting changes and requires a re-index before querying. The AI-Based Programming course is indexed with OpenRouter (240 chunks) and its grounded retrieval evaluation passed. The original sample-course indexes remain local-preview indexes until separately rebuilt with OpenRouter embeddings.
