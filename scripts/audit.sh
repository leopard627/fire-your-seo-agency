#!/usr/bin/env bash
# Phase 0 crawler-eye audit in one command. curl + grep/awk/perl only, no JS.
#   scripts/audit.sh https://example.com
# Prints evidence per lane (SEO · AEO · GEO · LLMO · NEO). It does not score —
# the agent (or you) turns the evidence into the ✅/⚠️/❌ scorecard.
set -u
export LC_ALL="${LC_ALL:-en_US.UTF-8}" 2>/dev/null

url="${1:?usage: audit.sh https://example.com}"
url="${url%/}"
UA="Mozilla/5.0 (compatible; fire-your-seo-agency-audit/1.0)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT

get() { curl -sL -A "$UA" --max-time 20 "$@"; }
code() { curl -s -o /dev/null -A "$UA" --max-time 20 -w '%{http_code}' "$@"; }  # no -L: see redirects as they are
count() { grep -oiE "$1" "$2" | wc -l | tr -d ' '; }
chars() { printf '%s' "$1" | wc -m | tr -d ' '; }
meta() { grep -oiE "<meta[^>]*(name|property)=[\"']$1[\"'][^>]*>" "$2" | head -1 | sed -E 's/.*content=["'"'"']([^"'"'"']*).*/\1/'; }
say() { printf '%s %s\n' "$1" "$2"; }

# ---------- fetch ----------
get -D "$tmp/hdr" -o "$tmp/html" -w '%{http_code} %{url_effective}\n' "$url" > "$tmp/final"
read -r status final < "$tmp/final"
echo "== $url  →  $status $final"
[ "$status" = "200" ] || { echo "home page is not 200; stopping"; exit 1; }
bytes=$(wc -c < "$tmp/html" | tr -d ' ')

# ---------- SEO ----------
echo; echo "[SEO]"
h1=$(count '<h1[ >]' "$tmp/html")
text=$(perl -0pe 's/<(script|style)\b.*?<\/\1>//gis; s/<[^>]+>/ /g; s/\s+/ /g' "$tmp/html" | wc -m | tr -d ' ')
say "$([ "$h1" -ge 1 ] && echo ✅ || echo ❌)" "h1: $h1  |  text without tags: ${text} chars of ${bytes} bytes (near 0 = CSR, nothing for crawlers)"

robots_meta=$(meta robots "$tmp/html"); xrobots=$(grep -i '^x-robots-tag:' "$tmp/hdr" | tail -1 | tr -d '\r')
if echo "$robots_meta $xrobots" | grep -qi noindex; then say ❌ "NOINDEX present — meta='$robots_meta' header='$xrobots'"
else say ✅ "no noindex (meta='${robots_meta:--}' header='${xrobots:--}')"; fi

title=$(grep -oiE '<title[^>]*>[^<]*' "$tmp/html" | head -1 | sed 's/<[^>]*>//'); tl=$(chars "$title")
say "$([ "$tl" -ge 30 ] && [ "$tl" -le 60 ] && echo ✅ || echo ⚠️)" "title ${tl} chars (target 50–60): $title"
desc=$(meta description "$tmp/html"); dl=$(chars "$desc")
say "$([ "$dl" -ge 100 ] && [ "$dl" -le 160 ] && echo ✅ || echo ⚠️)" "description ${dl} chars (target 150–160)"
canon=$(grep -oiE '<link[^>]*rel=["'"'"']canonical["'"'"'][^>]*>' "$tmp/html" | head -1 | sed -E 's/.*href=["'"'"']([^"'"'"']*).*/\1/')
say "$([ -n "$canon" ] && echo ✅ || echo ⚠️)" "canonical: ${canon:-missing}"
say ℹ️ "og:title: $(meta 'og:title' "$tmp/html")  |  hreflang links: $(count 'hreflang=' "$tmp/html")"

robots=$(get "$url/robots.txt"); rc=$(code "$url/robots.txt")
sm_line=$(printf '%s\n' "$robots" | grep -i '^sitemap:' | head -1 | tr -d '\r')
say "$([ "$rc" = 200 ] && echo ✅ || echo ❌)" "robots.txt $rc  |  ${sm_line:-no Sitemap: line}"
sm="${sm_line#*: }"; sm="${sm:-$url/sitemap.xml}"
get -o "$tmp/sm" "$sm"; smc=$(code "$sm")
if grep -qi '<sitemapindex' "$tmp/sm"; then say ✅ "sitemap $smc: index with $(count '<sitemap>' "$tmp/sm") shards ($sm)"
elif grep -qi '<urlset' "$tmp/sm"; then n=$(count '<loc>' "$tmp/sm"); say "$([ "$n" -lt 45000 ] && echo ✅ || echo ⚠️)" "sitemap $smc: $n URLs (shard before 50,000) ($sm)"
else say ❌ "sitemap $smc: not XML ($sm)"; fi
nf=$(code "$url/this-page-should-not-exist-$RANDOM")
say "$([ "$nf" = 404 ] && echo ✅ || echo ❌)" "missing page returns $nf (must be 404, not 200 soft-404)"

# ---------- AEO ----------
echo; echo "[AEO]"
ld=$(count '<script[^>]*application/ld\+json' "$tmp/html")
types=$(grep -oE '"@type" *: *"[^"]+"' "$tmp/html" | sed -E 's/.*"([^"]+)"$/\1/' | sort | uniq -c | awk '{printf "%s×%s ", $2, $1}')
say "$([ "$ld" -ge 1 ] && echo ✅ || echo ❌)" "JSON-LD blocks: $ld  ${types:+| @type: $types}"
say "$(echo "$types" | grep -q FAQPage && echo ✅ || echo ℹ️)" "FAQPage: $(echo "$types" | grep -q FAQPage && echo present || echo none on home page — check answer pages)"
say ℹ️ "Bing Webmaster Tools / GSC registration cannot be checked from outside — ask the user"

# ---------- GEO ----------
echo; echo "[GEO]"
lc=$(code "$url/llms.txt")
say "$([ "$lc" = 200 ] && echo ✅ || echo ❌)" "llms.txt $lc  $( [ "$lc" = 200 ] && get "$url/llms.txt" | head -1 )"
# ponytail: robots groups resolved per bot only (no wildcard/path matching); enough to spot Disallow: /
bots="GPTBot OAI-SearchBot ChatGPT-User ClaudeBot Claude-SearchBot Claude-User PerplexityBot Perplexity-User Google-Extended Bingbot Yeti"
printf '%s\n' "$robots" | tr -d '\r' | awk -v bots="$bots" '
  BEGIN{n=split(bots,B," "); for(i=1;i<=n;i++){want[tolower(B[i])]=B[i]}}
  /^[ \t]*#/ {next}
  tolower($0) ~ /^user-agent:/ { ua=tolower($0); sub(/^user-agent:[ \t]*/,"",ua); if(!inua){delete cur}; cur[ua]=1; inua=1; next }
  tolower($0) ~ /^(dis)?allow:/ { inua=0; rule=$0; sub(/^[Aa]llow:[ \t]*/,"allow ",rule); sub(/^[Dd]isallow:[ \t]*/,"disallow ",rule)
      for(u in cur){ if(rule=="disallow /") blocked[u]=1; seen[u]=1 } next }
  END{ for(k in want){ u=tolower(k)
         if(blocked[u]) s="❌ blocked"; else if(seen[u]) s="✅ allowed"; else if(blocked["*"]) s="❌ blocked via *"; else s="ℹ️ unspecified (falls to *)"
         printf "%-18s %s\n", want[k], s } }' | sort
say ℹ️ "Google-Extended only governs Gemini training/grounding; AI Overviews use the normal Googlebot index"

# ---------- LLMO ----------
echo; echo "[LLMO]"
org=$(grep -oE '"@type" *: *"(Organization|WebSite|Person)"' "$tmp/html" | wc -l | tr -d ' ')
same=$(grep -oE '"sameAs"' "$tmp/html" | wc -l | tr -d ' ')
say "$([ "$org" -ge 1 ] && echo ✅ || echo ⚠️)" "Organization/WebSite entity LD: $org  |  sameAs declared: $same (link every official surface)"
say ℹ️ "brand-name consistency and model recall must be checked by hand (references/llmo.md §4)"

# ---------- NEO ----------
echo; echo "[NEO]"
nv=$(meta naver-site-verification "$tmp/html")
say "$([ -n "$nv" ] && echo ✅ || echo ℹ️)" "naver-site-verification meta: $([ -n "$nv" ] && echo present || echo 'absent (Search Advisor may be verified another way — ask)')"
vp=$(meta viewport "$tmp/html")
say "$([ -n "$vp" ] && echo ✅ || echo ❌)" "viewport meta (Naver is mobile-first): ${vp:-missing}"
say ℹ️ "Yeti policy: see robots table above"
