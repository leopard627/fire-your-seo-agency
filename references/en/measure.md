# The Measurement Loop — fixing it is not the finish line

This is the real difference between an agency and this skill. An agency sends a
"work completed" report; this skill checks **whether the numbers moved**. Optimization
without measurement is just a claim.

## 1. Baseline — record it BEFORE you fix anything

If you don't capture the before state, you can never prove the effect:

- Google Search Console: last 28 days of impressions, clicks, average position
  (by page group)
- Naver Search Advisor: content impressions/clicks, top queries list
- AI citations: actually ask 5–10 target questions in Perplexity, ChatGPT, and Naver
  AI Briefing, and record cited-or-not as O/X
- Index counts: `site:domain` result count + GSC indexed pages (check Bing with
  `site:` too)
- **AI crawler visits**: the trend of GPTBot, PerplexityBot, ClaudeBot, etc. in your
  server logs. Crawls come before citations — this is the leading indicator

```bash
# Count AI crawler visits in the access log (leading indicator)
AI_BOTS='GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|Claude-SearchBot|Claude-User|PerplexityBot|Perplexity-User|CCBot|Google-Agent'
grep -ciE "$AI_BOTS" access.log
# Status-code breakdown — 403/429 means your CDN/WAF is blocking them (field 9 in combined log format)
grep -iE "$AI_BOTS" access.log | awk '{print $9}' | sort | uniq -c
# No log access? Substitute your host's bot-traffic breakdown (Cloudflare/Vercel etc.)
```

## 2. The re-measurement date is part of the work

- Search reflects changes with lag: **re-measure 14 days after the change** by default,
  and exclude the most recent 2–3 days from comparisons (reporting delay)
- Don't leave re-measurement to "remembering" — put it on a schedule or set an agent
  reminder. If this skill did the work, stating the re-measurement date in the report
  is part of the definition of done

## 3. The stale data trap

> **Stale data passes every lower bound.**

Monitoring that only checks "the metric isn't zero" happily passes a value that's been
stuck for days. When you build measurement pipelines, watch **the date of the value,
not the value**: "if the last update is older than N days, don't display the metric"
is the safe default.

## 4. How to read the numbers

- **Impressions first, clicks later**: the first signal of structural improvement is
  rising impressions. Clicks (CTR) only move once title/description improvements follow.
  Impressions up but CTR flat = your next task is meta
- **Weekend dips are normal**: weekday-natured topics (business, finance) go quiet on
  weekends. That pattern is evidence of real demand, not a problem
- **The query list is your roadmap**: Search Advisor / GSC top queries are the list of
  questions people actually type. A top query with no dedicated landing page = the next
  page to build

## 5. Report format

```
[Baseline]   8/1–8/28: 12,400 impressions · 180 clicks · AI citations 0/8 questions
[Change]     8/29: 6 intent landing pages + llms.txt + FAQ LD
[Re-measure] scheduled 9/12
[Result]     31,000 impressions (+150%) · 610 clicks · AI citations 3/8  ← this line is "done"
```
