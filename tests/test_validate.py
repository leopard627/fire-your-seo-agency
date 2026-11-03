"""Tests for tools/validate.py.

Each case writes a small repository into a temp directory, breaks one thing and
expects exactly that check to fail.
"""

from __future__ import annotations

import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import validate  # noqa: E402

GEO = """# GEO

| 용도 | 대표 User-agent | 비고 |
|---|---|---|
| 학습 | GPTBot, Google-Extended | x |
| 검색 | OAI-SearchBot | x |

확인일: 2026-11-01

## 1. 첫 절

본문 [예시](https://example.com/a)
"""

GEO_EN = GEO.replace("용도", "Purpose").replace("확인일", "Last verified").replace("첫 절", "First")

MEASURE = """# 측정

```bash
AI_BOTS='GPTBot|OAI-SearchBot'\ngrep -ciE "$AI_BOTS" access.log
```
"""

BASE = {
    "SKILL.md": "---\nname: demo-skill\ndescription: Demo skill.\n---\n\n# Demo\n\nSee `references/geo.md`.\n",
    ".claude-plugin/plugin.json": '{"name": "demo-skill", "version": "1.0.0"}',
    ".claude-plugin/marketplace.json": '{"name": "demo-skill", "plugins": [{"name": "demo-skill", "version": "1.0.0"}]}',
    "CHANGELOG.md": "# Changelog\n\n## 1.0.0 — 2026-01-01\n\n- first\n",
    "README.md": "# Demo\n\n[GEO](references/geo.md#1-첫-절) · [repo](https://github.com/leopard627/fire-your-seo-agency)\n",
    "references/geo.md": GEO,
    "references/en/geo.md": GEO_EN,
    "references/measure.md": MEASURE,
    "references/en/measure.md": MEASURE.replace("측정", "Measure"),
    "tools/allowed-domains.txt": "# comment\nexample.com\ngithub.com/leopard627/fire-your-seo-agency\n",
}


class CheckTestCase(unittest.TestCase):
    def run_checks(self, changes=None, **kwargs) -> dict:
        files = dict(BASE, **(changes or {}))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel, body in files.items():
                if body is None:
                    continue
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text(body, encoding="utf-8")
            return validate.validate(root, **kwargs)

    def assert_only_failure(self, check: str, changes=None, contains: str = "", **kwargs) -> None:
        results = self.run_checks(changes, **kwargs)
        failing = {name for name, problems in results.items() if problems}
        self.assertEqual(failing, {check}, results)
        if contains:
            self.assertIn(contains, " ".join(results[check]))


class TestFixture(CheckTestCase):
    def test_fixture_passes(self) -> None:
        self.assertFalse(any(self.run_checks().values()))


class TestRelease(CheckTestCase):
    def test_changelog_behind_manifest(self) -> None:
        self.assert_only_failure("release", {"CHANGELOG.md": "## 0.9.0\n"}, "versions disagree")

    def test_marketplace_version_drift(self) -> None:
        market = BASE[".claude-plugin/marketplace.json"].replace("1.0.0", "1.0.1")
        self.assert_only_failure("release", {".claude-plugin/marketplace.json": market}, "versions disagree")

    def test_plugin_renamed(self) -> None:
        plugin = BASE[".claude-plugin/plugin.json"].replace('"demo-skill"', '"other"')
        self.assert_only_failure("release", {".claude-plugin/plugin.json": plugin}, "names disagree")

    def test_broken_manifest(self) -> None:
        self.assert_only_failure("release", {".claude-plugin/plugin.json": "{"}, "cannot read")


class TestSkill(CheckTestCase):
    def test_name_not_kebab_case(self) -> None:
        skill = BASE["SKILL.md"].replace("demo-skill", "Demo_Skill")
        results = self.run_checks({"SKILL.md": skill})
        self.assertTrue(results["skill"])

    def test_description_too_long(self) -> None:
        skill = BASE["SKILL.md"].replace("Demo skill.", "x" * 1025)
        self.assert_only_failure("skill", {"SKILL.md": skill}, "1-1024")


class TestLinks(CheckTestCase):
    def test_missing_file(self) -> None:
        self.assert_only_failure("links", {"README.md": "[x](references/nope.md)\n"}, "does not exist")

    def test_missing_korean_anchor(self) -> None:
        self.assert_only_failure("links", {"README.md": "[x](references/geo.md#9-없는-절)\n"}, "no heading")

    def test_missing_path_mention(self) -> None:
        skill = BASE["SKILL.md"].replace("references/geo.md", "references/gone.md")
        self.assert_only_failure("links", {"SKILL.md": skill}, "references/gone.md")


class TestDomains(CheckTestCase):
    def readme(self, text: str) -> dict:
        return {"README.md": text + "\n"}

    def test_unlisted_url(self) -> None:
        self.assert_only_failure("domains", self.readme("[사례](https://some-agency.co.kr/case)"), "some-agency.co.kr")

    def test_bare_domain_before_korean_particle(self) -> None:
        self.assert_only_failure("domains", self.readme("자세한 내용은 blog.naver.com/promo에서"), "blog.naver.com/promo")

    def test_url_inside_code_block(self) -> None:
        self.assert_only_failure("domains", self.readme("```\ncurl https://tracker.example.net\n```"))

    def test_lookalike_hosts(self) -> None:
        for host in ("notexample.com", "example.com.evil.io"):
            with self.subTest(host=host):
                self.assert_only_failure("domains", self.readme("https://%s/x" % host))

    def test_path_prefix_entry(self) -> None:
        self.assert_only_failure("domains", self.readme("https://github.com/someone/seo-tool"), "github.com/someone")
        self.assertFalse(self.run_checks(self.readme("https://github.com/leopard627/fire-your-seo-agency/fork"))["domains"])
        self.assert_only_failure("domains", self.readme("https://github.com/leopard627/fire-your-seo-agency-pro"))

    def test_subdomain_of_listed_host(self) -> None:
        self.assertFalse(self.run_checks(self.readme("https://blog.example.com/post"))["domains"])

    def test_missing_allowlist(self) -> None:
        self.assert_only_failure("domains", {"tools/allowed-domains.txt": None}, "missing or empty")


class TestMirror(CheckTestCase):
    def test_missing_english_mirror(self) -> None:
        self.assert_only_failure("mirror", {"references/seo.md": "# SEO\n"}, "no English mirror")

    def test_section_dropped_in_translation(self) -> None:
        self.assert_only_failure("mirror", {"references/en/geo.md": GEO_EN.replace("## 1. First", "First")})

    def test_link_only_in_one_language(self) -> None:
        geo = GEO + "\n[ref](https://schema.org/Thing)\n"
        files = {"references/geo.md": geo, "tools/allowed-domains.txt": BASE["tools/allowed-domains.txt"] + "schema.org\n"}
        self.assert_only_failure("mirror", files, "only ko: ['schema.org']")


class TestCrawlers(CheckTestCase):
    def test_grep_misses_a_table_entry(self) -> None:
        measure = MEASURE.replace("GPTBot|", "")
        self.assert_only_failure("crawlers", {"references/measure.md": measure}, "missing ['GPTBot']")

    def test_robots_only_token_is_not_expected_in_logs(self) -> None:
        measure = MEASURE.replace("GPTBot|", "GPTBot|Google-Extended|")
        self.assert_only_failure("crawlers", {"references/en/measure.md": measure}, "extra ['Google-Extended']")


class TestFreshness(CheckTestCase):
    def test_off_by_default(self) -> None:
        self.assertNotIn("freshness", self.run_checks())

    def test_recent_date_passes(self) -> None:
        results = self.run_checks(max_age=30, today=dt.date(2026, 11, 20))
        self.assertEqual(results["freshness"], [])

    def test_stale_date_fails(self) -> None:
        self.assert_only_failure("freshness", max_age=30, today=dt.date(2027, 1, 1), contains="61 days ago")

    def test_missing_date_fails(self) -> None:
        geo = GEO.replace("확인일: 2026-11-01", "")
        self.assert_only_failure("freshness", {"references/geo.md": geo}, "no '확인일", max_age=30)


class TestRealRepository(unittest.TestCase):
    def test_repository_passes(self) -> None:
        results = validate.validate(ROOT)
        self.assertEqual({k: v for k, v in results.items() if v}, {})


if __name__ == "__main__":
    unittest.main()
