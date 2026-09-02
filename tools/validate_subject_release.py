from __future__ import annotations

import html
import json
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path


SITE = Path(__file__).resolve().parents[1]
CATEGORIES = ("고등영어학원", "고등수학학원", "초4수학학원", "초4영어학원", "초5수학학원", "초5영어학원")
CATEGORY_LABELS = {
    "고등영어학원": "고등 영어학원",
    "고등수학학원": "고등 수학학원",
    "초4수학학원": "초4 수학학원",
    "초4영어학원": "초4 영어학원",
    "초5수학학원": "초5 수학학원",
    "초5영어학원": "초5 영어학원",
}
BANNED_VISIBLE = (
    "제공된 자료",
    "제공된 학교",
    "제공된 위치",
    "정보성 페이지",
    "정보성 학원 페이지",
    "지역명만 바꾼",
    "학부모가 상담 후 남길 법한",
    "후기 예시",
    "원자료",
    "학원리뷰",
    "학부모 관점에서 정리했습니다",
    "제공된 수업학교",
    "입시 후기",
    "자료에 기재된 학원주소",
    "수업 자료의 센터 안내",
    "상담 자료의 센터 안내",
    "본문에서 이 학교명을 반영",
    "다음 내용이 기재",
    "페이지 원고",
    "검색자가 바로",
    "참고 키워드",
    "참고 확인 항목",
    "제공된 수업 학교",
    "자료의 제공된",
    "페이지의 학교 정보",
    "CSV",
    "입력 데이터",
    "입력값",
    "입력 자료의 학교 항목",
    "입력된 학교 항목",
    "이 행의 학교 항목",
    "이 행의 세부 소재",
    "제공된 단어",
    "가상 학생",
    "가상 유형",
    "데이터에 없",
    "이 글에서 임의",
)
HIGH_MATH_BANNED = (
    "학생의 구체적인 영어 범위",
    "영어에 대한 부담으로 문제 풀이를 미루는 학생",
    "단어를 외워도 오래 기억하지 못하는 학생",
    "읽는 속도가 느려 긴 지문을 부담스러워하는 학생",
    "문법 개념은 알지만 문장에 적용하기 어려운 학생",
    "학생이라는 학생",
    "서안내",
    "원안내",
    "주소는 입력값 그대로",
    "확인된 단어만으로",
    "전달 주기와 매체는",
    "제공되지 않았으므로",
    "특정 학원의 프로그램을 뜻하지 않으며",
    "일반적인 설명을 실제 학생의 성적이나 학교생활 결과로 바꾸어 말해서는 안 됩니다",
    "가상 상황과 실제 학생",
    "해당 학교와 학원의 제휴나 실제 재원 관계",
    "학습을 점검하다",
    "제휴나 실제 수강 관계",
)
HIGH_ENGLISH_BANNED = (
    "학생의 구체적인 수학 범위",
    "참고어인 영어 수학",
    "수학 수업이나 과목 연계",
    "고등 수학 수업을 비교",
    "고등 수학 상담 전",
    "풀이 첫 줄과 마지막 검산",
    "계산·개념·조건 해석",
    "함수와 그래프의 조건을 식과 그림",
    "수열이나 확률·통계 문제",
    "정답 수보다 풀이 과정을 말로 설명",
    "기본 유형과 서술형을 분리",
)
HIGH_SCHOOL_BAD_GRAMMAR = (
    "경우인 경우",
    "합니다 같은 유형",
    "고려합니다고",
    "과정별 과정에서는",
)
HIGH_SCHOOL_BAD_PATTERNS = (
    (re.compile(r"[가-힣]고이\s+(?:포함|수업)"), "학교명 조사 오류"),
    (re.compile(r"같은 유형[^.!?]{0,180}같은 유형"), "같은 유형 반복"),
    (re.compile(r"\.’(?:입니다|을 참고|\s*안내)"), "위치 안내 인용 결합 오류"),
    (re.compile(r"니다\)\."), "괄호 문장부호 위치 오류"),
    (re.compile(r"(?:층|호|옆|앞)\.\)"), "괄호 안 명사구 문장부호 오류"),
    (re.compile(r"학부모라면\s+학부모(?:는|가)"), "학부모 표현 반복"),
    (re.compile(r"학습을 점검한다면\s+학습에서"), "학습 표현 반복"),
    (re.compile(r"\s+[,;:]"), "문장부호 앞 공백"),
    (re.compile(r"\(\s+"), "여는 괄호 뒤 공백"),
    (re.compile(r"에서는\s+(?:실제 풀이 장면|오답 재풀이 과정|학생의 자기 설명)에서는"), "이중 주제 표현"),
)
BAD_GRAMMAR = (
    "학원를",
    "준비이 필요",
    "대비이 필요",
    "시간표이 필요",
    "테스트이 필요",
    "난이도이 필요",
    "방식를 확인",
    "관리 관리",
    "합니다, 이후",
    "상담 상담",
    "수업 수업",
    "학습 학습",
    "학생 학생",
    "초은 ",
    "중은 ",
    "고은 ",
    "니다.을 ",
    "학원이전",
    "센터 자료에서 확인되는 수업 가능 학교에 있는",
    "이 안내에서 기준으로 삼은 학생 유형",
)
JSON_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
STANDALONE_DRAFT_RE = re.compile(r"(?<![가-힣A-Za-z0-9])원고(?![가-힣A-Za-z0-9])")


class VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.main = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "head"}:
            self.skip += 1
        if tag == "main":
            self.main += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "head"} and self.skip:
            self.skip -= 1
        if tag == "main" and self.main:
            self.main -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip and self.main and data.strip():
            self.parts.append(data.strip())


def visible_main(source: str) -> str:
    parser = VisibleText()
    parser.feed(source)
    return re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts))).strip()


def one(pattern: str, source: str, flags: int = 0) -> str:
    matches = re.findall(pattern, source, flags)
    if len(matches) != 1:
        raise ValueError(f"expected one match for {pattern!r}, got {len(matches)}")
    return html.unescape(matches[0]).strip()


def ngrams(text: str, n: int = 3) -> set[tuple[str, ...]]:
    words = re.findall(r"[가-힣A-Za-z0-9]+", text)
    return {tuple(words[i:i + n]) for i in range(max(0, len(words) - n + 1))}


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    descriptions: set[str] = set()
    canonicals: set[str] = set()
    orgs_by_identity: dict[tuple[str, str], set[str]] = defaultdict(set)
    org_signatures: dict[str, set[str]] = defaultdict(set)
    category_bodies: dict[str, list[tuple[str, set[tuple[str, ...]]]]] = defaultdict(list)
    page_count = 0

    for category in CATEGORIES:
        pages = sorted((SITE / "과목별학원" / category).glob("*/index.html"))
        if len(pages) != 371:
            errors.append(f"{category}: expected 371 local pages, got {len(pages)}")
        category_descriptions: set[str] = set()
        for page in pages:
            page_count += 1
            source = page.read_text(encoding="utf-8")
            rel = page.relative_to(SITE).as_posix()
            try:
                title = one(r"<title>(.*?)</title>", source, re.S).removesuffix(" | 온담학습")
                h1 = one(r"<h1>(.*?)</h1>", source, re.S)
                description = one(r'<meta name="description" content="([^"]*)">', source)
                canonical = one(r'<link rel="canonical" href="([^"]*)">', source)
                og_url = one(r'<meta property="og:url" content="([^"]*)">', source)
            except ValueError as exc:
                errors.append(f"{rel}: {exc}")
                continue

            if title != h1:
                errors.append(f"{rel}: title/H1 mismatch")
            if canonical != og_url:
                errors.append(f"{rel}: canonical/og:url mismatch")
            if len(description) > 80:
                errors.append(f"{rel}: description too long ({len(description)})")
            if description in category_descriptions:
                errors.append(f"{rel}: duplicate category description")
            category_descriptions.add(description)
            descriptions.add(description)
            canonicals.add(canonical)

            text = visible_main(source)
            if STANDALONE_DRAFT_RE.search(text):
                errors.append(f"{rel}: internal wording remains: 원고")
            for token in BANNED_VISIBLE:
                if token in text:
                    errors.append(f"{rel}: internal wording remains: {token}")
            if category == "고등수학학원":
                for token in HIGH_MATH_BANNED:
                    if token in text:
                        errors.append(f"{rel}: subject mismatch remains: {token}")
            if category == "고등영어학원":
                for token in HIGH_ENGLISH_BANNED:
                    if token in text:
                        errors.append(f"{rel}: subject mismatch remains: {token}")
            if category in {"고등수학학원", "고등영어학원"}:
                for token in HIGH_SCHOOL_BAD_GRAMMAR:
                    if token in text:
                        errors.append(f"{rel}: malformed wording remains: {token}")
                for pattern, label in HIGH_SCHOOL_BAD_PATTERNS:
                    if pattern.search(text):
                        errors.append(f"{rel}: malformed wording remains: {label}")
            for token in BAD_GRAMMAR:
                if token in text:
                    errors.append(f"{rel}: malformed wording remains: {token}")
            local = title.removesuffix(" " + CATEGORY_LABELS[category]).strip()
            if f"{local}에서 {local}" in text:
                errors.append(f"{rel}: duplicated locality phrase")
            if text.count(title) > 12:
                warnings.append(f"{rel}: exact target phrase repeated {text.count(title)} times")
            if '<nav class="breadcrumb" aria-label="현재 위치">' not in source or 'aria-current="page"' not in source:
                errors.append(f"{rel}: semantic breadcrumb missing")

            payloads = JSON_RE.findall(source)
            if len(payloads) != 1:
                errors.append(f"{rel}: JSON-LD block count {len(payloads)}")
                continue
            try:
                graph = json.loads(payloads[0]).get("@graph", [])
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: JSON-LD parse error {exc}")
                continue
            org = next((node for node in graph if "EducationalOrganization" in (node.get("@type") if isinstance(node.get("@type"), list) else [node.get("@type")])), None)
            if not org:
                errors.append(f"{rel}: organization missing")
            else:
                address = org.get("address", {})
                identity = (org.get("name", ""), address.get("streetAddress", ""))
                orgs_by_identity[identity].add(org.get("@id", ""))
                stable_fields = {
                    key: org.get(key)
                    for key in (
                        "name", "alternateName", "telephone", "image", "address", "areaServed",
                        "knowsAbout", "makesOffer", "identifier",
                    )
                }
                org_signatures[org.get("@id", "")].add(
                    json.dumps(stable_fields, ensure_ascii=False, sort_keys=True)
                )
                if address.get("streetAddress") and not address.get("addressRegion"):
                    errors.append(f"{rel}: addressRegion missing")
                if address.get("streetAddress") and not address.get("addressLocality"):
                    errors.append(f"{rel}: addressLocality missing")
            for node in graph:
                if str(node.get("@id", "")).endswith("#schools") and not node.get("itemListElement"):
                    errors.append(f"{rel}: empty school ItemList")
            if category in {"고등수학학원", "고등영어학원"}:
                has_grade_notice = 'class="subject-grade-availability-notice"' in source
                has_service = any(str(node.get("@id", "")).endswith("#service") for node in graph)
                if has_grade_notice == has_service:
                    errors.append(f"{rel}: grade availability notice/service schema mismatch")

            match = re.search(r'<section class="section subject-manuscript">(.*?)</section>\s*<section class="section subject-center-card">', source, re.S)
            if match:
                body_text = visible_main("<main>" + match.group(1) + "</main>")
                normalized = body_text.replace(title, " ").replace(local, " ")
                category_bodies[category].append((rel, ngrams(normalized)))

        print(f"{category}: pages={len(pages)} unique_descriptions={len(category_descriptions)}")

    fragmented = {identity: ids for identity, ids in orgs_by_identity.items() if len(ids) > 1}
    if fragmented:
        errors.append(f"organization identities fragmented: {len(fragmented)}")
    inconsistent = {org_id: signatures for org_id, signatures in org_signatures.items() if len(signatures) > 1}
    if inconsistent:
        errors.append(f"organization entities inconsistent: {len(inconsistent)}")

    for category, docs in category_bodies.items():
        maximum = (0.0, "", "")
        over_092 = 0
        for i, (left_name, left) in enumerate(docs):
            for right_name, right in docs[i + 1:]:
                if not left or not right:
                    continue
                score = len(left & right) / len(left | right)
                if score >= 0.92:
                    over_092 += 1
                if score > maximum[0]:
                    maximum = (score, left_name, right_name)
        print(f"{category}: max_normalized_3gram={maximum[0]:.3f} pairs_ge_0.92={over_092}")

    print(f"local_pages={page_count} unique_canonical={len(canonicals)} unique_description={len(descriptions)}")
    print(f"stable_center_identities={len(orgs_by_identity)} warnings={len(warnings)} errors={len(errors)}")
    for item in warnings[:20]:
        print("WARN", item)
    for item in errors[:50]:
        print("ERROR", item)
    if len(errors) > 50:
        print(f"ERROR ... {len(errors) - 50} more")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
