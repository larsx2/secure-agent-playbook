"""Dependency closure and install-layout invariants (no network or target execution)."""
import tempfile
import unittest
from unittest import mock
import zipfile
from pathlib import Path

from package_skills import NO_SYMLINKS, dependency_files, package_skill, check_links, skills, symlink_stub


class PackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # One actionable error instead of a failure per skill on symlink-less checkouts.
        if symlink_stub():
            raise AssertionError(NO_SYMLINKS)

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
        self.assertIn(Path('plays/code-review-security.md'), code)
        self.assertIn(Path('templates/finding.md'), code)
        self.assertIn(Path('data/asvs/V6.2.md'), code)
        web = dependency_files(by_name['web-security-review'])
        self.assertIn(Path('plays/sca-audit.md'), web)
        full_loop = dependency_files(by_name['securability-engineering'])
        self.assertIn(Path('plays/securable-generation.md'), full_loop)
        self.assertIn(Path('data/fiasse/S2.1.md'), full_loop)
        mobile = dependency_files(by_name['mobile-code-review'])
        self.assertTrue(any(path.parts[:2] == ('data', 'mastg') for path in mobile))

    def test_peer_skill_references_resolve_to_canonical_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            plugin = Path(directory)
            skill = plugin / 'skills' / 'example'
            peer = plugin / 'skills' / 'peer'
            skill.mkdir(parents=True)
            peer.mkdir(parents=True)
            (skill / 'SKILL.md').write_text('Follow `references/peer.md`.')
            (peer / 'SKILL.md').write_text('Peer procedure.')
            self.assertEqual(dependency_files(skill)[Path('references/peer.md')], peer / 'SKILL.md')

    def test_unbundled_dataset_cited_by_a_play_is_skipped_but_not_by_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            plugin = Path(directory)
            skill = plugin / 'skills' / 'example'
            skill.mkdir(parents=True)
            (plugin / 'templates').mkdir()
            (plugin / 'templates/finding.md').write_text('See `data/opencre/README.md`.')
            (skill / 'SKILL.md').write_text('Use `templates/finding.md`.')
            self.assertEqual(set(dependency_files(skill)), {Path('SKILL.md'), Path('templates/finding.md')})
            (skill / 'SKILL.md').write_text('Use `data/opencre/README.md`.')
            with self.assertRaisesRegex(ValueError, 'Missing dependency'):
                dependency_files(skill)

    def test_symlink_text_stubs_get_one_actionable_error(self):
        with tempfile.TemporaryDirectory() as directory:
            plugin = Path(directory)
            skill = plugin / 'skills' / 'example'
            (skill / 'templates').mkdir(parents=True)
            (plugin / 'templates').mkdir()
            (plugin / 'templates/finding.md').write_text('Finding format.')
            (skill / 'SKILL.md').write_text('Use `templates/finding.md`.')
            (skill / 'templates/finding.md').write_text('../../../templates/finding.md')
            with mock.patch('package_skills.skills', return_value=[skill]):
                self.assertEqual(symlink_stub(), skill / 'templates/finding.md')
                with self.assertRaisesRegex(ValueError, 'core.symlinks'):
                    check_links(skill, dependency_files(skill))

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
