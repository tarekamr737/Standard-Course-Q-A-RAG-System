# PRODUCT.md

## Product Name
CourseGround

## Product Summary
CourseGround is a Streamlit-based Retrieval-Augmented Generation application that helps students ask questions about course materials and receive grounded answers with clear source attribution.

The system supports three courses and accepts PDF, CSV, DOCX, and TXT files. It extracts, cleans, chunks, embeds, and indexes the content, then retrieves the most relevant passages before generating an answer through OpenRouter.

## Primary Users
- Students reviewing course content.
- Teaching assistants answering repeated questions.
- Instructors validating whether course materials cover a topic.

## Core User Goals
- Select a course and ask a natural-language question.
- Receive a concise answer based only on uploaded materials.
- Inspect the exact sources used to generate the answer.
- Upload or update course files and rebuild the knowledge base.

## Main User Flow
1. Open the app.
2. Select one of the three courses.
3. Confirm that course materials are indexed.
4. Ask a question in the chat input.
5. View the generated answer.
6. Expand the source section to inspect citations and retrieved excerpts.
7. Ask follow-up questions within the same course context.

## Core Features
- Three-course knowledge base.
- Support for PDF, CSV, DOCX, and TXT.
- File upload and indexing workflow.
- Course-level search isolation.
- Conversational Q&A interface.
- Grounded answers with source citations.
- Retrieved-context viewer.
- No-answer fallback when evidence is insufficient.
- Indexing status and document summary.
- Clear loading, success, warning, and error states.

## AI Stack
- LLM: `google/gemma-4-26b-a4b-it:free` through OpenRouter.
- Embeddings: `nvidia/nemotron-3-embed-1b:free` through OpenRouter.
- Retrieval: vector similarity search with metadata filtering.
- Response policy: answer only from retrieved course content.

## Information Architecture

### Sidebar
- Product logo and name.
- Course selector.
- Knowledge-base status.
- Indexed file count.
- Upload materials action.
- Rebuild index action.
- Settings for retrieval depth and optional advanced controls.

### Main Workspace
- Selected course title and short description.
- Suggested questions for first-time users.
- Chat conversation area.
- User question cards.
- Assistant answer cards.
- Inline citation markers.
- Expandable source panel under each answer.
- Persistent question input at the bottom.

### Source Panel
Each source item should show:
- File name.
- File type.
- Page, section, or row reference when available.
- Relevance score if exposed.
- Short retrieved excerpt.

## Key Screens and States

### 1. Ready State
- Course selected.
- Knowledge base indexed.
- Suggested starter questions visible.
- Question input active.

### 2. Empty Knowledge Base
- Explain that no materials are indexed.
- Provide a prominent upload action.
- Show supported file types.

### 3. Upload and Indexing
- Drag-and-drop upload area.
- Uploaded-file list with type and size.
- Indexing progress and current step.
- Success summary after indexing.

### 4. Answering State
- User question immediately added to chat.
- Visible generation/loading state.
- Input temporarily disabled or clearly busy.

### 5. Answer With Sources
- Concise answer first.
- Citation markers connected to source cards.
- Expandable evidence section.

### 6. Insufficient Evidence
- State that the uploaded course materials do not contain enough information.
- Avoid guessing.
- Suggest a more specific question or another course.

### 7. Error State
- Human-readable message.
- Retry action.
- No exposure of API keys or internal stack traces.

## Visual Direction
Create a polished academic productivity tool rather than a generic chatbot.

The interface should feel:
- Trustworthy.
- Focused.
- Modern.
- Calm.
- Evidence-driven.

Use a clean light-first design with strong readability, generous spacing, subtle borders, soft elevation, and restrained color usage. The selected course can provide a small accent color, but the product should remain visually consistent.

Avoid:
- Neon AI aesthetics.
- Excessive gradients.
- Decorative illustrations that reduce focus.
- Dense dashboards.
- Oversized chat bubbles.
- Hidden citations.

## Design System Guidance
- Desktop-first responsive layout.
- Maximum readable content width for answers.
- Clear typography hierarchy.
- Accessible contrast meeting WCAG AA.
- Keyboard-accessible controls and visible focus states.
- Color-blind-safe status indicators supported by text and icons.
- Reduced-motion-friendly transitions.
- Consistent 8-point spacing system.
- Reusable cards, badges, tabs, accordions, progress indicators, and alerts.

## Suggested Components
- Course selector.
- Knowledge-base status badge.
- File uploader.
- Indexed-file table.
- Suggested-question chips.
- Chat message cards.
- Citation chips.
- Source accordion.
- Retrieved-excerpt card.
- Progress indicator.
- Empty-state panel.
- Error alert.
- Sticky question composer.

## Content Style
- Use concise, student-friendly language.
- Clearly separate generated answers from source evidence.
- Label citations with understandable references such as `Lecture 2, page 6`.
- Never imply certainty when retrieved evidence is weak.
- Prefer “The course materials do not provide enough information” over speculative answers.

## Success Criteria
- A student can select a course and ask a question without instructions.
- Every supported answer includes inspectable source attribution.
- Questions cannot retrieve content from another course.
- Unsupported questions produce a clear no-answer response.
- Uploading and indexing status is understandable at every step.
- The app works across desktop, tablet, and mobile layouts.
- Chrome DevTools MCP evaluation reports no critical accessibility, responsiveness, performance, or console issues.

## Stitch Design Request
Generate a complete responsive UI design for this Streamlit product, including:
- Main Q&A workspace.
- Sidebar navigation and course selector.
- Empty knowledge-base state.
- File upload and indexing state.
- Answer with citations and expanded sources.
- Insufficient-evidence state.
- Error state.
- Mobile layout.

The final design should be implementation-friendly for Streamlit and avoid interactions that require a complex custom frontend.
