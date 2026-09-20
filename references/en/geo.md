# GEO — Generative Engine Optimization (ChatGPT · Perplexity · Claude)

The lane that makes generative AI **cite you as the primary source** when it reads the web
through browsing/search tools. It overlaps with AEO, but generative engines ① run different
crawlers ② read llms.txt ③ reward the *original source* much more strongly.

## 1. llms.txt

`/llms.txt` at the site root — a site guide addressed to AI. Format is markdown:

```markdown
# Service Name

> One-sentence description (state what you are the primary source of)

## Key pages
- [Earnings calendar](https://example.com/earnings): earnings release schedule for listed companies
- [Stock data](https://example.com/stocks): filings-based financials & valuation

## Data policy
- Source: computed in-house from official filings, refreshed daily
- Cite as: example.com
```

- [ ] `/llms.txt` (the guide) + `/llms-full.txt` (full key data) if you can afford it
- [ ] Pack it with trust signals: data source, refresh cadence, what you originate
- [ ] Serving it from an app route is fine (it doesn't have to be a static file) —
      keep it always current

## 2. Decide your AI crawler policy

AI crawlers come in **three kinds by purpose**, and your robots.txt policy should be
written per purpose. No policy = leaving it to chance:

| Purpose | Representative User-agents | What blocking costs you |
|---|---|---|
| **Training** (model training data) | GPTBot, ClaudeBot, Google-Extended, CCBot, Applebot-Extended | future models knowing your brand (LLMO) |
| **Search indexing** (AI search's own index) | OAI-SearchBot, Claude-SearchBot, PerplexityBot | citations in ChatGPT/Claude/Perplexity search |
| **Live fetch** (page loads at question time) | ChatGPT-User, Perplexity-User, Claude-User | direct citations & traffic at answer time |

```
# If citations are the goal, Allow across the board is the default
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Perplexity-User
Allow: /
```

- ⚠️ **Google-Extended ≠ AI Overviews**: Google-Extended only governs Gemini training and
  grounding. AI Overviews and AI Mode draw from the regular Googlebot index, so this token
  neither blocks nor enables them — and blocking Googlebot kills Search itself. Don't mistake
  "block AI training" and "get cited by AI search" for the same switch.

If your content is an asset and you only want to block **training**, Disallow only the
first row — blocking search/fetch along with it kills citation traffic itself.
The roster changes — recheck each vendor's crawler docs quarterly.

- [ ] **Check your Bing index**: ChatGPT search relies on the Bing index on top of its own
      crawler. If you're not in Bing Webmaster Tools, start with section 0 of
      `references/aeo.md` (or `references/en/aeo.md`)

## 3. Becoming the primary source — the heart of GEO

Generative engines trace "where did this number originate." A page summarizing someone
else's data loses the citation to the original.

- [ ] Define which numbers only you compute or collect (in-house metrics, aggregations,
      observations)
- [ ] Name that number and always serve it from the same page (stable URL = citation address)
- [ ] Paragraph-level citability: when each paragraph carries
      [subject + number + as-of date + methodology], it gets cited as a unit — measured:
      both Naver AI Briefing and Perplexity clip at exactly this granularity

## 4. Verification

- Ask real questions in Perplexity and ChatGPT (search mode) and check whether your domain
  appears in the source list
- Not appearing? Check in order: llms.txt exists → crawlers allowed → that page is SSR →
  a competing original source exists
