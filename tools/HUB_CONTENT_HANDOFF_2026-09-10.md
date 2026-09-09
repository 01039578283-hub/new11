# 온담학습.com 허브 보강 — 2026-09-10

## 범위와 보존

- 사용자 승인: 허브 내용 보강과 공개 배포.
- 저장소: new11 / main. 시작 커밋: 63677e55c3347a0dc01b2c2f35caa6794f8ca56d.
- 정식 주소: https://xn--jk1bu21awrcryv.com (온담학습.com).
- 전국학원 루트+수학/영어/영수3개, 과목별학원 루트+학교급6개+초4/초5 영어/수학4개: 총15개.
- 비대상 공개 HTML4,826개와 기존assets757개(이미지755개)는 초기 원시SHA 그대로 보존.
- title/H1, 기존링크5,176개, 지역앵커 및 ItemList 유지. 전국계열4개 상대 canonical/og:url만 같은경로의 정식도메인 절대주소로 정리.
- 기존 동네 원고, 가격, 시간표, 후기, 전화번호, 이미지, 배포설정은 변경하지 않음. 기존 미추적 tmp/ 보존·커밋제외.

## 보강 내용

- 각 허브 고유3개절·6개문단: 총45절·90문단. 해당주제 질문3개+공통2개로 FAQ75쌍.
- 실제자료 대조 센터32곳 중 허브당3곳, 총45카드·54과목안내. 서로다른3지역 예시, 실제지점수로 오인되지 않게 안내.
- 주소·등록학원명·등록번호·가능학년/과목·실제상세path와조직ID 대조. 초4/초5 정확학년, 영수 같은학년 교집합, 제한조건 보존.
- 공통 학습공간 WebP2개(500×300/800×600) 전체비율 표시. 접기/자르기 없음. 특정지점실사로 표시하지 않음.
- 온담학습의 기존아이보리/녹색·서체 유지, 제목/본문/목차/상담버튼 모바일 배치조정.
- category13개 지역/동네 검색·초기화 추가. JS없이 모든371개링크가 HTML에 남음.
- 메타설명, CollectionPage/ItemList/FAQPage, about/mentions/hasPart 및 실제센터관계 정리.
- sitemap4,841URL 유지, 해당15개 lastmod만2026-09-10으로 갱신. 이전RSS없음 → 이번허브15개 RSS신규 생성.
- 사진 OG전체개편, 새지점/동네생성, 기존전체원고사실감사, 호스팅이전/요금제/DNS변경은 범위아님.

## 검증

- 독립정적QA479/479 PASS. 기존원본HTML/assets보존, 링크/앵커/ItemList 유지, 중복ID·JSON파싱·내부목적지 정상.
- 실제센터45카드와조직ID/과목54개 대조, 조건부·정확학년 회귀16건 PASS.
- 고유문단90개/전용FAQ45개 HTML정확반영. 이전site3/4/6/7/8 전용원고와 동일문단/40자이상문장 재사용0.
- 생성기 재실행 changed0 (멱등성).
- 브라우저15허브×320/390/430/900/1280px=75화면: 가로넘침/작은주요버튼0, 각guide3/센터3/FAQ5.
- category13검색: 명일동1/강동구2/없는검색0/초기화371, 지역13·바로가기13복구와서울앵커 정상.
- FAQ5대표유형+목차, 사진실제로드/전체비율, 명일동고등수학상세이동 확인. 상담전화/문자는 링크표시만 점검하고 실제발신하지 않음.
- 초기전국root 브라우저캐시를 피하여 review query로 최종파일 재점검.

## 재실행 및 자료

- tools/data/hub-guides/subject-copy.json 및 center-examples.json은 고정된 검토입력.
- python tools/enrich_top_hubs_site11.py --date YYYY-MM-DD
- python tools/refresh_enriched_hub_discovery.py --modified YYYY-MM-DDTHH:MM:SS+09:00
- 후자는 현재 허브15개 RSS를 작성하므로, 향후 다른feed항목추가시 보존/병합방식으로 먼저수정.
- bs4 필요. 현장QA 라이브러리는 CodexData/tmp/site15-branches-2026-09-09/qa-libs.
- 독립근거: CodexData/tmp/site11-hub-enrichment-2026-09-10/qa 및 provenance.json, notes.md.
- 브라우저/생성기/공개검증과 최종커밋·배포기록: tools/reports/hub-enrichment/ (gitignore, vercelignore 적용).
- GitHub new11/main에 먼저 반영. Vercel 프로젝트조회 결과 git link=null이므로 자동배포연결을 추가하지 않고, 기존 new11에 CLI production 배포. 최종원격상태/정식도메인HTML·리소스 동일성을 확인하고 RELEASE.md에 기록.
