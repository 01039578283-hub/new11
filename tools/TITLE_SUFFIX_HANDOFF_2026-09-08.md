# 새 홈페이지11: 본문 근거형 타이틀 접미사

작업일: 2026-09-08

## 사이트와 범위

- 사이트: 온담학습.com (`https://xn--jk1bu21awrcryv.com`)
- GitHub: `01039578283-hub/new11`, main. 기존 공개 저장소를 유지한다.
- Vercel: new11, `prj_lTSmPkUtwnQCOfgLLJ8eS16vIgBS`, scope `1992kjb`.
- 변경 전 고정 Git 기준: `a213dc7be304b66dea08493901b9738d89b6914d`.
- HTML 4,841개 중 전국학원·과목별학원 하위 4,836개: 분류 허브 13개 + 지역 상세 4,823개.
- 과목별학원 10분류: 고등/중등/초등/초4/초5 × 수학/영어. 각 371지역.
- 전국학원 3분류: 수학학원/영어학원/영수학원. 각 371지역.
- 홈, 두 최상위 허브, 학습가이드, 상담문의는 수정하지 않는다.
- title 및 기존 og:title/twitter:title 값만 변경한다. 제목 접두사, H1, 본문, FAQ, 후기, 이미지, 숨김 대표 이미지, ALT, 목차, 디자인, URL, canonical, robots, JSON-LD는 유지한다.
- 기존 sitemap.xml 4,841 URL, robots.txt, llms.txt, vercel.json을 그대로 유지한다. 기존에 RSS가 없으므로 이번 작업에서는 생성하지 않는다.

## 선정 원칙

- 페이지의 실제 학습 본문만 근거로 사용하며 지역명이나 난수로 접미사를 배정하지 않는다.
- subject-manuscript 안의 subject-intro와 subject-copy-card를 해석한다. 도입부뿐 아니라 뒤쪽 카드에 배치된 실제 학생의 어려움도 반영한다.
- 전국학원 상세는 실제 답변과 학습 요약을 중심으로 한다. 질문 문장만으로 학습 내용을 추정하지 않는다.
- 센터 정보, 학교 목록, 운영 조건, 등록/환불, 후기와 숨김 내용은 학습 근거에서 제외한다.
- 초등 과정의 접미사에 내신·수능 등을 넣지 않는다. 수학과 영어 근거를 구분한다.
- 문맥이라는 단어가 지역 안내에 쓰인 경우 어휘 문맥 이해로, 방학 진도와 학기 중 복습을 방학 복습으로, 단어·문장의 단순 나열을 둘의 연결 학습으로 바꾸지 않는다.
- 원문 학습 주제가 같으면 접미사가 일부 동일할 수 있다. 모든 접미사를 고유하게 만들기 위해 새로운 내용을 꾸며내지 않는다.

## 실행 및 검증

프로젝트 루트에서 실행한다.

1. `python -m unittest discover -s tools -p test_title_suffixes.py`
2. `python tools/personalize_title_suffixes.py` (수정 없는 계획)
3. `python tools/personalize_title_suffixes.py --write`
4. `python tools/verify_title_release.py` (전수 검사 및 고정 원본 비교)
5. `python tools/personalize_title_suffixes.py --check` (재실행 변경 0 확인)
6. 배포 후 `python tools/verify_title_release.py --public`

원고 생성기를 다시 실행하면 이전의 공통 접미사로 돌아갈 수 있으므로 제목 후처리와 검증을 다시 실행한다. 페이지 수가 바뀌면 고정 범위와 신규 허브 근거를 먼저 점검한다.

- `tools/reports/title-suffix-audit.json`: 페이지별 변경 전후 제목, 실제 근거 문구, 제목 외 내용 해시.
- `tools/reports/title-suffix-local-verification.json`: 전수 검사 결과.
- 계획/공개 검사/배포 증빙은 로컬 보고서로 보관하고 Git 업로드에서 제외한다. tools 전체는 공개 사이트에 업로드하지 않는다.
- 변경 전 기존 목차 검사: 과목별 상세 3,710개, 목차 링크 41,361개, 변경 필요 0. 제목 검증에서도 각 목차를 다시 검사한다.

최종 로컬 검증: 회귀 테스트 55개 통과, 대상 4,836페이지 전수 검사 실패 0, 제목 외 내용 변경 0, 재실행 변경 0. 전체 제목 4,836개 고유, 접미사 조합 1,184개, 제목 길이 25~42자. 기존 사이트맵 4,841 URL과 목차 3,710페이지 보존 확인. 배포 파일 목록은 HTML 4,841개를 포함하며 tools/tmp/환경설정/Git 기록을 제외한 것을 확인했다.

## 사용자 파일과 배포

- 처음부터 untracked인 `tmp/ondam-mobile-final.png`는 수정·삭제·Git 업로드하지 않는다.
- 해당 PNG의 SHA-256은 `cd4ea92d7fb64074e7a76fe834041b742d946a81301ba571b3f0bb6476d9982a`이며 보존 여부를 검사한다. 기존 tmp/ 배포 제외 규칙을 유지한다.
- .env.local은 읽거나 공개하지 않는다. tools/, tmp/, .env, .git 및 .vercel/이 배포 파일 목록에 없는지 확인한다.
- 현재 Vercel 프로젝트에는 Git 자동 배포 연결이 없다. 검증한 main 커밋을 GitHub에 push한 후 동일 소스를 기존 프로젝트에 CLI로 배포한다.
- 배포 후 READY/production, 실제 도메인 alias, 배포 메타데이터의 커밋 일치, 공개 페이지·사이트맵을 확인한다.
- 최종 배포 증빙은 `tools/reports/title-suffix-release.json`에 남긴다. DNS, 요금제, 도메인, 저장소 공개 범위를 변경하지 않는다.
- 검색엔진의 제목 표시와 반영 시점은 재수집 및 검색엔진의 판단에 따르며 노출 순위는 보장하지 않는다.
