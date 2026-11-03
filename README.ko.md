# 🔥 fire-your-seo-agency

**한국어** · [English](./README.md)

[![GitHub stars](https://img.shields.io/github/stars/leopard627/fire-your-seo-agency?style=flat&logo=github)](https://github.com/leopard627/fire-your-seo-agency/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/leopard627/fire-your-seo-agency?style=flat&logo=github)](https://github.com/leopard627/fire-your-seo-agency/fork)
[![Latest release](https://img.shields.io/github/v/release/leopard627/fire-your-seo-agency?style=flat&label=release)](https://github.com/leopard627/fire-your-seo-agency/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat)](./LICENSE)

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

**거기에 콘텐츠 엔진.** 대행비의 대부분은 "월 N건 포스팅"에 나갑니다. 이 스킬은 그 일을
파이프라인으로 대체합니다: 내 검색 데이터에서 뽑은 질문 백로그, JSON-LD까지 생성하는
frontmatter 콘텐츠 모델, 모든 글이 통과해야 하는 발행 게이트, 글이 썩지 않게 하는
갱신·병합 정책. 성과는 "발행 건수"가 아니라 "노출·인용된 글의 비율"로 잽니다.

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

Codex에서는 `.agents/skills` 아래에 두면 됩니다 (복사본을 저장소에 커밋할 필요 없음):

```bash
git clone https://github.com/leopard627/fire-your-seo-agency.git .agents/skills/fire-your-seo-agency   # 프로젝트
git clone https://github.com/leopard627/fire-your-seo-agency.git ~/.agents/skills/fire-your-seo-agency # 개인
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
6. **콘텐츠 엔진** — 서브 블로그 세팅, 질문 백로그, 발행 게이트, 갱신·병합 정책
7. **측정 루프** — 고치고 끝이 아니라, 재측정 일정을 잡고 숫자로 확인합니다

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
  content.md          ← 콘텐츠 운영 (서브 블로그·콘텐츠 모델·백로그·발행 게이트·갱신)
  measure.md          ← 측정 루프 (고치고 끝이 아니다)
  en/                 ← 전체 레퍼런스 영문 미러 (사람 독자용)
.claude-plugin/       ← 플러그인·마켓플레이스 매니페스트 (/plugin 설치 지원)
tools/                ← 저장소 검사(validate.py) + 외부 도메인 허용 목록
tests/                ← 검사별 단위 테스트
.github/workflows/    ← 푸시·PR마다 검사·테스트, 매월 크롤러 표 신선도 점검
```

> `references/`의 한국어 문서가 정본이고(에이전트가 읽는 것), `references/en/`은
> 사람 독자를 위한 영문 미러입니다.

## 저장소 검사

`.github/workflows/validate.yml`이 푸시·PR마다 돌리는 검사입니다 (표준 라이브러리만 사용):

```bash
python3 tools/validate.py                   # 저장소 검사
python3 -m unittest discover -s tests -t .  # 검사기 테스트
python3 tools/validate.py --max-age 100     # 크롤러 표 확인일이 100일 넘었는가 (매월 자동)
```

- **도메인** — 문서에 나오는 모든 외부 URL·도메인은 `tools/allowed-domains.txt`에 있어야
  합니다. 새 도메인은 그 파일을 고치는 diff로만 들어옵니다
- **크롤러** — `geo.md`의 AI 크롤러 표와 `measure.md`의 로그 집계 명령이 같은 User-agent를
  다루는지 (한/영 모두)
- **릴리스** — `SKILL.md`·`plugin.json`·`marketplace.json`·`CHANGELOG.md`의 이름·버전 일치
- **미러** — 영문 미러가 한국어 정본과 구조(제목·절 번호·표·체크박스)와 외부 출처가 같은지
- **링크·스킬** — 상대 링크·앵커·경로 언급이 실재하는지, `SKILL.md` frontmatter 한도

기여 기준은 [CONTRIBUTING.md](./CONTRIBUTING.md)에 있습니다.

## Star History

<a href="https://www.star-history.com/#leopard627/fire-your-seo-agency&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=leopard627/fire-your-seo-agency&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=leopard627/fire-your-seo-agency&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=leopard627/fire-your-seo-agency&type=Date" />
  </picture>
</a>

## 라이선스

MIT — 마음껏 쓰고, 대행비는 아끼세요.
