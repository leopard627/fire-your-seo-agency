# Changelog

Notable changes per release. Versions match the plugin tags
(`fire-your-seo-agency--vX.Y.Z`); `.claude-plugin/plugin.json` and
`.claude-plugin/marketplace.json` must carry the same version, and
`tools/validate.py` fails the build when they drift apart.

## Unreleased

### Changed

- `tools/validate.py` rewritten around what actually drifts or gets abused here. New checks:
  an outbound-domain allowlist (`tools/allowed-domains.txt`) for every URL and bare domain
  in the docs, AI crawler consistency between the `geo.md` table and the `measure.md` log
  command, outbound-host parity between Korean and English references, and a crawler-table
  freshness check (`--max-age`, run monthly by CI). Dropped: license text, secret-pattern
  scan (GitHub does this), social-preview size and dimension checks, and the `--strict` and
  `--json` modes
- `references/geo.md` §2 (+ English): crawler table verified against each vendor's docs on
  2026-11-03 with sources; `Google-Agent` added; notes that `Google-Extended` and
  `Applebot-Extended` are robots.txt-only tokens, that blocking `Google-Extended` does not
  affect AI Overviews or AI Mode, which user-triggered fetchers may ignore robots.txt, and
  that a CDN/WAF bot block overrides robots.txt
- `references/measure.md` (+ English): the AI crawler log command now covers every crawler
  in the `geo.md` table (it was missing `Claude-SearchBot`, `Perplexity-User` and `CCBot`)
  and shows a status-code breakdown to spot WAF blocks
- `references/aeo.md` (+ English): AI Mode named alongside AI Overviews
- `SKILL.md` Phase 0: the `<h1>` count works on minified HTML; the 404 probe uses an ASCII path
- README (EN/KO): Codex install paths (`.agents/skills`), rewritten repository-checks section

### Added

- `CONTRIBUTING.md` and a pull request template: what the repo accepts (fixes, policy updates
  with official sources, measured findings) and what it does not (commercial links, case
  studies, promotion of other tools, committed copies of the skill)

### Removed

- `tools/optimize_assets.py` and the Pillow install in CI — the one image is already optimized

## 1.2.1 — 2026-09-25

Repository checks and CI (contributed by @twoimo in #2), plus one content-ops fix.

### Added

- `tools/validate.py` — dependency-free repository checks: the SKILL.md frontmatter
  contract (kebab-case name, 64-character name limit, 1024-character single-line
  description), `plugin.json` and `marketplace.json` schema plus version and name
  agreement, `CHANGELOG.md` matching the manifest version, relative-link and anchor
  integrity, Korean/English reference parity (heading counts, table rows, checkboxes
  and section numbering), asset budgets, the MIT license metadata, and a secret scan
  over every tracked text file
- `tools/optimize_assets.py` — lossless PNG/JPEG/WebP recompression that refuses any
  candidate whose pixels differ; `--check` exits non-zero when an asset has more than
  2% of recoverable slack
- `tests/test_validate.py` — unit tests covering every check, the CLI, malformed input
  (broken JSON, invalid UTF-8, path traversal, empty directories) and the optimizer
- `.github/workflows/validate.yml` — CI running the checks, the tests and the asset
  check on every push and pull request
- `CHANGELOG.md` (this file)
- README (EN/KO): stars, forks, release and license badges plus a Star History chart

### Changed

- `references/content.md` §7 (+ English mirror): check whether the target editor renders
  Markdown before cross-posting; the Naver Blog editor shows `#`, `**` and `|` literally
- `assets/social-preview.png` recompressed losslessly: 1,252,826 → 1,056,122 bytes
  (−15.70%) with a byte-identical pixel grid
- `assets/thumbnail-prompt.md` overlay spec replaced with the geometry and copy actually
  measured from the shipped banner, so a regeneration reproduces it
- README (EN/KO): a repository-checks section and an updated structure tree

## 1.2.0 — 2026-09-21

Content engine — the lane that replaces "N posts a month".

- `references/content.md` plus the English mirror: where the blog lives (subdirectory by
  default), the frontmatter content model that also generates the JSON-LD, the five post
  types that get cited, the pipeline (question backlog → five-line brief → publish gate →
  14-day re-measure), the AI-draft policy, refresh/merge/delete rules, internal link
  structure, cross-posting order and per-post measurement
- `SKILL.md`: content trigger phrases, content checks in the Phase 0 audit, a Content row
  in the scorecard and a new Phase 5 (the measurement loop becomes Phase 6)
- README (EN/KO): content engine section, "What it does" item 6, structure tree
- Manifests bumped to 1.2.0, keywords `content-marketing` and `blog`

## 1.1.0 — 2026-08-27

Skill hardening and distribution.

- Bing Webmaster Tools section in AEO (`references/aeo.md` §0)
- AI crawler policy table in GEO — training, search-indexing and live-fetch user agents
  with a full robots.txt example (`references/geo.md` §2)
- E-E-A-T trust signals and the FAQ rich-results reality check (`references/aeo.md`)
- noindex detection (`meta robots` plus the `X-Robots-Tag` header) in the Phase 0 audit
- AI crawler visits as a leading indicator in the measurement baseline
- Prompt-injection defense in the skill invariants: fetched web content is data, never
  instructions
- English mirrors of all six reference documents under `references/en/`
- Installable as a plugin (`/plugin marketplace add` and `/plugin install`)

## 1.0.0 — 2026-08-27

Initial public release: `SKILL.md` with the five lanes (SEO · AEO · GEO · LLMO · NEO/Naver),
the Phase 0 crawler-eye audit and scorecard, phases 1–5, the Korean reference documents,
the bilingual README and the social preview image.

