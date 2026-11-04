"""Real CLI smoke test; no browser needed for --help."""
from pathlib import Path
import subprocess
import sys
import unittest
import importlib.util
import os
import struct
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / 'skills/html-poster-design/scripts/render.py'

class RendererTests(unittest.TestCase):
    def test_cli_explains_input_and_output(self):
        result = subprocess.run([sys.executable, str(RENDERER), '--help'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--output', result.stdout)
        self.assertIn('--browser', result.stdout)

    def test_invalid_input_fails_with_actionable_message(self):
        result = subprocess.run([sys.executable, str(RENDERER), 'missing.html', '--output', 'out.png'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Input HTML does not exist', result.stderr)

    @unittest.skipUnless(importlib.util.find_spec('playwright'), 'Install requirements-render.txt for browser integration tests')
    def test_renders_local_html_to_exact_png_dimensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'poster.html'
            output = Path(tmp) / 'poster.png'
            source.write_text('<!doctype html><meta charset="utf-8"><style>body{margin:0}.poster{width:200px;height:300px;background:#a7d4e4}</style><main class="poster">Hello / שלום / Привет</main>', encoding='utf-8')
            result = subprocess.run([sys.executable, str(RENDERER), str(source), '--output', str(output), '--width', '200', '--height', '300', '--scale', '2', '--selector', '.poster', '--browser', os.environ.get('RENDER_BROWSER', 'chromium')], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.exists(), 'Renderer did not create a PNG')
            raw = output.read_bytes()
            self.assertEqual(raw[:8], b'\x89PNG\r\n\x1a\n')
            self.assertEqual(struct.unpack('>II', raw[16:24]), (400, 600))

    @unittest.skipUnless(importlib.util.find_spec('playwright'), 'Install requirements-render.txt for browser integration tests')
    def test_renderer_rejects_broken_images_and_page_errors(self):
        cases = [
            ('<img src="missing.png">', 'Broken images'),
            ('<script>throw new Error("intentional test error")</script>', 'Page JavaScript errors'),
            ('<img src="https://example.invalid/test.png">', 'Remote asset requests blocked'),
        ]
        for content, expected in cases:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / 'bad.html'
                output = Path(tmp) / 'bad.png'
                source.write_text('<!doctype html>' + content, encoding='utf-8')
                result = subprocess.run([sys.executable, str(RENDERER), str(source), '--output', str(output), '--browser', os.environ.get('RENDER_BROWSER', 'chromium')], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr)
                self.assertFalse(output.exists())

if __name__ == '__main__':
    unittest.main()
