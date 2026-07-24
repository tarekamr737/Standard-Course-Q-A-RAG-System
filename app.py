"""CourseGround Streamlit application."""

from __future__ import annotations

import html
from pathlib import Path

import streamlit as st

from courseground.config import COURSES, INDEX_DIR, MATERIALS_DIR, UPLOADS_DIR, Settings, ensure_data_directories
from courseground.embeddings import embedding_client
from courseground.indexing import CourseIndexer
from courseground.loaders import SUPPORTED_EXTENSIONS, discover_course_files
from courseground.models import Answer
from courseground.rag import GroundedAnswerer
from courseground.vector_store import LocalVectorStore


st.set_page_config(page_title="CourseGround", page_icon="▱", layout="wide", initial_sidebar_state="auto")


APP_CSS = """
<style>
:root {
  --ink: #131b2e; --muted: #515f74; --faint: #737686; --paper: #faf8ff;
  --canvas: #ffffff; --side: #f2f3ff; --line: #c3c6d6; --line-soft: #e2e8f0;
  --blue: #0043ae; --blue-dark: #00328a; --blue-wash: #e7edff;
  --source: #f1f5f9; --green: #08745c; --green-wash: #d9f7ea;
  --amber: #9a6100; --amber-wash: #fff0c5; --red: #ba1a1a; --red-wash: #ffdad6;
}
.stApp { background: var(--paper); color: var(--ink); font-family: 'Inter', ui-sans-serif, system-ui, sans-serif; }
[data-testid='stAppViewContainer'] > .main { background: var(--canvas); }
[data-testid='stHeader'] { background: transparent; }
[data-testid='stToolbar'] { right: 1rem; }
[data-testid='stSidebar'] { background: var(--side); border-right: 1px solid var(--line-soft); min-width: 280px; }
[data-testid='stSidebar'] > div:first-child { padding: 1.75rem 1.5rem 1.5rem; }
.block-container { max-width: 68rem; padding: 3.25rem 2.5rem 8rem; }
@media (max-width: 740px) { .block-container { padding: 1.5rem 1rem 7rem; } [data-testid='stSidebar'] { min-width: 0; } }
h1, h2, h3 { font-family: 'Hanken Grotesk', ui-sans-serif, system-ui, sans-serif; color: var(--ink); text-wrap: balance; }
div[data-testid='stMarkdownContainer'] h1 { font-family: 'Source Serif 4', Georgia, serif !important; font-size: clamp(2.25rem, 5vw, 3.5rem); line-height: 1.08; letter-spacing: -0.025em; font-weight: 600; margin: 0 0 1.75rem; }
h2 { font-size: 1.25rem; letter-spacing: -0.01em; margin: 0; }
p, li { color: var(--muted); }
.cg-brand { display:flex; align-items:center; gap:.65rem; margin: .25rem 0 2.75rem; color:var(--blue); font:700 1.65rem/1 'Hanken Grotesk',sans-serif; letter-spacing:-.04em; }
.cg-mark { width:2rem; height:2rem; display:grid; place-items:center; border:2px solid var(--blue); border-radius:.45rem; font-size:1rem; }
.cg-eyebrow { margin: 1.75rem 0 .7rem; color: var(--faint); font: 700 .72rem/1.2 'Inter',sans-serif; letter-spacing: .09em; }
.cg-status { display:flex; gap:.8rem; align-items:flex-start; padding: .7rem 0 1.2rem; }
.cg-status-dot { flex:0 0 auto; display:grid; place-items:center; width:1.55rem; height:1.55rem; border-radius:99px; background:var(--green); color:#fff; font-weight:700; }
.cg-status-name { color: var(--green); font: 700 1.15rem/1.2 'Hanken Grotesk',sans-serif; }
.cg-status-detail { margin-top:.22rem; color:var(--muted); font-size:.82rem; }
.cg-empty-dot { background: var(--amber); }
.cg-empty-name { color: var(--amber); }
.cg-file-row { display:flex; gap:.5rem; justify-content:space-between; align-items:center; color:var(--ink); font-size:.88rem; padding:.52rem 0; border-bottom:1px solid var(--line-soft); }
.cg-file-row:last-child { border:0; }
.cg-file-count { color:var(--muted); font-variant-numeric: tabular-nums; }
.cg-index-card { border:1px solid var(--line); border-radius:.65rem; padding:1rem; margin:1.75rem 0; background:#f8f9ff; }
.cg-index-card strong { display:block; color:var(--ink); font-size:.9rem; margin-bottom:.3rem; }
.cg-index-card p { margin:0; font-size:.82rem; line-height:1.45; }
.cg-kicker { color:var(--blue); font:700 .76rem/1.2 'Inter',sans-serif; letter-spacing:.08em; text-transform:uppercase; margin-bottom:.8rem; }
.cg-subtitle { margin:-1.1rem 0 2rem; font-size:1rem; }
.cg-suggestions { display:flex; flex-wrap:wrap; gap:.65rem; margin:0 0 2rem; }
.cg-question { border:1px solid var(--line); border-radius:.55rem; padding:1.15rem 1.3rem; background:#fff; color:var(--ink); font-size:1.05rem; line-height:1.5; margin: 2.1rem 0 1.6rem; }
.cg-answer { border-top:1px solid var(--line); padding-top:1.5rem; margin-top:1rem; }
.cg-answer-label { display:flex; gap:.55rem; align-items:center; color:var(--ink); font:700 1.12rem/1.2 'Hanken Grotesk',sans-serif; margin-bottom:.9rem; }
.cg-answer-copy { color:var(--ink); font: 400 1.14rem/1.7 'Source Serif 4', Georgia, serif; max-width: 65ch; text-wrap:pretty; }
.cg-answer-copy p { color:var(--ink); margin:0 0 1rem; }
.cg-answer-copy sup { color:var(--blue); font-family:'Inter',sans-serif; font-weight:700; }
.cg-citation-line { display:flex; align-items:center; gap:.65rem; color:var(--faint); font-size:.82rem; padding:.85rem 0; border-top:1px solid var(--line-soft); }
.cg-evidence-head { display:flex; justify-content:space-between; align-items:center; gap:1rem; color:var(--ink); font:700 1.2rem/1.2 'Hanken Grotesk',sans-serif; }
.cg-evidence-count { display:inline-grid; place-items:center; min-width:1.75rem; height:1.75rem; padding:0 .4rem; border-radius:99px; background:var(--blue-wash); color:var(--blue); font:700 .8rem/1 'Inter',sans-serif; }
.cg-source { display:grid; grid-template-columns: 2.25rem 1fr auto; gap:.85rem; align-items:start; padding:1rem 0; border-bottom:1px solid var(--line); }
.cg-source:last-child { border:0; }
.cg-source-num { display:grid; place-items:center; width:1.75rem; height:1.75rem; background:var(--blue); color:#fff; border-radius:.28rem; font:700 .78rem/1 'Inter',sans-serif; }
.cg-source-title { color:var(--ink); font-size:.9rem; font-weight:700; line-height:1.35; }
.cg-source-excerpt { margin-top:.3rem; color:var(--muted); font:400 .98rem/1.5 'Source Serif 4',Georgia,serif; }
.cg-source-meta { color:var(--muted); font-size:.78rem; white-space:nowrap; }
.cg-empty { border:1px dashed var(--line); background:#fbfcff; padding:3rem 1.5rem; text-align:center; border-radius:.75rem; }
.cg-empty-icon { display:grid; place-items:center; width:3rem; height:3rem; margin:0 auto 1rem; border-radius:99px; background:var(--blue-wash); color:var(--blue); font-size:1.4rem; }
.cg-empty h2 { margin-bottom:.55rem; }
.cg-empty p { max-width:38ch; margin:0 auto; line-height:1.55; }
.cg-fallback { display:flex; gap:.8rem; align-items:flex-start; padding:1.15rem; border:1px solid #eacb7a; border-radius:.5rem; background:var(--amber-wash); margin:.8rem 0 1.25rem; }
.cg-fallback strong { color:#6d4300; display:block; margin-bottom:.25rem; }
.cg-fallback p { color:#6d4300; margin:0; line-height:1.45; }
.stButton > button { min-height:2.75rem; border-radius:.42rem; border:1px solid var(--blue); color:var(--blue); background:transparent; font-family:'Inter',sans-serif; font-weight:600; transition:background .18s ease-out, color .18s ease-out, transform .18s ease-out; }
.stButton > button:hover { color:#fff; background:var(--blue); border-color:var(--blue); }
.stButton > button:active { transform:translateY(1px); }
.stButton > button:focus-visible, [data-baseweb='select'] > div:focus-within { outline:3px solid #b3c5ff; outline-offset:2px; }
[data-testid='stBottom'] { background:#faf8ff; border-top:1px solid var(--line-soft); padding:1rem 2.5rem calc(1.25rem + env(safe-area-inset-bottom)); }
[data-testid='stBottom'] form { max-width:68rem; margin:0 auto; padding:.55rem .65rem; border:1px solid var(--line); border-radius:.6rem; box-shadow:0 5px 16px rgba(19,27,46,.08); background:#fff; }
[data-testid='stBottom'] [data-testid='stTextInput'] { flex:1; }
[data-testid='stBottom'] [data-testid='stTextInput'] input { font-family:'Inter',sans-serif; color:var(--ink); }
[data-testid='stBottom'] button[kind^='primary'] { min-height:2.5rem; background:var(--blue); border-color:var(--blue); color:#fff !important; }
[data-testid='stBottom'] button[kind^='primary'] p, [data-testid='stBottom'] button[kind^='primary'] svg, [data-testid='stBottom'] button[kind^='primary'] [data-testid='stIconMaterial'] { color:#fff !important; fill:currentColor; }
[data-testid='stExpander'] { border:0; border-top:1px solid var(--line); border-radius:0; background:transparent; margin-top:1.75rem; }
[data-testid='stExpander'] details { background:transparent; }
[data-testid='stExpander'] summary { color:var(--ink); font:700 1.15rem/1.2 'Hanken Grotesk',sans-serif; padding:.9rem 0; }
[data-testid='stAlert'] { border-radius:.5rem; }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition:none !important; animation:none !important; } }
@media (max-width: 620px) { .cg-source { grid-template-columns:2rem 1fr; } .cg-source-meta { grid-column:2; white-space:normal; } .cg-question { padding:1rem; } .cg-answer-copy { font-size:1.05rem; } }
</style>
"""


@st.cache_resource(show_spinner=False)
def services():
    settings = Settings.load()
    ensure_data_directories()
    store = LocalVectorStore(INDEX_DIR / "courseground-vectors.json")
    embedder = embedding_client(settings)
    indexer = CourseIndexer(store, embedder, settings.chunk_size, settings.chunk_overlap)
    answerer = GroundedAnswerer(settings, store, embedder)
    return settings, store, indexer, answerer


def safe(value: str) -> str:
    return html.escape(str(value), quote=True)


def course_files(course: str) -> list[Path]:
    return discover_course_files(course, [MATERIALS_DIR, UPLOADS_DIR])


def save_uploads(course: str, uploads) -> tuple[int, list[str]]:
    target = UPLOADS_DIR / course
    target.mkdir(parents=True, exist_ok=True)
    saved, errors = 0, []
    for upload in uploads:
        path = Path(upload.name)
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            errors.append(f"{path.name}: use PDF, CSV, DOCX, or TXT.")
            continue
        destination = target / path.name
        destination.write_bytes(upload.getbuffer())
        saved += 1
    return saved, errors


def render_sidebar(course: str, settings, store, indexer) -> None:
    info = COURSES[course]
    files = course_files(course)
    chunk_count = store.course_count(course)
    index_current = store.course_index_matches(course, indexer.index_signature())
    with st.sidebar:
        st.markdown("<div class='cg-brand'><span class='cg-mark'>▱</span>CourseGround</div>", unsafe_allow_html=True)
        st.markdown("<div class='cg-eyebrow'>COURSE</div>", unsafe_allow_html=True)
        selected = st.selectbox("Selected course", list(COURSES), index=list(COURSES).index(course), format_func=lambda code: COURSES[code]["name"], label_visibility="collapsed")
        if selected != course:
            st.session_state.course = selected
            st.session_state.history = []
            st.rerun()

        st.markdown("<div class='cg-eyebrow'>INDEX STATUS</div>", unsafe_allow_html=True)
        if chunk_count and index_current:
            state_html = f"<div class='cg-status'><span class='cg-status-dot'>✓</span><div><div class='cg-status-name'>Indexed</div><div class='cg-status-detail'>{chunk_count} searchable passages across {len(files)} files</div></div></div>"
        elif chunk_count:
            state_html = "<div class='cg-status'><span class='cg-status-dot cg-empty-dot'>!</span><div><div class='cg-status-name cg-empty-name'>Re-index needed</div><div class='cg-status-detail'>Your embedding or chunk settings changed. Rebuild before asking.</div></div></div>"
        else:
            state_html = "<div class='cg-status'><span class='cg-status-dot cg-empty-dot'>!</span><div><div class='cg-status-name cg-empty-name'>Not indexed</div><div class='cg-status-detail'>Index course materials to begin.</div></div></div>"
        st.markdown(state_html, unsafe_allow_html=True)

        if files:
            st.markdown("<div class='cg-eyebrow'>SOURCES</div>", unsafe_allow_html=True)
            for item in files[:6]:
                st.markdown(f"<div class='cg-file-row'><span>▧&nbsp; {safe(item.stem[:29])}</span><span class='cg-file-count'>{safe(item.suffix[1:].upper())}</span></div>", unsafe_allow_html=True)
            if len(files) > 6:
                st.caption(f"+ {len(files) - 6} more files")

        with st.expander("Upload materials", icon=":material/upload_file:", expanded=False):
            uploads = st.file_uploader("Add PDF, CSV, DOCX, or TXT", type=["pdf", "csv", "docx", "txt"], accept_multiple_files=True, key=f"uploads_{course}")
            if uploads and st.button("Save uploaded materials", key=f"save_{course}"):
                saved, errors = save_uploads(course, uploads)
                if saved:
                    st.success(f"Saved {saved} file{'s' if saved != 1 else ''}. Index to use them.")
                for error in errors:
                    st.error(error)

        action = "Rebuild course index" if chunk_count else "Index course materials"
        if st.button(action, key=f"index_{course}", icon=":material/database:", width="stretch"):
            progress = st.progress(0, text="Reading course materials…")
            try:
                progress.progress(35, text="Cleaning text and preserving source details…")
                summary = indexer.index_course(course, [MATERIALS_DIR, UPLOADS_DIR])
                progress.progress(80, text="Creating searchable course passages…")
                progress.progress(100, text="Index ready.")
                if summary.chunks:
                    st.success(f"Indexed {summary.chunks} passages from {summary.files} files.")
                else:
                    st.warning("No readable course material was found. Upload supported files, then try again.")
                for error in summary.errors:
                    st.warning(error)
                st.rerun()
            except Exception:
                st.error("Indexing did not finish. Check that the files are valid and try again.")

        st.markdown("<div class='cg-index-card'><strong>Your evidence stays visible</strong><p>Every supported answer includes the retrieved course passages used to answer it.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='cg-eyebrow'>SETTINGS</div>", unsafe_allow_html=True)
        st.caption(f"Retrieval depth: {settings.top_k} passages")
        if not settings.openrouter_api_key:
            st.info("Local preview mode is active. Add an OpenRouter key in `.env` for model-generated answers.")


def show_answer(answer: Answer) -> None:
    if not answer.supported:
        st.markdown("<div class='cg-fallback'><span aria-hidden='true'>⌕</span><div><strong>Insufficient course evidence</strong><p>The indexed materials do not support a confident answer. Try a more specific question or index additional sources.</p></div></div>", unsafe_allow_html=True)
        if answer.mode == "generation-error":
            st.warning(answer.text)
        return
    st.markdown("<div class='cg-answer'><div class='cg-answer-label'>Answer</div></div>", unsafe_allow_html=True)
    if answer.mode == "generation-fallback":
        st.info("The live model is temporarily unavailable, so this is a source-only evidence preview. Please retry for a synthesized answer.")
    st.markdown(f"<div class='cg-answer-copy'>{safe(answer.text).replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
    labels = " · ".join(f"[{item.number}] {safe(item.file_name)}, {safe(item.location)}" for item in answer.citations)
    st.markdown(f"<div class='cg-citation-line'>Evidence used: {labels}</div>", unsafe_allow_html=True)
    with st.expander(f"Evidence ({len(answer.citations)})", icon=":material/menu_book:", expanded=True):
        for item in answer.citations:
            st.markdown(
                f"<div class='cg-source'><span class='cg-source-num'>[{item.number}]</span><div><div class='cg-source-title'>{safe(item.file_name)} <span style='font-weight:500;color:#515f74'>· {safe(item.file_type)}</span></div><div class='cg-source-excerpt'>{safe(item.excerpt)}</div></div><span class='cg-source-meta'>{safe(item.location)}<br>score {item.score:.2f}</span></div>",
                unsafe_allow_html=True,
            )
    feedback_a, feedback_b, feedback_c = st.columns([1, 1, 4])
    feedback_a.button("Helpful", key=f"helpful_{len(st.session_state.history)}", icon=":material/thumb_up:")
    feedback_b.button("Not helpful", key=f"unhelpful_{len(st.session_state.history)}", icon=":material/thumb_down:")
    feedback_c.caption("Answers are grounded in the selected course only.")


def submit_question(question: str, course: str, store, indexer, answerer) -> None:
    question = question.strip()
    if not question:
        return
    if not store.course_count(course):
        st.session_state.notice = "Index this course before asking a question."
        return
    if not store.course_index_matches(course, indexer.index_signature()):
        st.session_state.notice = "Rebuild this course's index before asking. Its embedding or chunk settings changed."
        return
    with st.spinner("Checking the selected course materials…"):
        answer = answerer.answer(question, course)
    st.session_state.history.append({"question": question, "answer": answer})


def main() -> None:
    st.markdown(APP_CSS, unsafe_allow_html=True)
    st.session_state.setdefault("course", "CS4780")
    st.session_state.setdefault("history", [])
    course = st.session_state.course
    settings, store, indexer, answerer = services()
    render_sidebar(course, settings, store, indexer)

    info = COURSES[course]
    st.markdown(f"<div class='cg-kicker'>{safe(info['short_name'])}</div><h1>Ask your course materials</h1><p class='cg-subtitle'>{safe(info['description'])}</p>", unsafe_allow_html=True)
    if notice := st.session_state.pop("notice", None):
        st.warning(notice)

    index_current = store.course_index_matches(course, indexer.index_signature())
    if not store.course_count(course):
        st.markdown("<div class='cg-empty'><div class='cg-empty-icon'>▧</div><h2>Build this course’s evidence base</h2><p>CourseGround is ready for PDF, CSV, DOCX, and TXT materials. Upload files from the sidebar or index the included sample materials.</p></div>", unsafe_allow_html=True)
    elif not index_current:
        st.warning("Rebuild this course's index before asking. The current index was created with different embedding or chunk settings.")
    else:
        suggestions = [
            info["sample_question"],
            "What are the most important concepts in the indexed material?",
        ]
        with st.container(horizontal=True, gap="small"):
            for index, suggestion in enumerate(suggestions):
                if st.button(
                    suggestion,
                    key=f"suggestion_{course}_{index}",
                    icon=":material/auto_awesome:",
                ):
                    submit_question(suggestion, course, store, indexer, answerer)
                    st.rerun()
        for message in st.session_state.history:
            st.markdown(f"<div class='cg-question'>{safe(message['question'])}</div>", unsafe_allow_html=True)
            show_answer(message["answer"])

    with st.bottom:
        with st.form("course_question_form", border=False, clear_on_submit=True):
            with st.container(horizontal=True, vertical_alignment="bottom", gap="small"):
                question = st.text_input(
                    "Course question",
                    placeholder=f"Ask a question about {info['short_name']}…",
                    key="course_question_input",
                    label_visibility="collapsed",
                )
                submitted = st.form_submit_button(
                    "Ask",
                    type="primary",
                    icon=":material/arrow_upward:",
                    icon_position="right",
                    width="content",
                )
        if submitted:
            submit_question(question, course, store, indexer, answerer)
            st.rerun()


if __name__ == "__main__":
    main()
