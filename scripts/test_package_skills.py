"""Dependency closure and install-layout invariants (no network or target execution)."""
import tempfile
import unittest
import zipfile
from pathlib import Path

from package_skills import dependency_files, package_skill, check_links, skills


class PackagingTests(unittest.TestCase):
    def test_discoverable_skills_have_one_canonical_entrypoint(self):
        from package_skills import ROOT
        self.assertEqual(set(ROOT.glob('**/SKILL.md')), {
            skill / 'SKILL.md' for skill in skills()
        })

    def test_all_committed_install_layouts_match_dependency_closure(self):
        for skill in skills():
            with self.subTest(skill=skill.name):
                expected = dependency_files(skill)
                self.assertLessEqual(len(expected), 200)
                check_links(skill, expected)
                for relative, source in expected.items():
                    self.assertEqual((skill / relative).read_bytes(), source.read_bytes())

    def test_release_archives_match_direct_install_files(self):
        with tempfile.TemporaryDirectory() as directory:
            for skill in skills():
                with self.subTest(skill=skill.name):
                    expected = dependency_files(skill)
                    archive = package_skill(skill, Path(directory))
                    with zipfile.ZipFile(archive) as bundle:
                        self.assertEqual(set(bundle.namelist()), {
                            f'{skill.name}/{path}' for path in expected
                        })
                        for relative, source in expected.items():
                            self.assertEqual(bundle.read(f'{skill.name}/{relative}'), source.read_bytes())

    def test_transitive_dependencies_are_included(self):
        by_name = {skill.name: skill for skill in skills()}
        code = dependency_files(by_name['code-review-security'])
        self.assertIn(Path('plays/sca-audit.md'), code)
        self.assertIn(Path('templates/report.md'), code)
        self.assertIn(Path('data/asvs/V6.2.md'), code)
        full_loop = dependency_files(by_name['securability-engineering'])
        self.assertIn(Path('references/prd-securability-enhancement.md'), full_loop)
        self.assertIn(Path('references/securability-engineering-review.md'), full_loop)
        threat = dependency_files(by_name['multi-agentic-threat-model'])
        self.assertIn(Path('plays/multi-agentic-threat-model.md'), threat)

    def test_missing_dependency_fails_instead_of_silently_shipping(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / 'skills' / 'example'
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').write_text('Read `plays/missing.md`.')
            with self.assertRaisesRegex(ValueError, 'Missing dependency'):
                dependency_files(skill)

    def test_cycles_terminate_and_nested_play_dependencies_are_followed(self):
        with tempfile.TemporaryDirectory() as directory:
            plugin = Path(directory)
            skill = plugin / 'skills' / 'example'
            skill.mkdir(parents=True)
            (plugin / 'plays').mkdir()
            (skill / 'SKILL.md').write_text('Read `plays/first.md`.')
            (plugin / 'plays/first.md').write_text('Read `plays/second.md`.')
            (plugin / 'plays/second.md').write_text('Read `plays/first.md`.')
            self.assertEqual(set(dependency_files(skill)), {
                Path('SKILL.md'), Path('plays/first.md'), Path('plays/second.md')
            })

    def test_missing_file_in_existing_dataset_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            plugin = Path(directory)
            skill = plugin / 'skills' / 'example'
            skill.mkdir(parents=True)
            (plugin / 'data/asvs').mkdir(parents=True)
            (plugin / 'data/asvs/V6.2.md').write_text('Password requirements')
            (skill / 'SKILL.md').write_text('Read `data/asvs/V99.1.md`.')
            with self.assertRaisesRegex(ValueError, 'Missing dependency'):
                dependency_files(skill)

    def test_external_urls_do_not_become_local_dependencies(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / 'skills' / 'example'
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').write_text(
                '[External](https://example.org/plays/external.md) '
                'https://example.org/data/external/reference.md'
            )
            self.assertEqual(set(dependency_files(skill)), {Path('SKILL.md')})


if __name__ == '__main__':
    unittest.main()
