"""Tests that the review assessment contract stays shared — run via: python scripts/test_assessment_contract.py -v"""
import unittest
from pathlib import Path

PLUGINS = Path(__file__).resolve().parent.parent / "plugins"
CONTRACT = "plays/assessment-contract.md"
# Skills that write code or requirements rather than review existing ones.
NOT_REVIEW_SKILLS = {"securability-engineering", "prd-securability-enhancement"}


class TestAssessmentContract(unittest.TestCase):
    def test_plugin_copies_are_identical(self):
        code = (PLUGINS / "code-security-skills" / CONTRACT).read_text()
        ai = (PLUGINS / "ai-security-skills" / CONTRACT).read_text()
        self.assertEqual(code, ai)

    def test_review_skills_and_agents_reference_contract(self):
        files = [
            skill for skill in PLUGINS.glob("*/skills/*/SKILL.md")
            if skill.parent.name not in NOT_REVIEW_SKILLS
        ] + list(PLUGINS.glob("*/agents/*.md"))
        self.assertTrue(files)
        missing = [str(f.relative_to(PLUGINS)) for f in files if CONTRACT not in f.read_text()]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
