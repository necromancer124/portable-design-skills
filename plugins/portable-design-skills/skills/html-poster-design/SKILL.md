---
name: html-poster-design
description: "Use when the user asks for a poster, flyer, social media image, announcement, event graphic, fan tribute, or visual quote, or wants one revised with a new photo, name, palette, or language. Builds the poster as editable HTML/CSS at exact dimensions, keeps supplied images uncropped, makes separate language variants, exports a high-resolution PNG with the bundled Playwright renderer, and inspects the render."
license: MIT
compatibility: Authoring works with any Markdown-reading agent. PNG export requires Python 3.10+, Playwright, and an explicitly installed Chromium, Chrome, or Edge browser.
metadata:
  author: Portable Design Skills contributors
  version: "1.0.0"
  related-skills: sanzo-wada-design artifact-design
---

# HTML poster design and export

## Overview
Use HTML/CSS as an editable design canvas, then render the actual PNG. This skill provides `scripts/render.py` and `assets/poster.html`. It is not a diffusion model or an image-generation API. It requires no AI-provider subscription or API key.

## When to use
- The user wants a poster, shareable image, fan tribute, announcement, or visual quote.
- An existing poster needs a new photo, name, palette, or language.
- Multiple PNGs must share a layout while preserving the requested languages and character sets.

## Workflow

### 1. Resolve the brief
Confirm the subject, exact visible name/pronouns, language, photo choice, and crop policy. Ask only if one of those is genuinely ambiguous. A supplied screenshot is not automatically permission to remove its surrounding text. Keep personal images local unless explicitly authorized for publication.

Name the intended composition and dimensions. A portrait canvas might be 1080 by 1350 CSS pixels, but choose dimensions to fit the content; do not make every poster a screenshot of the same website.

Done: one subject, a clear reading order, and explicit dimensions.

### 2. Select a real palette
Use the sibling `../sanzo-wada-design/SKILL.md` if requested. Retrieve an actual combination, map it to paper, ink, accent, and panels, and verify each text/background pair. Use original `--wada-color-N` tokens, with semantic variables separate. Any supporting neutral or derived shade must be labeled with its exact HEX.

Done: color provenance is recorded, not guessed from visual resemblance.

### 3. Author the editable HTML
Start from `assets/poster.html` only if it suits the brief. Copy it to a working/output directory rather than editing an installed skill. Keep CSS and JS embedded for portability, and avoid external fonts when offline delivery matters.

Use a `.poster` element with explicit width/height. Grid rows are useful, but inspect content height: min-content can still overflow a fixed row. Avoid absolute bottom footers unless the content above is measured. Use HTML escaping when inserting plain text programmatically; permit markup only for intentionally authored structure.

For full-image preservation:

```css
.photo { width: 100%; height: auto; object-fit: contain; }
```

For a bounded frame, set both frame dimensions and keep `object-fit: contain`. Embed local image bytes as data URLs for a self-contained file; keep original aspect ratio and do not pretend that upscaling adds detail. Use `cover` only when the brief permits cropping. Do not include a private image in a reusable public template.

Done: complete UTF-8 HTML exists; names and visible text are correct.

### 4. Create separate language variants
Set the HTML `lang` attribute to the requested language, such as `<html lang="ru">` for Russian. Translate naturally rather than word-by-word; retain requested exact phrases when intentional. Inspect punctuation, line wraps, Cyrillic support, and fallback fonts in the rendered image.

Keep faces, flags, logos, and photographs unchanged unless the user explicitly requests an image transformation. A politician's slogan is not a verified quote. Check quotations against a reliable source, or clearly call them user-written copy. Never invent a named person's endorsement.

Done: each language file has independently reviewed text, direction, and line breaks.

### 5. Install the optional renderer deliberately
PNG export needs Playwright for Python and a browser, installed by the user. Point them to the official guide at https://playwright.dev/python/docs/intro (Python package plus its Chromium browser); do not install anything on your own. A dedicated environment is a good idea. Run `python3` instead of `python` if that is the executable on the host.

The renderer defaults to downloaded Chromium. Alternatively use `--browser chrome` or `--browser msedge` for an already-installed channel. It does not install browsers, discover secret profiles, attach to the user's browser, or silently switch providers. Headless rendering uses a fresh browser context.

Done: a documented installed browser is available, or the blocker is reported honestly.

### 6. Export the actual artifact
From the plugin root (`${CLAUDE_PLUGIN_ROOT}` when installed as a Claude Code plugin):

```sh
python skills/html-poster-design/scripts/render.py skills/html-poster-design/assets/poster.html --output output/poster.png --selector .poster --width 1080 --height 1350 --scale 2
```

For an installed skill, replace the script/template paths with that skill's actual directory. When installed as a Claude Code plugin, that directory is `${CLAUDE_PLUGIN_ROOT}/skills/html-poster-design`, so the script is `${CLAUDE_PLUGIN_ROOT}/skills/html-poster-design/scripts/render.py` and the template is `${CLAUDE_PLUGIN_ROOT}/skills/html-poster-design/assets/poster.html`. Write output to the user's working directory, not inside the plugin folder. Output at scale 2 is twice the CSS width and height. Use `--full-page` instead of `--selector` for a full-page website screenshot. The renderer blocks HTTP(S) asset requests by default. Prefer embedded or downloaded assets; use `--allow-network` only with deliberate permission to request remote resources.

Only render trusted HTML. Network blocking is not a security sandbox: JavaScript executes, local file references may be readable by the browser, and no protection against arbitrary hostile HTML is promised. The process checks broken images and page JavaScript errors, but does not audit every CSS box, CSS background image, or accessibility criterion.

Done: a real PNG exists; a zero exit status is not a substitute for seeing it.

### 7. Inspect and deliver
Open the PNG in the agent's image viewer. Check headline/quote/footers, image crop, labels, and punctuation. If clipped, repair the composition and rerender. Keep the previous version when making significant revisions. Reopen or attach the final file the user will receive, not a stale screenshot.

Provide PNG and editable HTML if requested. For a requested Desktop copy, discover the actual Desktop path instead of assuming an English folder or ignoring OneDrive redirection. Copy only the requested artifacts and read them back or compare hashes before claiming success. Use your host agent's file-delivery tools; no Hermes-specific delivery marker is required by the skill.

Done: concise delivery with exact paths/URLs and an accurate account of verification. No unsolicited git commits or public uploads.

## Common pitfalls
- Using a screenshot of the old version after editing HTML.
- Suppressing broken images or substituting an unrelated photo without saying so.
- A `width` change that distorts an image because a fixed height remains.
- A footer hiding body text or punctuation wrapping onto the wrong line.
- Assuming the user's Desktop is `~/Desktop` on every OS.
- Claiming a full test suite passed after merely rendering the image.

## Verification checklist
- [ ] Correct subject, name, pronouns, language, and version scope.
- [ ] Colors retrieved and actual text pairs checked.
- [ ] Image policy respected; no private material in public examples.
- [ ] PNG exported and visually inspected.
- [ ] Requested destination copies confirmed.
- [ ] Known limitations distinguished from automated checks.
