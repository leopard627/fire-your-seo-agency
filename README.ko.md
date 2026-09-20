# 🔥 fire-your-seo-agency

**한국어** · [English](./README.md)

![fire-your-seo-agency](./assets/social-preview.png)

> **월 50~350만 원짜리 SEO·AEO 대행, 해고하세요. 당신의 AI 에이전트가 직접 합니다.**

"AI 시대 검색 최적화", "챗GPT 인용 보장", "네이버 상위 노출" — 이런 문구로 월 구독료를 받는
대행 서비스가 쏟아지고 있습니다. 그런데 그들이 하는 일의 대부분은 **공개된 표준 문서와
반복 가능한 체크리스트**입니다. 사람이 하면 용역이지만, AI 에이전트가 하면 스킬입니다.

이 저장소는 [Claude Code](https://claude.com/claude-code) 스킬입니다. 설치하면 당신의 에이전트가
사이트를 진단하고, 고칠 것을 직접 고치고, 결과를 측정합니다.

## 만든 사람의 실측

이 스킬은 이론이 아닙니다. 1인 개발 증권 서비스 [치킨스탁](https://www.chickstockfi.com)에 같은 플레이북을 적용해서:

- 30일 검색 노출 **153.9만 회** (전월 대비 +85,578%), 클릭 7.4천
- **네이버 AI 브리핑이 문단마다 인용하는 페이지** 확보 (교과서적 인용 카드 노출)
- 마케팅비 0원 — 전부 검색·AI 인용 유입

과정은 [Threads @kindainvestor](https://www.threads.com/@kindainvestor)에서 공개적으로 기록하고 있습니다.

## 다섯 레인

같은 "검색 최적화"라도 상대하는 엔진이 다릅니다. 이 스킬은 다섯 레인을 구분해서 각각 최적화합니다.

| 레인 | 상대 | 핵심 질문 |
|---|---|---|
| **SEO** | 구글·빙 크롤러 | 크롤러가 내 콘텐츠를 읽고 색인할 수 있는가? |
| **AEO** (Answer Engine) | 구글 AI Overviews, 빙 Copilot | 검색 결과 위 AI 답변이 나를 인용하는가? |
| **GEO** (Generative Engine) | ChatGPT, Perplexity, Claude | 생성 AI가 브라우징할 때 나를 1차 소스로 쓰는가? |
| **LLMO** (LLM Optimization) | 모델 자체의 지식 | 모델이 내 브랜드를 알고, 정확히 아는가? |
| **NEO** (Naver Engine) | 네이버 검색·AI 브리핑 | 한국 시장의 절반, 네이버가 나를 인용하는가? |

**NEO는 이 스킬의 차별점입니다.** 글로벌 AEO 가이드는 네이버를 다루지 않지만,
한국 서비스라면 트래픽의 절반이 네이버에서 옵니다.

## 설치

플러그인으로 (권장 — 한 줄 설치, 업데이트 쉬움):

```
/plugin marketplace add leopard627/fire-your-seo-agency
/plugin install fire-your-seo-agency@fire-your-seo-agency
```

또는 git clone으로:

```bash
# 프로젝트 스킬로 (해당 프로젝트에서만)
git clone https://github.com/leopard627/fire-your-seo-agency.git .claude/skills/fire-your-seo-agency

# 또는 개인 스킬로 (모든 프로젝트에서)
git clone https://github.com/leopard627/fire-your-seo-agency.git ~/.claude/skills/fire-your-seo-agency
```

그리고 Claude Code에서:

```
/fire-your-seo-agency 내 사이트 진단해줘
```

에이전트는 손대기 전에 크롤러의 눈으로 진단부터 하고, 이런 점수표를 먼저 보여줍니다:

| 레인 | 상태 | 근거 |
|---|---|---|
| SEO | ⚠️ | 본문은 SSR이나 상세 페이지 214건이 사이트맵에 누락 |
| AEO | ❌ | 첫 문단 직답 없음, FAQ 구조화 데이터 0건 |
| GEO | ❌ | llms.txt 없음, robots.txt에 AI 크롤러 정책 미정 |
| LLMO | ⚠️ | 브랜드명 표기가 표면마다 3가지로 갈림 |
| NEO | ❌ | 네이버 서치어드바이저 미등록 |

…그다음 우선순위를 제안하고, 구현하고, 재측정 일정을 잡습니다.

## 무엇을 하나

1. **진단** — 사이트를 크롤러의 눈으로 읽고(자바스크립트 없이), 다섯 레인 각각의 현재 상태를 측정합니다
2. **기술 기반** — SSR 노출, 사이트맵, 메타, 구조화 데이터를 고칩니다
3. **의도 랜딩** — "질문 하나 = 페이지 하나" 원칙으로 검색 의도별 페이지를 설계합니다
4. **기계 가독** — llms.txt, JSON-LD, 인용 가능한 문단 구조를 만듭니다
5. **네이버** — 서치어드바이저 등록부터 AI 브리핑 인용 요건까지
6. **측정 루프** — 고치고 끝이 아니라, 재측정 일정을 잡고 숫자로 확인합니다

## 하지 않는 것

- ❌ 백링크 구매, 품앗이 자동화, 콘텐츠 스팸 — **검색엔진과 싸우지 않습니다**
- ❌ "상위 노출 보장" 같은 약속 — 측정 없이는 주장하지 않습니다
- ❌ 키워드 스터핑, 숨긴 텍스트, 클로킹 — 걸리면 계정이 죽는 일은 하지 않습니다

이 스킬의 철학은 하나입니다: **AI가 인용하는 것은 잘 쓴 글이 아니라 정확한 데이터입니다.**
당신이 어떤 숫자의 1차 소스가 되면, 인용은 따라옵니다.

## 구조

```
SKILL.md              ← 에이전트 운영 절차 (진단 → 구현 → 측정)
references/
  seo.md              ← 기술 SEO 체크리스트 + 실전 함정
  aeo.md              ← 답변엔진 최적화 (Bing 등록·AI Overviews·Copilot·E-E-A-T)
  geo.md              ← 생성엔진 최적화 (AI 크롤러 정책·llms.txt·1차 소스)
  llmo.md             ← 모델 인지 최적화 (브랜드 엔티티)
  neo-naver.md        ← 네이버 (서치어드바이저·AI 브리핑·블로그 투트랙)
  measure.md          ← 측정 루프 (고치고 끝이 아니다)
  en/                 ← 전체 레퍼런스 영문 미러 (사람 독자용)
scripts/audit.sh      ← Phase 0 진단 한 방: 다섯 레인 근거를 크롤러의 눈으로 출력 (curl만 사용)
.claude-plugin/       ← 플러그인·마켓플레이스 매니페스트 (/plugin 설치 지원)
```

> `references/`의 한국어 문서가 정본이고(에이전트가 읽는 것), `references/en/`은
> 사람 독자를 위한 영문 미러입니다.

## 라이선스

MIT — 마음껏 쓰고, 대행비는 아끼세요.
