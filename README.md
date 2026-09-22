# 🔥 fire-your-seo-agency

[한국어](./README.ko.md) · **English**

![fire-your-seo-agency](./assets/social-preview.png)

> **Paying $400–$2,500/month for an SEO or "AI visibility" agency? Fire them. Your AI agent can do the work.**

A wave of services now charges monthly retainers for "AI-era search optimization",
"guaranteed ChatGPT citations", and "LLM visibility". Most of what they actually do is
**public standards and repeatable checklists**. When a human does it, it's a retainer.
When your agent does it, it's a skill.

This repository is a [Claude Code](https://claude.com/claude-code) skill. Install it and
your agent audits your site, fixes what's broken, and measures the results.

## Built on real numbers

This is not theory. The same playbook, applied to [Chickenstock](https://www.chickstockfi.com) — a solo-built Korean stock research service:

- **1.54M search impressions in 30 days** (+85,578% MoM), 7.4K clicks
- Pages **cited paragraph-by-paragraph by Naver's AI Briefing** (Korea's answer engine)
- Zero ad spend — all inbound from search and AI citations

The journey is documented publicly on [Threads @kindainvestor](https://www.threads.com/@kindainvestor).

## The five lanes

"Search optimization" means different things to different engines. This skill treats them
as five distinct lanes:

| Lane | Target | The question it answers |
|---|---|---|
| **SEO** | Google & Bing crawlers | Can crawlers read and index my content at all? |
| **AEO** (Answer Engine) | Google AI Overviews, Bing Copilot | Does the AI answer box above the results cite me? |
| **GEO** (Generative Engine) | ChatGPT, Perplexity, Claude | When generative AI browses, am I the primary source? |
| **LLMO** (LLM Optimization) | The model's own knowledge | Does the model know my brand — and know it correctly? |
| **NEO** (Naver Engine) | Naver search & AI Briefing | Half of the Korean market — does Naver cite me? |

**NEO is what makes this skill different.** Global AEO guides ignore Naver entirely,
but if you serve the Korean market, half your traffic lives there.

**Plus a content engine.** Most of a retainer pays for "N posts a month". This skill
replaces that with a pipeline: a question backlog pulled from your own search data, a
frontmatter content model that generates the JSON-LD, a publish gate every post must pass,
and a refresh/merge policy so posts don't rot. Output is measured as "posts that get seen
and cited", not "posts published".

## Install

As a plugin (recommended — one command, easy updates):

```
/plugin marketplace add leopard627/fire-your-seo-agency
/plugin install fire-your-seo-agency@fire-your-seo-agency
```

Or via git clone:

```bash
# As a project skill (this project only)
git clone https://github.com/leopard627/fire-your-seo-agency.git .claude/skills/fire-your-seo-agency

# Or as a personal skill (every project)
git clone https://github.com/leopard627/fire-your-seo-agency.git ~/.claude/skills/fire-your-seo-agency
```

Then in Claude Code:

```
/fire-your-seo-agency audit my site
```

Your agent starts with a crawler-eye audit and returns a scorecard like this before
touching anything:

| Lane | Status | Evidence |
|---|---|---|
| SEO | ⚠️ | Body is SSR'd, but 214 detail pages missing from sitemap |
| AEO | ❌ | No direct-answer first paragraphs; FAQ structured data: 0 |
| GEO | ❌ | No llms.txt; GPTBot/PerplexityBot policy undecided in robots.txt |
| LLMO | ⚠️ | Brand name spelled 3 different ways across surfaces |
| NEO | ❌ | Not registered in Naver Search Advisor |

…then proposes priorities, implements them, and schedules the re-measurement.

## What it does

1. **Audit** — reads your site the way a crawler does (no JavaScript) and scores all five lanes
2. **Technical base** — fixes SSR exposure, sitemaps, meta, structured data
3. **Intent landing pages** — designs pages on the "one question = one page" principle
4. **Machine readability** — llms.txt, JSON-LD, citation-ready paragraph structure
5. **Naver** — from Search Advisor registration to AI Briefing citation requirements
6. **Content engine** — sub-blog setup, question backlog, publish gate, refresh & merge policy
7. **Measurement loop** — schedules a re-measurement and proves the change with numbers

### Focused audits

Ask for only the area you need, for example:

```text
/fire-your-seo-agency audit this site's Core Web Vitals, mobile usability and HTTPS
/fire-your-seo-agency review these pages for content quality and E-E-A-T
/fire-your-seo-agency compare these competitors using the attached keyword and backlink exports
/fire-your-seo-agency audit this local business and its Google Business Profile
```

- **Technical:** compare raw and rendered content; inspect mobile usability and HTTPS;
  separate real-user Core Web Vitals from lab measurements.
- **Content quality:** use Google QRG and people-first guidance to review evidence of
  experience, expertise, reputation and trust; identify thin or outdated content.
- **Competitors and backlinks:** compare keyword coverage and supplied link data with
  their market, time period and sampling limits recorded.
- **Local:** review eligible businesses, profile accuracy and website consistency.

These are instructions, not bundled crawlers, paid datasets or account connections.
Without tool/account access or exports, the agent reviews public evidence and marks the
rest **unverified/unmeasured**, rather than inventing metrics. Quality reviews are not
official Google scores, and neither rankings nor AI citations are guaranteed.
The examples use the existing skill invocation; this does not add `/seo` subcommands.

## What it refuses to do

- ❌ Buying backlinks, engagement pods, content spam — **we don't fight the search engine**
- ❌ "Guaranteed rankings" promises — no claims without measurement
- ❌ Keyword stuffing, hidden text, cloaking — nothing that gets your domain killed

The whole philosophy fits in one line: **AI doesn't cite good writing. AI cites accurate data.**
Become the primary source for a number, and the citations follow.

## Structure

```
SKILL.md              ← agent operating procedure (audit → implement → measure)
references/
  seo.md              ← technical SEO checklist + real-world traps
  content-quality.md  ← QRG-informed content quality and E-E-A-T review
  competitive-links.md ← competitor keyword gaps and backlink evidence
  local-seo.md        ← local businesses and Google Business Profile
  aeo.md              ← answer engine optimization (Bing WMT · AI Overviews · Copilot · E-E-A-T)
  geo.md              ← generative engine optimization (AI crawler policy · llms.txt · primary source)
  llmo.md             ← model-knowledge optimization (brand entity)
  neo-naver.md        ← Naver (Search Advisor · AI Briefing · blog two-track)
  content.md          ← content ops (sub-blog · content model · backlog · publish gate · refresh)
  measure.md          ← the measurement loop (fixing it is not the finish line)
  en/                 ← English mirrors of all reference docs (for human readers)
.claude-plugin/       ← plugin & marketplace manifests (/plugin install support)
```

> The Korean documents under `references/` are canonical (the agent reads those);
> `references/en/` mirrors them in English for human readers.

## License

MIT — use it freely, and keep the retainer money.
