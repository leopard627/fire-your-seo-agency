# Changelog

Notable changes per release. Versions match the plugin tags
(`fire-your-seo-agency--vX.Y.Z`); `.claude-plugin/plugin.json` and
`.claude-plugin/marketplace.json` must carry the same version, and
`tools/validate.py` fails the build when they drift apart.

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

