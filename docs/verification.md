# Verification and limits

## Commands

```sh
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python -m unittest discover -s tests -v
python skills/sanzo-wada-design/scripts/palettes.py --self-test
python skills/html-poster-design/scripts/render.py skills/html-poster-design/assets/poster.html --output output/poster.png --selector .poster
```

Use `python3` if needed. For existing Chrome/Edge installations, add `--browser chrome` or `--browser msedge`; set `RENDER_BROWSER` to the same channel for browser tests. Windows PowerShell uses `$env:RENDER_BROWSER = 'msedge'`; POSIX shells use `RENDER_BROWSER=msedge python ...`.

The tests cover skill-frontmatter structure, relative references, dataset size and membership, palette lookup/filtering/invalid input, contrast arithmetic, and a real local HTML-to-PNG render when Playwright is installed. Browser tests require an installed browser and are explicitly skipped if the Playwright Python package is absent; a skipped browser test is not a verified renderer.

CI is configured for Windows and Linux with Python 3.11 and installed Chromium. Check the actual Actions run before claiming remote CI is green. Local Edge success is not proof of Linux/Chromium success.

## Boundaries

- Contrast helper checks opaque six-digit sRGB pairs, not a full WCAG audit.
- Wada colors are screen approximations, not certified print values.
- The upstream Dull Violet Black CMYK entry has an out-of-range value; it is preserved and reported rather than silently fixed.
- Renderer checks `<img>` decoding and JavaScript exceptions, but visual review is still needed for overflow, CSS backgrounds, font substitution, and RTL.
- HTTP(S) blocking is not a sandbox. Render only trusted HTML.
- No paid AI APIs or account credentials are needed by the included scripts.
- Open Agent Skills format compatibility is not a promise of auto-discovery in every AI product. See `compatibility.md`.
