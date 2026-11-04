"""Offline Wada palette lookup, contrast checks, and HTML swatch gallery. Stdlib only."""
import argparse
import html
import itertools
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def luminance(value):
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        raise ValueError("Expected a six-digit HEX color, for example #ffffff")
    rgb = [int(value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
    return sum(v * w for v, w in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(a, b):
    low, high = sorted((luminance(a), luminance(b)))
    return (high + 0.05) / (low + 0.05)


def palettes():
    colors = json.loads((ROOT / "assets/colors.json").read_text(encoding="utf-8"))
    result = {}
    for c in colors:
        for identifier in c["combinations"]:
            result.setdefault(identifier, []).append(c)
    return colors, dict(sorted(result.items()))


def report(identifier, colors):
    pairs = []
    for a, b in itertools.combinations(colors, 2):
        ratio = contrast(a["hex"], b["hex"])
        pairs.append({"a": a["name"], "b": b["name"], "ratio": round(ratio, 4),
                      "normal_text_AA": ratio >= 4.5, "large_text_AA": ratio >= 3})
    return {"combination": identifier, "colors": [{"name": c["name"], "hex": c["hex"], "cmyk": c["cmyk"]} for c in colors], "pairs": pairs}


def gallery(items, destination):
    cards = []
    for identifier, colors in items:
        swatches = []
        for c in colors:
            ink = max(("#000000", "#ffffff"), key=lambda t: contrast(t, c["hex"]))
            swatches.append('<div class="swatch" style="background:' + c["hex"] + ';color:' + ink + '"><strong>' + html.escape(c["name"]) + '</strong><code>' + c["hex"] + '</code></div>')
        cards.append('<article data-search="' + html.escape(' '.join(c['name'] for c in colors).lower(), quote=True) + '"><h2>Combination ' + str(identifier) + '</h2><div class="colors">' + ''.join(swatches) + '</div></article>')
    document = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sanzo Wada palette library</title>
<style>*{box-sizing:border-box}body{margin:0;background:#faf9f6;color:#202020;font:16px/1.5 system-ui,sans-serif}header{padding:32px clamp(16px,4vw,56px);border-bottom:1px solid #777}h1{font-size:clamp(28px,4vw,48px);margin:0}p{max-width:75ch}label{display:block;font-weight:650}input{padding:12px;width:min(100%,480px);font:inherit;border:1px solid #555;border-radius:4px}main{padding:24px clamp(16px,4vw,56px);display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:24px}article{border:1px solid #777;background:#fff;padding:16px}h2{font-size:17px;margin:0 0 12px}.colors{display:flex;min-height:190px}.swatch{flex:1;padding:12px 8px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;overflow-wrap:anywhere}.swatch strong{font-size:14px}.swatch code{font-size:12px}footer{padding:24px}a{color:#164f80}[hidden]{display:none!important}</style>
<header><h1>Sanzo Wada / Color combinations</h1><p>Book-derived combinations; digital sRGB approximations by Matt DesLauriers, based on Dain M. Blodorn Kim's transcription. Swatch order is dataset order. UI and layout are modern adaptations, not pages from the book.</p><label for="search">Find a color name or combination number</label><input id="search" type="search" placeholder="Try green, pink, or 125"><p id="count" aria-live="polite"></p></header><main>''' + ''.join(cards) + '''</main><footer>Source: <a href="https://github.com/mattdesl/dictionary-of-colour-combinations">MIT-licensed digital dataset</a>. Book: <a href="https://www.seigensha.com/books/978-4-86152-247-5/">Sanzo Wada, Seigensha</a>. Supporting page neutrals and typography are not original book specifications.</footer><script>const search=document.getElementById('search');function filter(){let n=0;for(const card of document.querySelectorAll('article')){card.hidden=!(card.dataset.search+' '+card.querySelector('h2').textContent.toLowerCase()).includes(search.value.toLowerCase().trim());if(!card.hidden)n++}document.getElementById('count').textContent=n+' combinations'}search.addEventListener('input',filter);filter();</script></html>'''
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document, encoding="utf-8")
    return {"gallery": str(path.resolve()), "combinations": len(cards)}


def self_test(colors, all_palettes):
    assert len(colors) == 159
    assert set(all_palettes) == set(range(1, 349))
    assert all(len(cs) in (2, 3, 4) for cs in all_palettes.values())
    assert len({c['name'] for c in colors}) == len(colors)
    for c in colors:
        luminance(c['hex'])
        assert [int(c['hex'][i:i + 2], 16) for i in (1, 3, 5)] == c['rgb']
        assert len(c['cmyk']) == 4
        assert all(isinstance(v, (int, float)) for v in c['cmyk'])
    assert abs(contrast('#000000', '#ffffff') - 21) < 1e-10
    assert contrast('#abcdef', '#abcdef') == 1
    assert contrast('#000000', '#ffffff') == contrast('#ffffff', '#000000')
    for bad in ('white', '#fff', '#gggggg'):
        try:
            luminance(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid HEX accepted')
    warnings = [{"name": c['name'], "cmyk": c['cmyk'], "warning": "Upstream CMYK out of range; preserved, not silently corrected. Use provided HEX for screen work; verify print values independently."} for c in colors if any(v < 0 or v > 100 for v in c['cmyk'])]
    return {"self_test": "PASS", "colors": len(colors), "combinations": len(all_palettes), "source_data_warnings": warnings}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--id', type=int)
    p.add_argument('--search', default='')
    p.add_argument('--size', type=int, choices=(2, 3, 4))
    p.add_argument('--min-contrast', type=float, default=1)
    p.add_argument('--limit', type=int)
    p.add_argument('--contrast', nargs=2, metavar=('FOREGROUND', 'BACKGROUND'))
    p.add_argument('--gallery')
    p.add_argument('--self-test', action='store_true')
    a = p.parse_args()
    if a.limit is not None and a.limit < 1:
        p.error('--limit must be positive')
    if not 1 <= a.min_contrast <= 21:
        p.error('--min-contrast must be between 1 and 21')
    if a.contrast:
        try:
            ratio = contrast(*a.contrast)
        except ValueError as e:
            p.error(str(e))
        print(json.dumps({"ratio": round(ratio, 4), "normal_text_AA": ratio >= 4.5, "large_text_AA": ratio >= 3}))
        return
    colors, all_palettes = palettes()
    if a.self_test:
        print(json.dumps(self_test(colors, all_palettes)))
        return
    if a.id is not None and a.id not in all_palettes:
        p.error('Combination ID must exist in dataset (1-348)')
    selected = []
    for identifier, cs in all_palettes.items():
        if a.id is not None and identifier != a.id:
            continue
        if a.size and len(cs) != a.size:
            continue
        if a.search and not any(a.search.casefold() in c['name'].casefold() for c in cs):
            continue
        if max(contrast(x['hex'], y['hex']) for x, y in itertools.combinations(cs, 2)) < a.min_contrast:
            continue
        selected.append((identifier, cs))
    if a.limit is not None:
        selected = selected[:a.limit]
    elif not a.gallery:
        selected = selected[:12]
    if a.gallery:
        print(json.dumps(gallery(selected, a.gallery)))
    else:
        print(json.dumps([report(i, cs) for i, cs in selected], indent=2))


if __name__ == '__main__':
    main()
