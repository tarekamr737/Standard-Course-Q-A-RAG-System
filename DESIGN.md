---
name: Academic Precision
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#434654'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#737686'
  outline-variant: '#c3c6d6'
  surface-tint: '#0f55d2'
  primary: '#0043ae'
  on-primary: '#ffffff'
  primary-container: '#1a5ad7'
  on-primary-container: '#d7dfff'
  inverse-primary: '#b3c5ff'
  secondary: '#515f74'
  on-secondary: '#ffffff'
  secondary-container: '#d5e3fc'
  on-secondary-container: '#57657a'
  tertiary: '#484b4d'
  on-tertiary: '#ffffff'
  tertiary-container: '#606365'
  on-tertiary-container: '#dde0e1'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b3c5ff'
  on-primary-fixed: '#001849'
  on-primary-fixed-variant: '#003fa5'
  secondary-fixed: '#d5e3fc'
  secondary-fixed-dim: '#b9c7df'
  on-secondary-fixed: '#0d1c2e'
  on-secondary-fixed-variant: '#3a485b'
  tertiary-fixed: '#e0e3e5'
  tertiary-fixed-dim: '#c4c7c9'
  on-tertiary-fixed: '#191c1e'
  on-tertiary-fixed-variant: '#444749'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
  success-green: '#10B981'
  warning-amber: '#F59E0B'
  error-red: '#EF4444'
  source-background: '#F1F5F9'
  border-subtle: '#E2E8F0'
typography:
  headline-xl:
    fontFamily: Hanken Grotesk
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Source Serif 4
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 30px
  body-md:
    fontFamily: Source Serif 4
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  headline-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 800px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style

The design system is anchored in the concept of "Evidence-Driven Clarity." It moves away from the typical "fluorescent AI" aesthetic in favor of a **Corporate / Modern** style with **Minimalist** sensibilities. The goal is to evoke the feeling of a high-end research library or a premium academic journal—focused, quiet, and authoritative.

Key brand attributes:
- **Trustworthy:** Grounded in facts, not hallucinations.
- **Calm:** Reducing the cognitive load for students during intense study sessions.
- **Structured:** Information architecture that prioritizes source hierarchy over chat bubbles.

The UI utilizes generous whitespace, crisp borders, and a light-first aesthetic to maintain a sense of openness. Visual flourishes are restricted to functional elements like status indicators and source citations to ensure the student's focus remains on the learning material.

## Colors

The palette is intentionally restrained to promote focus. 
- **Primary:** A "Scholarly Blue" used for actions, active states, and primary branding.
- **Secondary:** A cool Slate used for secondary text and icons, providing enough contrast for readability without the harshness of pure black.
- **Neutrals:** A range of off-whites and light grays form the background layers, creating a subtle "paper-like" feel.
- **Status Colors:** Standard green, amber, and red are used for indexing states and error messages, always accompanied by icons or text to ensure accessibility (WCAG AA).

Backgrounds should default to white or the lightest gray (`#F8FAFC`) to keep the interface feeling fresh and clean.

## Typography

This system employs a dual-font strategy to balance UI utility with reading comfort:
- **UI Elements (Hanken Grotesk & Inter):** Used for navigation, labels, buttons, and headers. These clean sans-serifs provide a modern, technical feel.
- **Reading Content (Source Serif 4):** Specifically chosen for generated answers and retrieved excerpts. The serif structure aids long-form reading and differentiates "AI-generated knowledge" from the application's interface controls.

Scale is managed through a strict hierarchy. Large headlines on desktop scale down for mobile to maintain readability without overwhelming the viewport. "Label-sm" is frequently used for metadata (e.g., "PAGE 4" or "PDF") to provide clear categorization at a glance.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy for the main workspace to ensure optimal line lengths for reading. While the sidebar and peripheral elements adapt to screen width, the central "Content Well" is capped at 800px to prevent lines of text from becoming too wide to scan comfortably.

- **Rhythm:** An 8px base unit governs all padding and margins.
- **The Sidebar:** Occupies a fixed 280px on desktop, housing course selection and status info.
- **Mobile Reflow:** On mobile, the sidebar collapses into a top navigation bar or a hamburger menu. The Content Well expands to fill the screen width minus 16px margins on either side.
- **Verticality:** We use "Stack" units (8, 16, 32px) to separate distinct sections (e.g., a user's question and the assistant's answer are separated by a `stack-lg`).

## Elevation & Depth

To maintain a "clean" and "academic" feel, this design system avoids heavy shadows. Instead, it uses **Tonal Layers** and **Low-Contrast Outlines**.

- **Level 0 (Surface):** The main background (`#F8FAFC`).
- **Level 1 (Cards):** White background (`#FFFFFF`) with a subtle 1px border (`#E2E8F0`). No shadow.
- **Level 2 (Active/Focus):** A very soft, diffused shadow (Blur: 8px, Y: 4px, Color: 2% Black) used only when a card is being interacted with or for the persistent question input.
- **Source Panels:** Use a slightly darker background (`#F1F5F9`) to create a "nested" or "inset" feel, signaling that these are secondary details.

Depth is used to represent the importance of information. The most critical information (the answer) sits on the cleanest white surface, while supporting evidence (sources) is tucked into recessed tonal layers.

## Shapes

The design system uses a **Soft (1)** roundedness profile. 
- **Standard Elements:** 0.25rem (4px) for buttons, input fields, and small cards. This creates a disciplined, professional appearance.
- **Containers:** Larger cards or the main content area use 0.5rem (8px).
- **Interactive Indicators:** Elements like "Suggested Question" chips use 1rem (Pill) to distinguish them as highly interactive, clickable objects.

This subtle rounding prevents the interface from feeling "sharp" or unfriendly while maintaining the structural integrity required for an academic tool.

## Components

### Buttons & Inputs
- **Primary Button:** Solid Scholarly Blue (`#1A5AD7`) with white text. 4px rounded corners.
- **Ghost Button:** Transparent background with Primary border and text for secondary actions like "Rebuild Index."
- **Question Input:** A sticky footer component with a subtle elevation (Level 2). It should feature a clean, mono-line border that highlights Primary Blue on focus.

### Knowledge Base & Sources
- **Status Badges:** Small, rounded-sm tags (e.g., "Indexed", "Empty"). Use background tints (e.g., light green background with dark green text) for clarity.
- **Citation Chips:** Inline markers within the text (e.g., `[1]`). These should be small, Scholarly Blue, and hoverable to reveal the source name.
- **Source Accordions:** Collapsible sections at the bottom of answers. When expanded, they reveal Source Excerpt Cards.
- **Source Excerpt Cards:** Nested cards with a monospaced font for file names and a serif font for the excerpt.

### Messaging & Feedback
- **Answer Cards:** No bubble tails. Structured as a clean vertical flow. The "Assistant" response is identified by a small icon or label rather than a colored bubble.
- **Empty States:** Centered illustrations (simple icons, no complex art) with a Headline-MD and a clear Primary CTA button.
- **Progress Indicators:** Linear progress bars for indexing, using the Primary Blue. Avoid circular spinners for long-duration tasks to show measurable progress.