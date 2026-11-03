#!/usr/bin/env python3
"""Repository checks for fire-your-seo-agency.

Each check guards something that has drifted or been abused in this repo:

  release    SKILL.md, plugin.json, marketplace.json and CHANGELOG.md agree on the
             name and version, so /plugin install serves what the changelog says.
  skill      SKILL.md frontmatter stays loadable (kebab-case name, description limits).
  links      Relative links, heading anchors and `references/...` mentions resolve.
  mirror     Each references/en/*.md keeps the Korean original's structure and cites
             the same outbound hosts.
  domains    Every outbound URL or bare domain in the docs is on
             tools/allowed-domains.txt. Outside PRs have tried to slip commercial
             links in; a new domain has to be allowed on purpose, in plain sight.
  crawlers   The AI crawler table in geo.md and the AI_BOTS list in measure.md
             name the same user agents, in both languages.
  freshness  (only with --max-age DAYS) the crawler table was verified recently.

Standard library only:
    python3 tools/validate.py [--root DIR] [--max-age DAYS]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ALLOWLIST = "tools/allowed-domains.txt"
DOC_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".txt", ".html", ".svg"}
SKIP_DIRS = {".git", "tools", "tests", "node_modules", "__pycache__"}
MIRRORS = (("references", "references/en"),)
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

# robots.txt control tokens: they decide training use, but no crawler sends them
# as its User-agent, so they never show up in an access log.
ROBOTS_ONLY_TOKENS = {"Google-Extended", "Applebot-Extended"}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
NUMBERED_RE = re.compile(r"^#{2,3}\s+(\d+(?:-\d+)?)\.\s")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]*)>?(?:\s+\"[^\"]*\")?\s*\)")
MENTION_RE = re.compile(r"`((?:references|assets|tools|tests|\.claude-plugin|\.github)/[\w./-]+)`")
_URL_TAIL = r"[^\s)\]>\"'`*<|]*"
URL_RE = re.compile(r"https?://([^/\s)\]>\"'`*<|]+)(" + _URL_TAIL + ")", re.I)
BARE_DOMAIN_RE = re.compile(
    # ASCII-only boundaries: Korean particles attach directly ("example.com에서"), and
    # \w would count them as part of the word and hide the domain.
    r"(?<![A-Za-z0-9_@./:-])((?:[a-z0-9-]+\.)+(?:com|net|org|io|co|kr|ai|app|dev|me|so|xyz|info|biz"
    r"|blog|shop|site|page|link|ly|gg|tv))(?![A-Za-z0-9_-])(/" + _URL_TAIL + ")?",
    re.I,
)
VERIFIED_RE = re.compile(r"(?:확인일|Last verified):\s*(\d{4}-\d{2}-\d{2})")
LOG_GREP_RE = re.compile(r"AI_BOTS='([^']+)'")


class Repo:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.files = self._list_files()

    def _list_files(self) -> list:
        """Tracked plus untracked-but-not-ignored files, so a new file is checked before it is committed."""
        try:
            out = subprocess.run(
                ["git", "-C", str(self.root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                capture_output=True, check=True,
            ).stdout.decode()
            paths = [self.root / p for p in out.split("\0") if p]
        except (OSError, subprocess.CalledProcessError):
            paths = list(self.root.rglob("*"))
        return sorted(p for p in paths if p.is_file() and not SKIP_DIRS & set(p.relative_to(self.root).parts[:-1]))

    def docs(self) -> list:
        return [p for p in self.files if p.suffix.lower() in DOC_SUFFIXES]

    def rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def read(self, rel: str):
        try:
            return (self.root / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None


def prose_lines(text: str):
    """Yield (lineno, line) outside fenced code blocks."""
    fenced = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if not fenced:
            yield lineno, line


def slugify(heading: str) -> str:
    """Approximate the anchor GitHub generates for a heading."""
    heading = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", heading).replace("`", "").lower().strip()
    return re.sub(r"\s", "-", "".join(ch for ch in heading if ch.isalnum() or ch in " -_"))


def frontmatter(text: str) -> dict:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("no --- frontmatter block")
    values = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line[:1].isspace():
            values[key.strip()] = value.strip()
    return values


def check_release(repo: Repo) -> list:
    problems = []
    skill = repo.read("SKILL.md")
    try:
        name = frontmatter(skill or "").get("name")
    except ValueError:
        name = None
    try:
        plugin = json.loads(repo.read(".claude-plugin/plugin.json") or "")
        market = json.loads(repo.read(".claude-plugin/marketplace.json") or "")
        entry = market["plugins"][0]
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        return ["cannot read the plugin manifests: %r" % exc]
    names = {"SKILL.md": name, "plugin.json": plugin.get("name"),
             "marketplace.json": market.get("name"), "marketplace plugins[0]": entry.get("name")}
    if len(set(names.values())) != 1:
        problems.append("names disagree: %s" % names)
    changelog = re.findall(r"^## (\d+\.\d+\.\d+)", repo.read("CHANGELOG.md") or "", re.M)
    versions = {"plugin.json": plugin.get("version"), "marketplace plugins[0]": entry.get("version"),
                "CHANGELOG.md top entry": changelog[0] if changelog else None}
    if len(set(versions.values())) != 1:
        problems.append("versions disagree: %s" % versions)
    elif not SEMVER_RE.match(str(plugin.get("version"))):
        problems.append("version %r is not X.Y.Z" % plugin.get("version"))
    return problems


def check_skill(repo: Repo) -> list:
    text = repo.read("SKILL.md")
    if text is None:
        return ["SKILL.md is missing or not UTF-8"]
    try:
        values = frontmatter(text)
    except ValueError as exc:
        return ["SKILL.md: %s" % exc]
    name, description = values.get("name", ""), values.get("description", "")
    problems = []
    if not SKILL_NAME_RE.match(name) or len(name) > 64:
        problems.append("name %r must be kebab-case, at most 64 chars" % name)
    if not description or len(description) > 1024:
        problems.append("description must be 1-1024 chars on one line (is %d)" % len(description))
    return problems


def check_links(repo: Repo) -> list:
    problems = []
    for path in repo.docs():
        if path.suffix != ".md":
            continue
        text = repo.read(repo.rel(path)) or ""
        for lineno, line in prose_lines(text):
            where = "%s:%d" % (repo.rel(path), lineno)
            for target in LINK_RE.findall(line):
                if not target or re.match(r"^[a-z][a-z0-9+.-]*:|^//", target, re.I):
                    continue
                file_part, _, anchor = target.partition("#")
                dest = (path.parent / unquote(file_part)).resolve() if file_part else path
                if not dest.exists():
                    problems.append("%s: %s does not exist" % (where, target))
                elif anchor and dest.suffix == ".md":
                    headings = {slugify(m.group(2)) for _, l in prose_lines(dest.read_text(encoding="utf-8"))
                                if (m := HEADING_RE.match(l))}
                    if unquote(anchor) not in headings:
                        problems.append("%s: no heading for #%s" % (where, anchor))
            # CHANGELOG.md records files that past releases had; they may be gone now.
            for mention in MENTION_RE.findall(line) if path.name != "CHANGELOG.md" else ():
                if not (repo.root / mention).exists():
                    problems.append("%s: `%s` does not exist" % (where, mention))
    return problems


def outbound(text: str):
    """Yield (host, path) for every URL and bare domain in text."""
    for regex in (URL_RE, BARE_DOMAIN_RE):
        for host, path in regex.findall(text):
            host = host.lower().split(":")[0].rstrip(".")
            if regex is BARE_DOMAIN_RE and "." not in host:
                continue
            yield host, unquote(path or "")


def load_allowlist(repo: Repo) -> list:
    entries = []
    for line in (repo.read(ALLOWLIST) or "").splitlines():
        line = line.split("#", 1)[0].strip().lower()
        if line:
            host, _, path = line.partition("/")
            entries.append((host, "/" + path if path else ""))
    return entries


def allowed(host: str, path: str, entries: list) -> bool:
    for ahost, apath in entries:
        if host == ahost or host.endswith("." + ahost):
            if not apath or path.lower() == apath or path.lower().startswith(apath) and path[len(apath)] in "/?#.":
                return True
    return False


def check_domains(repo: Repo) -> list:
    entries = load_allowlist(repo)
    if not entries:
        return ["%s is missing or empty" % ALLOWLIST]
    problems = []
    for path in repo.docs():
        for lineno, line in enumerate((repo.read(repo.rel(path)) or "").splitlines(), start=1):
            for host, url_path in outbound(line):
                if not allowed(host, url_path, entries):
                    problems.append("%s:%d: %s%s is not on %s" % (repo.rel(path), lineno, host, url_path, ALLOWLIST))
    return problems


def structure(text: str) -> dict:
    stats = {"headings": [], "numbering": [], "table rows": 0, "checkboxes": 0,
             "code fences": text.count("\n```") // 2}
    for _, line in prose_lines(text):
        if m := HEADING_RE.match(line):
            stats["headings"].append(len(m.group(1)))
        if m := NUMBERED_RE.match(line):
            stats["numbering"].append(m.group(1))
        stats["table rows"] += line.startswith("|")
        stats["checkboxes"] += bool(re.match(r"^\s*[-*] \[[ xX]\]", line))
    return stats


def check_mirror(repo: Repo) -> list:
    problems = []
    for source, mirror in MIRRORS:
        ko = {p.name for p in (repo.root / source).glob("*.md")}
        en = {p.name for p in (repo.root / mirror).glob("*.md")}
        problems += ["%s/%s has no English mirror" % (source, n) for n in sorted(ko - en)]
        problems += ["%s/%s has no Korean original" % (mirror, n) for n in sorted(en - ko)]
        for name in sorted(ko & en):
            a, b = repo.read("%s/%s" % (source, name)) or "", repo.read("%s/%s" % (mirror, name)) or ""
            sa, sb = structure(a), structure(b)
            problems += ["%s: %s differ (ko %s, en %s)" % (name, k, sa[k], sb[k]) for k in sa if sa[k] != sb[k]]
            ha, hb = {h for h, _ in outbound(a)}, {h for h, _ in outbound(b)}
            if ha != hb:
                problems.append("%s: outbound hosts differ (only ko: %s, only en: %s)"
                                % (name, sorted(ha - hb), sorted(hb - ha)))
    return problems


def crawler_table(text: str) -> set:
    """User agents listed in the markdown table whose header has a 'User-agent' column."""
    tokens, column = set(), None
    for _, line in prose_lines(text):
        if not line.startswith("|"):
            column = None
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if column is None:
            column = next((i for i, c in enumerate(cells) if "User-agent" in c), -1)
        elif column >= 0 and not set(cells[column]) <= set("-: "):
            tokens |= {t.strip() for t in cells[column].split(",") if t.strip()}
    return tokens


def check_crawlers(repo: Repo) -> list:
    problems = []
    for base in ("references", "references/en"):
        table = crawler_table(repo.read(base + "/geo.md") or "")
        grep = LOG_GREP_RE.search(repo.read(base + "/measure.md") or "")
        if not table or not grep:
            problems.append("%s: crawler table in geo.md or log grep in measure.md not found" % base)
            continue
        logged = set(grep.group(1).split("|"))
        expected = table - ROBOTS_ONLY_TOKENS
        if logged != expected:
            problems.append("%s/measure.md grep vs geo.md table: missing %s, extra %s"
                            % (base, sorted(expected - logged), sorted(logged - expected)))
    return problems


def check_freshness(repo: Repo, max_age: int, today: dt.date) -> list:
    problems = []
    for rel in ("references/geo.md", "references/en/geo.md"):
        match = VERIFIED_RE.search(repo.read(rel) or "")
        if not match:
            problems.append("%s: no '확인일: YYYY-MM-DD' / 'Last verified: YYYY-MM-DD' line" % rel)
            continue
        age = (today - dt.date.fromisoformat(match.group(1))).days
        if age > max_age:
            problems.append("%s: crawler table last verified %s (%d days ago, limit %d) — recheck each vendor's crawler docs"
                            % (rel, match.group(1), age, max_age))
    return problems


def validate(root: Path, max_age=None, today=None) -> dict:
    repo = Repo(root)
    results = {
        "release": check_release(repo),
        "skill": check_skill(repo),
        "links": check_links(repo),
        "mirror": check_mirror(repo),
        "domains": check_domains(repo),
        "crawlers": check_crawlers(repo),
    }
    if max_age is not None:
        results["freshness"] = check_freshness(repo, max_age, today or dt.date.today())
    return results


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--max-age", type=int, metavar="DAYS", help="also fail when the crawler table is older than DAYS")
    args = parser.parse_args(argv)
    results = validate(args.root.resolve(), args.max_age)
    for check, problems in results.items():
        print("%-4s %s" % ("ok" if not problems else "FAIL", check))
        for problem in problems:
            print("     - " + problem)
    return 1 if any(results.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
