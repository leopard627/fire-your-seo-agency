# SEO — 기술 기반 체크리스트

이 레인의 목표는 **대상 크롤러가 핵심 콘텐츠를 가져오고 해석할 수 있게** 만드는 것.
Google은 JavaScript를 렌더링하지만 모든 검색·AI 크롤러가 같은 기능을 지원하지는 않는다.
초기 HTML 제공은 호환성과 안정성에 유리하다. CSR이라는 이유만으로 색인 불가라고 판정하지 않는다.

## 1. 콘텐츠 노출

- [ ] 대표 URL(홈·목록·상세)을 비로그인으로 요청하여 상태 코드·최종 URL·본문을 저장한다.
      로그인·동의·봇 차단 화면이면 실제 콘텐츠 접근 제한으로 기록한다.
- [ ] robots.txt, robots meta, `X-Robots-Tag`를 함께 확인한다. robots.txt 차단은
      색인 제외를 보장하지 않으며, 차단된 URL의 `noindex`는 크롤러가 읽지 못할 수 있다.
- [ ] `curl -sL <url>` 초기 HTML과 브라우저 렌더 후 DOM의 본문·링크·메타·JSON-LD를 비교한다.
      차이가 크면 리소스 차단·JS 오류·사용자 클릭 의존 로딩을 확인하고 SSR·SSG 등을 검토한다.
- [ ] Search Console 접근 권한이 있으면 URL 검사의 색인 상태와 실시간 렌더 결과를 확인한다.
      브라우저에서 보이는 것과 Google의 실제 색인 여부를 구분하고, 권한이 없으면 미확인으로 남긴다.
- [ ] ⚠️ **CSR 바일아웃 함정**: SSR 프레임워크에서도 특정 훅·API 사용이 페이지를 통째로
      클라이언트 렌더로 바꿀 수 있다. 배포 전후 대표 페이지의 초기 HTML과 렌더 결과를 비교한다.

근거: [Google JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics),
[robots.txt의 한계](https://developers.google.com/search/docs/crawling-indexing/robots/intro).

## 2. 사이트맵

- [ ] sitemap.xml 존재 + robots.txt에서 참조
- [ ] 검색에 노출할 정본 상세 URL(제품·글·항목)이 포함되는가 — 목록 페이지만 넣지 않는다.
- [ ] 파일당 5만 URL·50MB(압축 해제 기준)를 넘지 않도록 분할한다 (sitemap index + 파트).
- [ ] 새 콘텐츠 유형의 정본 URL과 실제 변경을 반영한 `lastmod`를 갱신한다.
      사이트맵은 발견을 돕는 힌트이며 색인을 보장하지 않는다.

근거: [Google 사이트맵 작성](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).

## 3. 메타

- [ ] 제목은 페이지 내용을 정확하고 간결하게 설명하며 불필요한 키워드 반복을 피한다.
- [ ] 설명은 해당 페이지의 유용성을 요약한다. 고정 글자 수를 색인 통과 기준으로 쓰지 않는다.
- [ ] 제목·설명은 페이지별로 구분한다. Google이 표시 문구를 재작성할 수 있음을 감안한다.
- [ ] OG 이미지: 공유 시 보이는 얼굴. 페이지 유형별 동적 생성이 이상적

근거: [제목 링크](https://developers.google.com/search/docs/appearance/title-link),
[검색 스니펫](https://developers.google.com/search/docs/appearance/snippet).

## 4. 구조화 데이터 (JSON-LD)

- [ ] 페이지 유형에 맞는 스키마: Article, Product, FAQPage, BreadcrumbList, Organization
- [ ] 구조화 데이터는 사용자가 보는 콘텐츠와 사실이 일치해야 한다. 없는 정보·후기를 만들지 않는다.
- [ ] 같은 엔티티는 일관된 `@id`와 속성으로 연결한다. 페이지 간 상충되는 기관 정보를 피한다.
- [ ] 요청 시 실제 페이지에서 확인한 값으로 JSON-LD를 생성·수정하고, 미확인 값은 임의로 채우지 않는다.
- [ ] 게시 전 JSON 문법과 Schema Markup Validator로 구조를 검증하고, 지원 유형은 Rich Results Test로 확인한다.
      게시 후 실제 URL로 다시 검사한다. 문법·스키마 통과가 리치 결과 노출을 보장하지는 않는다.

근거: [Google 구조화 데이터 정책](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).

## 5. URL·응답 위생

- [ ] canonical: 파라미터 변형·중복 경로가 하나의 정본을 가리키게
- [ ] 다국어면 hreflang 상호 참조 (한쪽만 걸면 무효)
- [ ] 없는 페이지는 200이 아니라 404를 — soft 404는 색인 예산을 태운다
- [ ] ⚠️ **404 베이크 함정**: ISR·CDN 캐시 계층에서 일시 장애의 404가 몇 시간씩 구워질 수 있다.
      데이터 조회 실패 시 404를 반환하지 말고 throw(재시도)하라 — "없음"과 "못 가져옴"은 다르다
- [ ] 리다이렉트 체인 1홉 이내

## 6. Core Web Vitals 실측·성능

- [ ] 대표 URL별 PageSpeed Insights(PSI)의 모바일·데스크톱 결과를 확보한다.
      보고서 URL·조회일·기기·측정 범위(URL 또는 origin)를 함께 적는다.
- [ ] **필드 데이터**: CrUX의 최근 28일, 75백분위 LCP·INP·CLS를 각각 기록한다.
      URL 데이터가 없어 origin으로 대체되면 해당 페이지의 실측값으로 표현하지 않는다.
- [ ] 양호 기준: **LCP ≤ 2.5초 / INP ≤ 200ms / CLS ≤ 0.1**. 각 지표와 도구의 전체 판정을 구분한다.
      값이 없으면 `데이터 없음`, 실행하지 못했으면 `미측정`으로 표시하고 추정 점수를 만들지 않는다.
- [ ] **랩 데이터**: PSI/Lighthouse의 환경·LCP·CLS·TBT·진단 항목을 별도 기록한다.
      Lighthouse 탐색 측정의 TBT는 INP가 아니며, 성능 점수만으로 CWV 통과를 선언하지 않는다.
- [ ] LCP 요소와 로딩 지연, 긴 JS 작업(INP), 이미지·광고 공간 미확보(CLS)를 근거로 우선순위를 정한다.
      수정 후 같은 조건의 랩 측정을 비교하고, 필드의 28일 집계에는 과거 방문이 섞임을 명시한다.
- [ ] 이미지 WebP/AVIF + 명시적 width/height (CLS). 실제 LCP 이미지에 lazy-loading을 피하고
      필요한 경우에만 preload·우선순위를 조정한다. 모든 이미지·폰트를 미리 읽지 않는다.
- [ ] 로고·아이콘은 무손실 최적화 — 수백 KB 로고가 전 페이지에 실리는 낭비가 흔하다

근거: [Web Vitals 지표](https://web.dev/articles/vitals),
[PSI 데이터·판정](https://developers.google.com/speed/docs/insights/v5/about),
[필드와 랩의 차이](https://web.dev/articles/lab-and-field-data-differences).

## 7. 모바일·렌더링 일치

- [ ] 모바일 화면에서 viewport, 가로 넘침, 글자 가독성, 터치 조작, 본문을 가리는 팝업을 확인한다.
- [ ] 모바일·데스크톱의 핵심 본문·제목·robots·구조화 데이터가 동등한지 비교한다.
      레이아웃은 달라도 된다. 핵심 콘텐츠를 클릭·스크롤해야만 네트워크로 불러오는지 확인한다.
- [ ] 모바일에서 필요한 CSS·JS·이미지가 차단되지 않는지, 별도 모바일 URL이 있다면
      대응 URL·리다이렉트·canonical/alternate가 일관되는지 확인한다.

근거: [Google 모바일 우선 색인](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing).

## 8. HTTPS·안전한 콘텐츠 전달

- [ ] HTTPS 인증서의 유효기간·호스트 일치·인증서 오류와 HTTP→HTTPS 리다이렉트를 확인한다.
      내부 링크·canonical·사이트맵도 의도한 HTTPS URL을 가리켜야 한다.
- [ ] 브라우저 콘솔·네트워크에서 혼합 콘텐츠와 차단된 리소스를 확인한다.
      특히 HTTP 스크립트·스타일·iframe 때문에 본문이나 기능이 사라지는지 기록한다.
- [ ] 보안 헤더는 실제 응답을 기록하고 CSP 등으로 정상 리소스가 차단되는지 확인한다.
      헤더 하나의 누락을 색인 불가로 단정하지 않는다. 이 점검은 침투테스트나 보안 인증이 아니다.

근거: [web.dev 혼합 콘텐츠](https://web.dev/articles/what-is-mixed-content).

## 9. 색인 가속

- [ ] IndexNow: 새 페이지·갱신 페이지를 발행 즉시 핑 (Bing·Naver·Yandex 계열이 소비)
- [ ] Google은 IndexNow 미지원 — 사이트맵 lastmod 정확성으로 승부
- [ ] 대량 발행 시 핑도 발행 파이프라인에 내장하라 — 손으로 하는 핑은 반드시 끊긴다

## 10. 진단 결과 기록

`URL | 검사 항목 | 확인된 사실·증거 | 판정(정상/문제/미확인/미측정) | 영향 | 수정안 | 재검증 방법`
형태로 정리한다. 접근 권한·도구·데이터의 부재를 결함으로 단정하지 않는다.
설치·연결되지 않은 도구를 사용했다고 주장하지 말고, 가능한 공개 검사와 미실행 항목을 구분한다.
