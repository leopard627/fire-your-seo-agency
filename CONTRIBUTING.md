# Contributing

[English below](#english)

이 저장소는 대행사를 대체하는 공개 절차서입니다. 그래서 **측정이나 공식 문서로 확인되는 내용만**
받습니다.

## 받는 것

- 사실 오류·깨진 명령·오탈자 수정
- 검색엔진·AI 크롤러 정책 변경 반영 — **공식 문서 URL**을 PR 설명에 붙여 주세요
- 문서의 절차를 실제로 돌려 보고 발견한 빈틈 — 무엇을 재서 어떤 숫자가 나왔는지와 함께

## 받지 않는 것

- 상업 서비스·제품·도구·대행사로 가는 링크나 언급 (본인 것이든 아니든)
- 특정 사이트·업체 사례 연구, 다른 저장소나 도구 소개
- 측정 근거 없는 "이렇게 하면 좋다"류 주장
- 이 스킬의 사본을 저장소 안에 커밋하는 PR — 설치 방법은 README에 있습니다
- 범위를 크게 넓히는 변경 — 먼저 이슈로 이야기해 주세요

## 규칙

- `references/*.md`(한국어)가 정본입니다. 고치면 `references/en/`의 같은 파일도 같은 PR에서
  고쳐 주세요
- 문서에 새 외부 도메인이 들어가면 CI가 실패합니다. 정말 필요하면
  `tools/allowed-domains.txt`에 추가하고 PR 설명에 이유를 쓰세요. 추가 여부는 메인테이너가
  정합니다
- 올리기 전에:

  ```bash
  python3 tools/validate.py
  python3 -m unittest discover -s tests -t .
  ```

---

## English

This repo is a public playbook that replaces an agency, so it only takes changes that are
**backed by measurement or official documentation**.

**Welcome:** fixes to factual errors, broken commands and typos; updates for search-engine or
AI-crawler policy changes, with the **official documentation URL** in the PR description;
gaps you found by actually running a procedure, with what you measured and the numbers.

**Not accepted:** links to or mentions of commercial services, products, tools or agencies
(yours or anyone's); case studies of specific sites or businesses; promotion of other repos or
tools; claims without measurement; PRs that commit a copy of this skill (see the README for
installation); large scope changes without an issue first.

**Rules:** the Korean `references/*.md` are canonical — change the matching file in
`references/en/` in the same PR. A new outbound domain fails CI; if it is truly needed, add it
to `tools/allowed-domains.txt` and explain why in the PR — the maintainer decides. Run
`python3 tools/validate.py` and `python3 -m unittest discover -s tests -t .` before opening it.
