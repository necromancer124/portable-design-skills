"""Source-data and portable package regression checks (no network)."""
from pathlib import Path
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
PALETTES = ROOT / 'skills/sanzo-wada-design/scripts/palettes.py'

class PackageTests(unittest.TestCase):
    def test_skill_frontmatter_uses_open_standard_fields(self):
        skills = list((ROOT / 'skills').glob('*/SKILL.md'))
        self.assertEqual(len(skills), 3)
        for path in skills:
            raw = path.read_text(encoding='utf-8')
            self.assertTrue(raw.startswith('---\n'), str(path))
            parts = raw.split('---', 2)
            fm = yaml.safe_load(parts[1])
            self.assertEqual(fm['name'], path.parent.name)
            self.assertRegex(fm['name'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
            self.assertLessEqual(len(fm['name']), 64)
            self.assertTrue(0 < len(fm['description']) <= 1024)
            self.assertTrue(parts[2].strip())
            self.assertTrue(all(isinstance(k, str) and isinstance(v, str) for k, v in fm.get('metadata', {}).items()))
            self.assertFalse(set(fm) - {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'})

    def test_skill_local_backtick_file_references_exist(self):
        for path in (ROOT / 'skills').glob('*/SKILL.md'):
            for ref in re.findall(r'`((?:\.\./|references/|assets/|scripts/)[^`]+\.(?:md|json|py|html))`', path.read_text(encoding='utf-8')):
                self.assertTrue((path.parent / ref).is_file(), f'{path}: {ref}')

    def test_no_personal_assets_or_machine_paths(self):
        forbidden = ['C:\\Users\\', 'C:/Users/', '/c/Users/', 'composer-images', 'gho_' + 'A'*10]
        for path in ROOT.rglob('*'):
            if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts or 'output' in path.parts:
                continue
            if path == Path(__file__):
                continue
            if path.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp'):
                self.assertTrue('docs' in path.parts, f'Unexpected image: {path}')
                continue
            text = path.read_text(encoding='utf-8')
            for token in forbidden:
                self.assertNotIn(token, text, str(path))
            self.assertNotRegex(text, r'gh[pousr]_[A-Za-z0-9]{30,}')

    def test_dataset_integrity_and_known_anomaly(self):
        result = subprocess.run([sys.executable, str(PALETTES), '--self-test'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual((data['colors'], data['combinations']), (159, 348))
        self.assertEqual(data['self_test'], 'PASS')
        self.assertEqual(data['source_data_warnings'][0]['name'], 'Dull Violet Black')

    def test_palette_lookup_works_outside_repository(self):
        with tempfile.TemporaryDirectory() as cwd:
            result = subprocess.run([sys.executable, str(PALETTES), '--id', '75'], cwd=cwd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        palette = json.loads(result.stdout)[0]
        self.assertEqual(palette['combination'], 75)
        self.assertEqual([c['hex'] for c in palette['colors']], ['#a7d4e4', '#40456a'])

    def test_contrast_accepts_valid_hex_and_rejects_invalid_hex(self):
        result = subprocess.run([sys.executable, str(PALETTES), '--contrast', '#000000', '#ffffff'], capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout)['ratio'], 21)
        bad = subprocess.run([sys.executable, str(PALETTES), '--contrast', '#fff', 'red'], capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)

    def test_bad_combination_and_limit_are_rejected(self):
        for args in [('--id', '349'), ('--limit', '0')]:
            result = subprocess.run([sys.executable, str(PALETTES), *args], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)

    def test_filtered_gallery_is_written(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'gallery.html'
            result = subprocess.run([sys.executable, str(PALETTES), '--size', '2', '--limit', '3', '--gallery', str(target)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['combinations'], 3)
            self.assertEqual(target.read_text(encoding='utf-8').count('<article '), 3)

if __name__ == '__main__':
    unittest.main()
