---
name: sanzo-wada-design
description: Use when designing with Sanzo Wada color palettes. Retrieve real combinations,
  map colors to UI roles, and verify contrast for websites, posters, and presentations.
license: 'MIT; bundled data: references/DATA-LICENSE.md'
compatibility: Palette helper requires Python 3.10+. No network, account, or paid
  API required.
metadata:
  author: Hermes Agent
  version: 1.0.1
  related-skills: artifact-design html-poster-design
---

# Sanzo Wada: source-backed color and modern design

## Overview
Use the palette relationships in **A Dictionary of Color Combinations / 配色事典**, Sanzo Wada, Seigensha, ISBN 978-4-86152-247-5, for websites, app interfaces, slides, diagrams, posters, and visual identities. This skill contains a community digital transcription, not a scan or the complete book. The publisher describes 348 combinations originating in Wada's work from 1933 onward.

`assets/colors.json` is Matt DesLauriers' MIT-licensed dataset, derived from Dain M. Blodorn Kim's transcription with corrections and profile-based CMYK-to-sRGB conversion. Preserve `references/DATA-LICENSE.md` and attribution when redistributing the data. See `references/sources.md` and `assets/provenance.json`.

**Source boundary:** names, CMYK entries, and combination membership are transcribed source data. HEX/RGB are the dataset maintainer's approximations, not original exact digital specifications. Layouts, typography, component roles, mood labels, and proportions below are modern adaptations, not quoted rules from Wada. Never imply the whole book was read or that the book is public domain. Never download an unauthorized full-book copy.

## When to use
- User asks for Sanzo Wada, the Japanese color dictionary, unusual harmonious colors, or book-inspired design.
- User explicitly invokes this skill for a website, document, presentation, illustration, or redesign.
- Complement the relevant artifact-building skill; this skill supplies color decisions, not a replacement implementation framework.
- Do not override an existing brand palette, explicit user colors, or the requested style without agreement.

## Workflow

### 1. Resolve the brief
Identify artifact, audience, existing brand constraints, light/dark preference, and the desired mood from the request. Infer sensible low-stakes defaults rather than asking a questionnaire. Do not interpret Japanese color inspiration as permission to add stereotypical motifs or decorative Japanese text.
**Done:** state a short design intent and respect the actual medium.

### 2. Retrieve actual combinations
Run the bundled standard-library-only helper with Python 3.10 or later (`python` or `python3`, whichever is installed). Resolve SKILL_DIR from this skill directory, not a machine-specific home path; quote paths. Use your agent's available file and shell tools, not any particular vendor's tool names.

```text
python "SKILL_DIR/scripts/palettes.py" --search green --size 3 --limit 8
python "SKILL_DIR/scripts/palettes.py" --id 125
python "SKILL_DIR/scripts/palettes.py" --size 4 --min-contrast 4.5 --limit 8
python "SKILL_DIR/scripts/palettes.py" --gallery "OUTPUT_DIR/wada-palettes.html"
```

Search matches original color names, not interpreted moods. Size and minimum contrast filters combine with search. A candidate passes minimum contrast if at least ONE pair qualifies: this is NOT approval for every pair or every component. The script reports pairwise contrast for explicit palette inspection.
Choose two or three genuinely distinct candidates when exploring, then recommend one. If the user already chose an ID, use it. Do not invent IDs, HEX codes, book page numbers, or palette membership.
**Done:** record combination ID, original names, source HEX values, and reason for selection.

### 3. Translate colors into roles
Choose a dominant field, supporting surface, accent, and readable ink. A two-color combination may be all that is needed; do not always choose four colors or the same favorite palette.
- Preserve original swatches in `--wada-color-1` etc.; map semantic tokens separately (`--background`, `--surface`, `--text`, `--accent`, `--on-accent`, `--border`, `--focus`).
- Prefer a restrained dominant field and deliberately smaller accents; area ratios are a design decision, not a historical fact. Equal-area swatch previews do not mandate equal-area page designs.
- Add neutral ink/paper or derived shades only if needed. Label each addition **supporting neutral** or **derived**, with its exact value and purpose. Never mislabel an adaptation as an original Wada color.
- In multi-page artifacts, centralize tokens and repeat the same semantic roles. Respect light/dark variants as separate designs with separately verified contrast.
**Done:** provide a compact source-to-role mapping; original and added colors are distinguishable.

### 4. Build an appropriate composition
Modern adaptations to explore: clear hierarchy, intentional negative space, balanced warm/cool fields, crisp color-block relationships, and one deliberate contrasting accent. These are choices for the task, NOT claims about the author's layout philosophy.
Use typography and spacing appropriate to the medium and user. Avoid automatically imposing beige paper, distressed textures, faux Japanese styling, thin serif text, gradients, glassmorphism, or pill-shaped cards on every project. The book is a color resource, not a universal layout template.
For a website, demonstrate a real heading, body copy, navigation, button and card rather than only swatches. For slides/posters, show title/body hierarchy and actual content. Respect existing project conventions and reuse shared components.
**Done:** colors function in a realistic composition, not just a palette strip.

### 5. Verify accessibility and implementation
```text
python "SKILL_DIR/scripts/palettes.py" --contrast "#FOREGROUND" "#BACKGROUND"
python "SKILL_DIR/scripts/palettes.py" --self-test
```
Use numeric six-digit HEX values, not the placeholders above. Check every ACTUAL text/background pair, including button labels and hover/focus states. For opaque sRGB colors, target WCAG AA 4.5:1 normal text and 3:1 large text; large is at least 18 pt regular or 14 pt bold. Relevant UI boundaries and meaningful graphics generally require 3:1 against adjacent colors. Do not round a failing ratio upward to pass. The helper does not assess opacity, images, gradients, font size, keyboard behavior, or complete WCAG conformance.
If a pair fails, first change role assignment or add a declared neutral; if altering a source color is necessary, label it derived and rerun the check. Never rely on color alone for statuses. Verify rendered layouts using available browser/vision tools when delivering a visual artifact; numerical checks alone do not verify the whole interface.
**Done:** record tested pairs and limitations, exercise the artifact, and do not claim a visual inspection that did not occur.

### 6. Deliver
Give the working artifact, selected combination ID/names, compact role mapping, contrast results, and a short attribution: palette adapted from Sanzo Wada via Matt DesLauriers' digital dataset. Keep provenance detail in linked notes rather than flooding the user.

## Common pitfalls
- Different online transcriptions have different conversions and some different memberships. Use this bundled dataset consistently; do not mix its IDs/HEX values with another site without checking.
- Upstream anomaly: Dull Violet Black has CMYK [95, 106, 38, 50] (magenta exceeds 100). Preserve provenance; use the supplied HEX for screen work, but flag and independently verify CMYK before print. Self-test reports this warning rather than falsely treating the original data as pristine.
- A historical harmonious palette is not automatically accessible UI.
- --min-contrast identifies at least one useful pairing, not universal readability.
- Palette array order is dataset order, not verified printed spatial arrangement.
- Do not treat all original palettes as a required theme for every future task; use this skill when relevant and honor user direction.
- Do not change the host application theme or settings just because this skill is loaded. Apply palettes only to the requested artifact.

## Verification checklist
- [ ] Existing combination retrieved from bundled data; names and values retained.
- [ ] Original swatches separated from derived/supporting tokens.
- [ ] Modern design interpretation not presented as book quotation.
- [ ] Actual text/background and control-state contrast measured.
- [ ] Artifact exercised; visual inspection and limitations reported honestly.
- [ ] Attribution and dataset license retained where data is redistributed.
