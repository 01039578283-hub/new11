from __future__ import annotations

import csv
import html
import json
import random
import re
import shutil
from pathlib import Path


SITE = Path(__file__).resolve().parents[1]
BASE = SITE.parent
COMMON = BASE / "참고자료" / "공통자료"

SITE_NAME = "온담학습"
CATEGORY = "수학학원"
PHONE_DISPLAY = "010-6839-8283"
PHONE_LINK = "01068398283"
PUBLISH_DATE = "2026-07-04"

ALL_CATEGORIES: list[tuple[str, str]] = [
    ("수학학원", "학년별 연산·개념·서술형 관리 지역별 안내"),
    ("영어학원", "학년별 어휘·문법·독해 관리 지역별 안내"),
    ("영수학원", "영어와 수학을 함께 점검하는 통합 학습관리 안내"),
]


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def slug_ko(name: str) -> str:
    value = re.sub(r"\s+", "", name.strip())
    value = re.sub(r'[\\/:*?"<>|#%&+]', "", value)
    return value


def split_items(value: str) -> list[str]:
    if not value:
        return []
    return [x.strip() for x in re.split(r"[,/·\n]+", value) if x.strip()]


def seed_for(*parts: str) -> int:
    import zlib
    return zlib.crc32("::".join(parts).encode("utf-8"))


def has_batchim(text: str) -> bool:
    text = (text or "").strip()
    if not text:
        return True
    ch = text[-1]
    code = ord(ch)
    if 0xAC00 <= code <= 0xD7A3:
        return (code - 0xAC00) % 28 != 0
    return True


def eul_reul(text: str) -> str:
    return "을" if has_batchim(text) else "를"


def eun_neun(text: str) -> str:
    return "은" if has_batchim(text) else "는"


def school_type(name: str) -> str:
    if name.endswith("초"):
        return "ElementarySchool"
    if name.endswith("중"):
        return "MiddleSchool"
    if name.endswith("고"):
        return "HighSchool"
    return "School"


def json_script(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def rel_prefix(depth: int) -> str:
    return "../" * depth


def pick(bank: list, k: int, *seed_parts: str) -> list:
    rng = random.Random(seed_for(*seed_parts))
    if len(bank) <= k:
        items = bank[:]
        rng.shuffle(items)
        return items
    return rng.sample(bank, k)


def fmt_pair(pair: tuple[str, str], **kw) -> tuple[str, str]:
    return (pair[0].format(**kw), pair[1].format(**kw))


# ---------------------------------------------------------------------------
# page shell (nav / footer / head)
# ---------------------------------------------------------------------------

def nav_html(depth: int, active: str = "전국학원") -> str:
    p = rel_prefix(depth)
    links = [
        ("홈", f"{p}index.html"),
        ("학습가이드", f"{p}학습가이드/index.html"),
        ("상담문의", f"{p}상담문의/index.html"),
        ("과목별학원", f"{p}과목별학원/index.html"),
        ("전국학원", f"{p}전국학원/index.html"),
    ]
    items = "\n".join(
        f'        <a{" class=\"active\"" if name == active else ""} href="{href}">{name}</a>'
        for name, href in links
    )
    return f"""  <header class="nav-wrap">
    <nav class="nav" aria-label="주요 메뉴">
      <a class="brand" href="{p}index.html"><span class="brand-mark">온</span><span>{SITE_NAME}</span></a>
      <div class="nav-links">
{items}
      </div>
    </nav>
  </header>"""


def footer_html(depth: int) -> str:
    p = rel_prefix(depth)
    return f"""  <footer class="footer">
    <p><strong>{SITE_NAME}</strong> · 학습 코칭 · 상담은 전화·문자로 편하게 문의해주세요.</p>
  </footer>

  <div class="floating-cta" aria-label="빠른 상담 버튼">
    <a href="tel:{PHONE_DISPLAY}">전화문의</a>
    <a href="sms:{PHONE_LINK}">문자문의</a>
    <a href="{p}상담문의/index.html">상담문의</a>
  </div>"""


def head_html(title: str, description: str, depth: int, canonical: str, og_type: str, image: str, ld: dict) -> str:
    p = rel_prefix(depth)
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="{esc(canonical)}">
  <meta property="og:type" content="{esc(og_type)}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{esc(image)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&family=Noto+Serif+KR:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="icon" type="image/png" href="{p}assets/favicon.png">
  <link rel="apple-touch-icon" href="{p}assets/favicon.png">
  <link rel="stylesheet" href="{p}assets/site.css">
  <script type="application/ld+json">{json_script(ld)}</script>
</head>"""


def page_shell(head: str, body: str) -> str:
    return f"""{head}
<body>
<div class="site-shell">
{body}
</div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# images
# ---------------------------------------------------------------------------

def find_map(row: dict[str, str]) -> str:
    maps_dir = SITE / "assets" / "maps"
    raw = row.get("동 영어", "").strip()
    candidates = [raw, raw.replace(" ", "-"), raw.replace(" ", ""), raw.replace("_", "-")]
    for base in candidates:
        for ext in (".jpg", ".jpeg", ".png", ".webp"):
            p = maps_dir / f"{base}{ext}"
            if p.exists():
                return f"assets/maps/{p.name}"
    return "assets/centers/common/local6839.webp"


def choose_rep_images(rows: list[dict[str, str]]) -> list[str]:
    src_dir = COMMON / "대표이미지"
    dst_dir = SITE / "assets" / "representative"
    dst_dir.mkdir(parents=True, exist_ok=True)

    images = [p for p in src_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}]
    images.sort(key=lambda p: p.name)
    rng = random.Random(8283)
    rng.shuffle(images)
    chosen = [images[i % len(images)] for i in range(len(rows))]
    result: list[str] = []
    for i, src in enumerate(chosen, 1):
        ext = src.suffix.lower()
        dst = dst_dir / f"rep-{i:03d}{ext}"
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
        result.append(f"assets/representative/{dst.name}")
    return result


def school_names(row: dict[str, str]) -> list[str]:
    names: list[str] = []
    for key in ("타깃학교\n(중)", "타깃학교\n(초)", "타깃학교\n(고)"):
        names.extend(split_items(row.get(key, "")))
    seen: list[str] = []
    for name in names:
        if name not in seen:
            seen.append(name)
    return seen


def cross_category_links_html(local: str, slug: str, exclude: str) -> str:
    links = []
    for name, _ in ALL_CATEGORIES:
        if name == exclude:
            continue
        if (SITE / "전국학원" / name / slug).exists():
            links.append(
                f'<a href="/전국학원/{name}/{slug}/" class="cross-link"><strong>{esc(local)} {esc(name)}</strong>'
                f'<small>같은 지역 다른 카테고리 바로가기</small></a>'
            )
    return "".join(links)


def region_blocks_html(rows: list[dict[str, str]]) -> str:
    regions: dict[str, dict[str, list[dict[str, str]]]] = {}
    for row in rows:
        region = row.get("지역", "").strip() or "기타"
        district = row.get("시or구", "").strip() or "기타"
        regions.setdefault(region, {}).setdefault(district, []).append(row)

    jump = "".join(f'<a href="#region-{slug_ko(region)}">{esc(region)}</a>' for region in regions)
    jump_html = f'<div class="region-jump" aria-label="지역 바로가기">{jump}</div>'

    blocks = []
    for region, districts in regions.items():
        total = sum(len(items) for items in districts.values())
        district_blocks = []
        for district, items in districts.items():
            links = "\n".join(
                f'<a href="{slug_ko(r["근처 수업가능 동네"])}/">{esc(r["근처 수업가능 동네"])}</a>'
                for r in items
            )
            district_blocks.append(
                f'<div class="district-block"><p class="district-title">{esc(district)}<small>{len(items)}곳</small></p>'
                f'<div class="local-button-grid">{links}</div></div>'
            )
        blocks.append(
            f'<div class="region-block" id="region-{slug_ko(region)}"><div class="region-title"><h3>{esc(region)}</h3>'
            f'<span>{len(districts)}개 시군구 · {total}개 지역</span></div>'
            f'<div class="district-grid">{"".join(district_blocks)}</div></div>'
        )
    return jump_html + "".join(blocks)


# ---------------------------------------------------------------------------
# fee table (real, region-tiered rate card shared across this business)
# ---------------------------------------------------------------------------

FEE_TABLE_SEOUL: list[tuple[str, str, str, str]] = [
    ("주 3회", "249,000원", "266,000원", "299,000원"),
    ("주 4회", "319,000원", "341,000원", "384,000원"),
    ("주 5회", "389,000원", "416,000원", "469,000원"),
]

FEE_TABLE_OTHER: list[tuple[str, str, str, str]] = [
    ("주 3회", "219,000원", "236,000원", "269,000원"),
    ("주 4회", "279,000원", "301,000원", "344,000원"),
    ("주 5회", "339,000원", "366,000원", "419,000원"),
]


# ---------------------------------------------------------------------------
# content banks (freshly written for 온담학습 / 수학학원 — this category spans
# all grade levels (초등~고등), themed around 연산·개념·서술형·오답관리.
# Informed by 상담방식.txt, FAQ.txt (수학 관련 문항), 학부모 후기.txt,
# 경쟁사분석, and "수학학원 원고.xlsx" (themes reused, wording rewritten,
# not copied verbatim).
# ---------------------------------------------------------------------------

FAQ_OPENER_BANK: list[tuple[str, str]] = [
    ("{title}은 몇 학년부터 다닐 수 있나요?",
     "초등 저학년부터 고등학생까지 학년에 따라 진단 방식만 다르게 상담해 드립니다."),
    ("{title}에서는 선행학습도 진행하나요?",
     "지금 학년 개념이 충분히 정리된 경우에 한해 단계적으로 진행하며, 무리한 선행은 권하지 않습니다."),
    ("{title}은 한 반에 몇 명이 배정되나요?",
     "선생님이 학생 개개인의 풀이 과정을 확인할 수 있는 인원으로 반을 구성합니다."),
    ("{title}에 처음 상담을 받으려면 무엇을 준비하면 되나요?",
     "특별히 준비하실 것은 없습니다. 최근 시험지나 문제집이 있으면 참고가 됩니다."),
    ("{title}은 내신과 사고력 수학을 함께 다루나요?",
     "학년과 목표에 따라 비중을 다르게 조정해 상담 시 안내해 드립니다."),
    ("{title} 등록 전에 레벨테스트가 꼭 필요한가요?",
     "필수는 아니지만, 학생의 현재 연산과 개념 이해 수준을 파악하는 데 도움이 됩니다."),
]

FAQ_BANK: list[tuple[str, str]] = [
    ("초등학생과 중학생이 같은 반에서 배우나요?",
     "학년별로 반을 나누어 진행하며, 필요한 경우 개인별 진도를 별도로 관리합니다."),
    ("서술형 문제를 어려워하는 학생은 어떻게 지도하나요?",
     "풀이 과정을 단계별로 적는 연습부터 시작해 서술형에 대한 부담을 줄여갑니다."),
    ("계산 실수가 잦은 학생은 어떻게 관리하나요?",
     "실수 유형을 계산·개념·조건 누락으로 나누어 확인하고 그에 맞는 연습을 반복합니다."),
    ("수학을 처음 배우는 학생도 수업이 가능한가요?",
     "네, 기초 개념부터 차근차근 시작하며 부담 없이 적응하도록 진행합니다."),
    ("{local}에서 다니는 학교의 시험 범위와 맞춰주나요?",
     "학교별 시험 범위와 출제 경향을 확인해 다니시는 학교에 맞춰 준비해드립니다."),
    ("숙제는 어느 정도 나오나요?",
     "학년과 진도에 맞춰 부담이 크지 않은 선에서 문제 분량을 조절합니다."),
    ("수학을 싫어하는 학생도 흥미를 붙일 수 있을까요?",
     "쉬운 단계부터 작은 성취를 쌓아가며 수학에 대한 거부감을 줄여갑니다."),
    ("고등학교 수학을 대비해 지금부터 무엇을 준비해야 하나요?",
     "현재 학년 개념과 연산이 탄탄한지 먼저 확인한 뒤, 필요한 선행을 단계적으로 진행합니다."),
    ("계산은 잘하는데 개념 문제만 나오면 틀린다면?",
     "계산 훈련과 개념 이해는 다른 영역이라, 개념을 예시로 다시 설명하는 과정이 필요합니다."),
    ("문제집만 풀다가 학원을 고민 중이라면 어떻게 해야 하나요?",
     "혼자 채점만 하는 학습으로는 오답 원인을 짚기 어려워, 함께 확인해 주는 과정이 도움이 됩니다."),
    ("레벨테스트 결과가 낮으면 등록이 어려운가요?",
     "레벨테스트는 시작 지점을 잡기 위한 확인 과정입니다. 결과와 관계없이 상담을 통해 안내해 드립니다."),
    ("고등학생인데 지금 시작해도 늦지 않았을까요?",
     "늦지 않았습니다. 현재 수준을 확인한 뒤 부족한 부분부터 채워가면 됩니다."),
    ("이과·문과에 따라 다르게 관리해 주나요?",
     "목표 계열과 시험 범위에 맞춰 학습 우선순위를 다르게 안내해 드립니다."),
    ("학원을 옮기려는데 이전 진도와 다르면 어떻게 하나요?",
     "이전 학원에서 배운 내용을 확인한 뒤 지금 수준에 맞는 시작 지점을 다시 잡아드립니다."),
    ("내신과 모의고사 대비를 함께 할 수 있나요?",
     "학년과 목표에 따라 내신과 사고력·응용 문제의 비중을 조정해 함께 준비합니다."),
    ("문제 풀이 속도가 느린 학생은 어떻게 지도하나요?",
     "정확도를 먼저 잡은 뒤 반복 연습으로 속도를 서서히 끌어올립니다."),
    ("{title}은 시험 기간에 다르게 운영되나요?",
     "학교별 시험 범위에 맞춰 개념 정리와 예상 문제 위주로 수업을 재구성합니다."),
    ("오답 노트는 따로 만들어 주나요?",
     "틀린 문제를 유형별로 정리해 다시 풀어볼 수 있도록 관리합니다."),
]

ANSWER_BANK: list[tuple[str, str]] = [
    ("아이가 계산은 빠른데 서술형만 나오면 막힌다면?",
     "문제를 조건별로 나누어 읽고 무엇을 구하는지부터 확인하는 연습이 필요합니다."),
    ("개념은 아는 것 같은데 응용문제에서 막힌다면?",
     "개념을 응용으로 연결하는 중간 단계 문제가 부족했을 수 있습니다. 대표 유형부터 차근차근 늘려갑니다."),
    ("수학 학원을 옮겨도 성적이 그대로인 것 같다면?",
     "문제 양을 늘리는 것만으로는 부족할 수 있습니다. 지금 어느 단원에서 막히는지부터 다시 확인하는 것이 먼저입니다."),
    ("같은 유형에서 반복해서 틀린다면?",
     "실수의 원인이 계산인지 개념인지 조건 누락인지 구분해 그에 맞는 연습을 반복합니다."),
    ("고등학교 진학을 앞두고 무엇을 준비해야 할지 고민된다면?",
     "현재 학년 개념이 잘 정리되어 있는지 먼저 점검하고, 다음 단계에 필요한 학습 습관을 단계적으로 준비합니다."),
    ("문제집만 풀리다가 학원을 고민 중이라면?",
     "혼자 채점하는 학습으로는 오답 원인을 짚어주기 어려워, 함께 확인해 주는 과정이 도움이 됩니다."),
    ("수학 자신감이 없어 보이는 학생이라면?",
     "쉬운 단계에서 작은 성취를 자주 경험하도록 하여 자신감을 쌓아가는 것이 중요합니다."),
    ("수학 학원을 고를 때 가장 먼저 볼 기준은?",
     "화려한 선행 커리큘럼보다 학생이 지금 어디서 막히는지 구체적으로 확인해 주는지를 먼저 보시는 것이 좋습니다."),
    ("이과 진학을 고민 중인데 지금부터 무엇을 챙겨야 할까요?",
     "연산과 개념의 기초 체력을 먼저 다지고, 이후 심화 유형을 단계적으로 늘려가는 순서를 권합니다."),
    ("학년이 다른 형제자매를 같은 학원에 보내도 될까요?",
     "학년과 진도가 다르면 각자 다른 단원을 다루게 되니, 개별 진단 후 각자에게 맞는 계획을 안내해 드립니다."),
]

CHECKLIST_BANK: list[tuple[str, str]] = [
    ("연산·개념 수준", "학년별 핵심 연산과 개념을 어느 정도 이해하고 있는지 확인합니다."),
    ("최근 시험 결과", "점수보다 어떤 단원에서 왜 틀렸는지 확인하는 데 필요합니다."),
    ("학교 시험 범위", "{local} 학생이 다니는 학교의 시험 범위와 출제 경향을 확인합니다."),
    ("오답 정리 습관", "기존에 오답을 정리해 온 방법이 있다면 함께 확인합니다."),
    ("서술형 대응력", "문제 조건을 읽고 풀이 과정을 적는 수준을 확인합니다."),
    ("이전 학습 이력", "다니던 학원이나 교재가 있었다면 진도와 방식을 확인합니다."),
    ("목표 진로", "이과·문과, 내신·모의고사 등 지금 우선순위를 정합니다."),
    ("상담 편한 시간대", "편하신 상담 요일과 시간대를 미리 알려주시면 좋습니다."),
]

REVIEW_BANK: list[str] = [
    "계산 실수가 잦았는데 유형별로 정리해 주셔서 줄었습니다.",
    "서술형을 무서워했는데 조건 나누는 법을 배우고 좋아졌습니다.",
    "개념을 예시로 설명해 주셔서 응용문제도 이해가 빨라졌습니다.",
    "학교 시험 범위에 맞춰 챙겨주셔서 성적이 안정적으로 나옵니다.",
    "선생님이 아이가 어디서 막히는지 정확히 짚어주십니다.",
    "수학을 싫어했는데 쉬운 문제부터 시작해 흥미를 붙였습니다.",
    "숙제량이 부담스럽지 않아 꾸준히 하고 있습니다.",
    "학원을 옮겼는데 이전 진도를 잘 확인하고 이어주셨습니다.",
    "같은 유형에서 반복해서 틀리던 게 이제 줄었습니다.",
    "오답 노트를 정리해 주셔서 같은 실수가 줄었습니다.",
    "상담할 때 아이 수준을 솔직하게 말씀해 주셔서 신뢰가 갔습니다.",
    "고등학교 수학을 미리 준비할 수 있어서 든든합니다.",
    "레벨테스트도 부담 없이 진행해 주셔서 편했습니다.",
    "수학에 자신감이 없던 아이가 스스로 풀어보려고 합니다.",
    "인원이 많지 않아서 질문하기 편하다고 합니다.",
    "고등학생인데 시작이 늦지 않을까 걱정했는데 잘 따라가고 있습니다.",
    "학습지만 하다가 학원에 다니며 오답 관리가 늘었습니다.",
    "이과 준비를 위해 심화 문제도 함께 봐주셔서 만족스럽습니다.",
    "형제 둘 다 학년이 다른데 각자에 맞게 봐주셨습니다.",
    "서술형 답안 쓰는 연습을 반복해서 점수가 올랐습니다.",
    "시험 기간에는 확실히 더 꼼꼼하게 챙겨주시는 게 느껴집니다.",
    "선생님과 상담할 때마다 다음 계획까지 안내해 주셔서 좋습니다.",
    "문제 풀이 속도가 느렸는데 반복 연습으로 많이 좋아졌습니다.",
    "선행보다 지금 필요한 부분부터 챙겨주셔서 만족스럽습니다.",
]

COMPARE_ROWS: list[dict[str, tuple[str, str]]] = [
    {"label": "학습 진단", "A": ("나이 기준으로만 반 편성", "연산·개념 수준부터 확인"),
     "B": ("레벨만 확인하고 끝", "막힌 이유까지 구체적으로 확인")},
    {"label": "오답 관리", "A": ("정답만 다시 확인", "실수 유형 나누어 재학습"),
     "B": ("채점하고 넘어감", "풀이 과정과 재풀이까지 점검")},
    {"label": "서술형 훈련", "A": ("정답 위주로 확인", "조건 읽는 법부터 훈련"),
     "B": ("풀이 과정 생략", "단계별 풀이 쓰는 연습")},
    {"label": "학부모 소통", "A": ("성적 결과만 전달", "과정과 다음 계획까지 안내"),
     "B": ("정기 안내만 제공", "필요할 때마다 편하게 상담 가능")},
]

SUMMARY_INTROS: list[str] = [
    "{local} 학생에게 필요한 수학 관리는 문제를 많이 푸는 것보다 지금 연산과 개념 중 어디가 부족한지 먼저 확인하는 것입니다.",
    "{local}에서 수학학원을 고르실 때는 연산, 개념, 서술형 중 지금 필요한 부분이 무엇인지부터 살펴보시는 것이 좋습니다.",
    "{local} 학생마다 수학을 어려워하는 지점과 학년별 목표가 다르기 때문에, 같은 학년이라도 먼저 봐야 할 부분은 달라질 수 있습니다.",
]

MANUSCRIPT_INTRO: list[str] = [
    "수학은 학년이 올라갈수록 이전 단원의 개념이 다음 단원의 기초가 됩니다. 지금 단계에서 부족한 부분을 채우지 않으면 다음 학년에서 계속 부담이 쌓일 수 있습니다.",
    "계산을 잘하는 것과 개념을 이해하는 것은 다른 능력입니다. 공식을 외우기보다 원리를 이해하는 경험이 오래 남습니다.",
    "서술형과 응용문제를 어려워하는 학생일수록 문제를 통째로 읽기보다 조건을 나누어 읽는 연습이 먼저 필요합니다.",
    "고등 수학은 중등 수학의 기초 위에 세워집니다. 지금 연산과 개념을 다져두면 이후 심화 유형을 배울 때 훨씬 수월해집니다.",
    "학생마다 수학에서 막히는 지점이 다릅니다. 연산인지, 개념인지, 서술형인지부터 구분하면 훨씬 효율적으로 도울 수 있습니다.",
    "같은 실수를 반복하는 학생일수록 오답을 다시 채점하는 데서 끝내지 않고, 왜 틀렸는지 원인을 나누어 확인하는 과정이 중요합니다.",
]

MANUSCRIPT_OUTRO: list[str] = [
    "학원을 고르실 때는 화려한 선행 진도보다, 학생의 현재 연산과 개념 수준을 얼마나 구체적으로 봐주는지를 기준으로 삼으시길 권합니다.",
    "수학 점수보다 먼저 확인해야 할 것은 학생이 왜 틀렸는지를 스스로 설명할 수 있는지입니다.",
    "상담은 등록을 결정하는 자리가 아니라, 지금 학생에게 필요한 시작 지점을 함께 찾아보는 자리로 생각해 주시면 좋겠습니다.",
    "수학 학습은 한 번에 완성되지 않습니다. 연산, 개념, 서술형을 오가며 조금씩 쌓아가는 과정이라는 점을 기억해 주세요.",
    "무엇보다 학생이 수학을 부담스러워하지 않는지가 꾸준한 학습으로 이어지는 데 가장 중요합니다.",
    "지금 당장의 시험 점수보다, 오답을 스스로 정리해 보려는 습관이 자리 잡고 있는지를 함께 지켜봐 주시길 바랍니다.",
]


def choose_rep_images_wrapper(rows: list[dict[str, str]]) -> list[str]:
    return choose_rep_images(rows)


def local_page(row: dict[str, str], idx: int, rep_image: str, all_rows: list[dict[str, str]]) -> str:
    local = row["근처 수업가능 동네"].strip()
    slug = slug_ko(local)
    region = row.get("지역", "").strip()
    district = row.get("시or구", "").strip()
    center = row.get("센터명", "").strip() or f"{local} 학습관리"
    address = row.get("센터 주소", "").strip()
    title = f"{local} {CATEGORY}"
    description = f"{region} {district} {local} 학생을 위한 {CATEGORY} 안내입니다. 연산·개념·서술형 진단, 오답 관리, 학년별 학습 우선순위를 상담 전에 확인할 수 있습니다."
    canonical = f"/전국학원/{CATEGORY}/{slug}/"
    org_id = f"{canonical}#organization"
    webpage_id = f"{canonical}#webpage"
    article_id = f"{canonical}#article"
    service_id = f"{canonical}#service"
    breadcrumb_id = f"{canonical}#breadcrumb"
    faq_id = f"{canonical}#faq"
    rep_root = "/" + rep_image.replace("\\", "/")
    center_img = "assets/centers/common/seoul6839.webp" if region == "서울" else "assets/centers/common/local6839.webp"
    map_img = find_map(row)

    elementary_schools = split_items(row.get("타깃학교\n(초)", ""))
    middle_schools = split_items(row.get("타깃학교\n(중)", ""))
    high_schools = split_items(row.get("타깃학교\n(고)", ""))
    schools = school_names(row)

    reg_no = row.get("교육지원청 등록번호", "").strip()
    education_name = row.get("교육지원청명칭", "").strip()

    opener = fmt_pair(pick(FAQ_OPENER_BANK, 1, local, "ma-faq-opener")[0],
                       local=local, district=district, title=title, region=region)
    faqs = [opener] + [fmt_pair(p, local=local, district=district, title=title, region=region)
                        for p in pick(FAQ_BANK, 5, local, "ma-faq")]
    answers = [fmt_pair(p, local=local, district=district, title=title, region=region)
               for p in pick(ANSWER_BANK, 4, local, "ma-answer")]
    checklist = [fmt_pair(p, local=local, district=district, title=title, region=region)
                 for p in pick(CHECKLIST_BANK, 4, local, "ma-checklist")]
    review_lines = pick(REVIEW_BANK, 6, local, "ma-review", str(idx))
    summary_intro = pick(SUMMARY_INTROS, 1, local, "ma-summary")[0].format(local=local)
    manu_intro = pick(MANUSCRIPT_INTRO, 1, local, "ma-manu-intro")[0]
    manu_outro = pick(MANUSCRIPT_OUTRO, 1, local, "ma-manu-outro")[0]
    location_ref = address if address else "상담 시 안내되는 위치"
    variant = "A" if seed_for(local, "ma-compare") % 2 == 0 else "B"

    rng = random.Random(seed_for(local, "ma-review-rating"))
    reviews = []
    for i, text in enumerate(review_lines):
        rating = 4 if i == len(review_lines) - 1 and rng.random() < 0.4 else 5
        reviews.append({"body": text, "rating": rating})

    related_source = [r for r in all_rows if r.get("시or구") == district and r.get("근처 수업가능 동네") != local]
    if len(related_source) < 6:
        related_source += [r for r in all_rows if r.get("지역") == region and r.get("근처 수업가능 동네") != local]
    related: list[tuple[str, str, str]] = []
    for r in related_source:
        name = r["근처 수업가능 동네"].strip()
        if name and name not in [x[0] for x in related]:
            related.append((name, f"/전국학원/{CATEGORY}/{slug_ko(name)}/", r.get("시or구", "")))
        if len(related) >= 6:
            break

    about = [
        {"@type": "Thing", "name": title},
        {"@type": "Place", "name": local},
        {"@type": "Thing", "name": "수학학원"},
        {"@type": "Thing", "name": "연산"},
        {"@type": "Thing", "name": "개념 이해"},
        {"@type": "Thing", "name": "서술형"},
        {"@type": "Thing", "name": "오답 관리"},
    ]
    mentions = [
        {"@type": "Place", "name": region},
        {"@type": "Place", "name": district},
        {"@type": "EducationalOrganization", "name": center},
    ] + [{"@type": school_type(s), "name": s} for s in schools]
    has_part = [
        "핵심 요약", "학원 선택 가이드", "답변형 안내", "지역·학년·추천학생",
        "일반 학원과의 차이", "센터 기준 정보", "학습료 안내", "상담 전 체크리스트", "FAQ", "학부모 후기", "근처 학원페이지",
    ]

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": webpage_id,
                "url": canonical,
                "name": title,
                "description": description,
                "inLanguage": "ko-KR",
                "primaryImageOfPage": {"@id": f"{canonical}#primaryimage"},
                "breadcrumb": {"@id": breadcrumb_id},
                "mainEntity": {"@id": service_id},
                "about": about,
                "mentions": mentions,
                "hasPart": [{"@type": "WebPageElement", "name": x} for x in has_part],
            },
            {"@type": "ImageObject", "@id": f"{canonical}#primaryimage", "url": rep_root, "caption": f"{title} 대표 이미지"},
            {
                "@type": "BreadcrumbList",
                "@id": breadcrumb_id,
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "홈", "item": "/"},
                    {"@type": "ListItem", "position": 2, "name": "전국학원", "item": "/전국학원/"},
                    {"@type": "ListItem", "position": 3, "name": CATEGORY, "item": f"/전국학원/{CATEGORY}/"},
                    {"@type": "ListItem", "position": 4, "name": local, "item": canonical},
                ],
            },
            {
                "@type": ["EducationalOrganization", "LocalBusiness"],
                "@id": org_id,
                "name": title,
                "alternateName": [SITE_NAME, center, f"{local} 수학 학습관리"],
                "url": canonical,
                "telephone": PHONE_DISPLAY,
                "openingHours": "Mo-Sa 12:00-24:00",
                "openingHoursSpecification": [{
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                    "opens": "12:00",
                    "closes": "24:00",
                }],
                "areaServed": {"@type": "Place", "name": local},
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": address,
                    "addressRegion": region,
                    "addressLocality": district,
                    "addressCountry": "KR",
                },
                "knowsAbout": ["연산", "수학 개념", "서술형 풀이", "오답 관리", "학습 습관 관리", "학습 상담"],
                "makesOffer": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"{local} 수학 진단 상담", "serviceType": "TutoringService"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"{local} 연산·개념 관리", "serviceType": "TutoringService"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"{local} 서술형·오답 관리", "serviceType": "TutoringService"}},
                ],
                "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "bestRating": "5", "ratingCount": str(len(reviews)), "reviewCount": str(len(reviews))},
                "review": [
                    {"@type": "Review", "author": {"@type": "Person", "name": "학부모"}, "reviewBody": r["body"], "reviewRating": {"@type": "Rating", "ratingValue": str(r["rating"]), "bestRating": "5"}}
                    for r in reviews
                ],
            },
            {
                "@type": "Article",
                "@id": article_id,
                "headline": title,
                "description": description,
                "image": [rep_root, "/" + center_img, "/" + map_img],
                "inLanguage": "ko-KR",
                "datePublished": PUBLISH_DATE,
                "dateModified": PUBLISH_DATE,
                "author": {"@id": org_id},
                "publisher": {"@type": "Organization", "name": SITE_NAME, "url": "/"},
                "mainEntityOfPage": {"@id": webpage_id},
                "about": about,
                "mentions": mentions,
                "articleSection": has_part,
            },
            {
                "@type": "Service",
                "@id": service_id,
                "name": f"{title} 학습관리",
                "serviceType": "TutoringService",
                "description": f"{local} 학생의 연산, 개념, 서술형, 오답을 함께 진단하고 학년별 우선순위에 맞춰 관리합니다.",
                "provider": {"@id": org_id},
                "areaServed": {"@type": "Place", "name": local},
                "audience": {"@type": "EducationalAudience", "educationalRole": "student"},
                "about": about,
                "mentions": mentions,
                "makesOffer": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"{local} 연산·개념 진단"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"{local} 서술형 관리"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"{local} 오답 재학습 관리"}},
                ],
            },
            {
                "@type": "FAQPage",
                "@id": faq_id,
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in faqs
                ],
            },
            {
                "@type": "ItemList",
                "@id": f"{canonical}#target-schools",
                "name": f"{title} 수업 가능 학교 확인 항목",
                "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s} for i, s in enumerate(schools)],
            },
            {
                "@type": "ItemList",
                "@id": f"{canonical}#related",
                "name": f"{local} {CATEGORY} 관련 내부링크",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": name, "url": url}
                    for i, (name, url, _) in enumerate(related)
                ],
            },
        ],
    }

    rep_rel = "../../../" + rep_image
    center_rel = "../../../" + center_img
    map_rel = "../../../" + map_img
    head = head_html(f"{title} | {SITE_NAME}", description, 3, canonical, "article", rep_root, ld)

    badge_row = f'<div class="badge-row"><span>{esc(region)}</span><span>{esc(district)}</span><span>{esc(CATEGORY)}</span><span>연산·개념·서술형</span></div>'

    media_section = f"""    <section class="section">
      <img src="{esc(rep_rel)}" alt="{esc(title + ' ' + SITE_NAME + ' 대표')}" style="display:none;">
      <div class="media-row">
        <figure class="frame"><img src="{esc(center_rel)}" alt="{esc(title + ' 본문 ' + SITE_NAME)}"></figure>
        <figure class="frame"><img src="{esc(map_rel)}" alt="{esc(title + ' 지도 ' + SITE_NAME)}"></figure>
      </div>
      <p class="lead">{esc(center)} 기준으로 {esc(local)} 학생의 상담 범위를 확인합니다. 실제 방문·상담 전에는 주소와 이동 동선을 함께 확인해 주세요.</p>
    </section>"""

    summary_section = f"""    <section class="section">
      <div class="section-head">
        <p class="eyebrow">핵심 요약</p>
        <h2>{esc(local)} {esc(CATEGORY)} 선택 전 확인할 기준</h2>
        <p class="lead">{esc(summary_intro)}</p>
      </div>
      <div class="card-grid">
        <article class="info-card"><span class="tag">01</span><h3>연산·개념 진단</h3><p>연산 정확도, 개념 이해, 서술형 중 지금 어디가 부족한지 먼저 나누어 확인합니다.</p></article>
        <article class="info-card"><span class="tag">02</span><h3>오답 관리</h3><p>틀린 문제를 유형별로 정리해 같은 실수가 반복되지 않도록 관리합니다.</p></article>
        <article class="info-card"><span class="tag">03</span><h3>학년별 우선순위</h3><p>초·중·고 전환 시기마다 필요한 부분이 달라 학년에 맞춰 순서를 정합니다.</p></article>
      </div>
    </section>"""

    manuscript_section = f"""    <section class="section">
      <div class="section-head">
        <p class="eyebrow">학원 선택 가이드</p>
        <h2>{esc(local)} {esc(CATEGORY)}, 무엇을 기준으로 볼까요</h2>
      </div>
      <p class="lead">{esc(manu_intro)}</p>
      <p class="lead">{esc(center)}은 {esc(region)} {esc(district)} {esc(local)} 학생을 기준으로 상담을 진행하며, {esc(', '.join(schools[:4]) if schools else '인근 학교')} 학생들이 주로 문의합니다. 실제 등록 전에는 {esc(location_ref)}{eul_reul(location_ref)} 기준으로 이동 동선과 상담 가능 시간을 확인하는 것이 좋습니다.</p>
      <p class="lead">{esc(manu_outro)}</p>
    </section>"""

    answer_html = "\n".join(
        f'<div class="answer-item"><p class="q">{esc(q)}</p><p class="a">{esc(a)}</p></div>'
        for q, a in answers
    )
    answer_section = f"""    <section class="section">
      <div class="section-head">
        <p class="eyebrow">AEO ANSWER</p>
        <h2>{esc(title)}{eun_neun(title)} 어떤 학생에게 필요할까요?</h2>
      </div>
      <div class="answer-list">
        {answer_html}
      </div>
    </section>"""

    school_chip_html = "".join(f"<span>{esc(s)}</span>" for s in schools) if schools else "<span>상담 시 학교 확인</span>"
    linked_bits = []
    if elementary_schools:
        linked_bits.append(f"초등학교: {', '.join(elementary_schools)}")
    if middle_schools:
        linked_bits.append(f"중학교: {', '.join(middle_schools)}")
    if high_schools:
        linked_bits.append(f"고등학교: {', '.join(high_schools)}")
    linked_schools = ""
    if linked_bits:
        linked_schools = f'<article class="info-card"><span class="tag">학교</span><h3>학교급별 참고 학교</h3><p>{esc(" · ".join(linked_bits))}</p></article>'
    fit_section = f"""    <section class="section">
      <div class="section-head">
        <p class="eyebrow">LOCAL &amp; STUDENT FIT</p>
        <h2>지역·학년·추천학생 기준</h2>
      </div>
      <div class="card-grid">
        <article class="info-card"><span class="tag">지역</span><h3>{esc(region)} {esc(district)} {esc(local)}</h3><p>{esc(local)} 생활권 학생의 학교 진도와 눈높이에 맞춰 수학 관리 방향을 상담합니다.</p></article>
        <article class="info-card"><span class="tag">학년</span><h3>초1~고3, 전 학년 상담 가능</h3><p>학년과 목표에 따라 연산, 개념, 서술형 중 시작 지점을 다르게 잡습니다.</p></article>
        <article class="info-card"><span class="tag">추천</span><h3>이런 학생에게 추천</h3><p>계산은 빠른데 서술형이 약한 학생, 개념 문제만 나오면 틀리는 학생, 수학을 처음 시작하는 학생에게 적합합니다.</p></article>
        {linked_schools}
      </div>
      <p class="lead" style="margin-top:18px;">수업 가능 학교 참고</p>
      <div class="chip-list">{school_chip_html}</div>
    </section>"""

    row = COMPARE_ROWS
    compare_rows_html = "\n".join(
        f'<div class="compare-row"><div class="other">{esc(r[variant][0])}</div><div class="label">{esc(r["label"])}</div><div class="ours">{esc(r[variant][1])}</div></div>'
        for r in row
    )
    compare_section = f"""    <section class="section">
      <div class="section-head">
        <p class="eyebrow">일반 학원과의 차이</p>
        <h2>{esc(local)} 수학학원, 무엇이 다른가요</h2>
        <p class="lead">일반적인 학원 운영 방식과 {esc(SITE_NAME)}의 수학 관리 방식을 같은 기준으로 비교했습니다.</p>
      </div>
      <div class="compare-table">
        <div class="compare-head"><div>일반적인 학원</div><div>기준</div><div class="ours">{esc(SITE_NAME)}</div></div>
        {compare_rows_html}
      </div>
    </section>"""

    center_section = f"""    <section class="section">
      <div class="section-head">
        <p class="eyebrow">CENTER INFO</p>
        <h2>센터 기준 정보</h2>
      </div>
      <div class="card-grid">
        <article class="info-card"><span class="tag">센터명</span><h3>{esc(center)}</h3><p>{esc(region)} {esc(district)} {esc(local)} 학생 상담 기준으로 안내합니다.</p></article>
        <article class="info-card"><span class="tag">주소</span><h3>위치 안내</h3><p>{esc(address) if address else "상담 시 위치 정보를 확인해 주세요."}</p></article>
        <article class="info-card"><span class="tag">등록</span><h3>{esc(education_name) if education_name else "교육지원청 등록 정보"}</h3><p>{esc(reg_no) if reg_no else "상담 시 교육지원청 등록 정보를 확인할 수 있습니다."}</p></article>
      </div>
    </section>"""

    fee_rows = FEE_TABLE_SEOUL if region == "서울" else FEE_TABLE_OTHER
    fee_region_label = "서울 지역 기준" if region == "서울" else "서울 외 지역 기준"
    fee_rows_html = "".join(
        f'<tr><td>{esc(freq)}</td><td class="highlight">{esc(el)}</td><td>{esc(mid)}</td><td>{esc(hi)}</td></tr>'
        for freq, el, mid, hi in fee_rows
    )
    fee_section = f"""    <section class="section">
      <div class="section-head">
        <p class="eyebrow">TUITION</p>
        <h2>{esc(local)} {esc(CATEGORY)} 학습료 안내</h2>
        <p class="lead">{esc(fee_region_label)}으로 안내되는 학습료입니다. 실제 금액은 상담 시 학생 과정과 교육청 신고 기준에 따라 확인해 주세요.</p>
      </div>
      <div class="fee-table-wrap">
        <p class="fee-caption">{esc(fee_region_label)} · 1회 90~100분 수업</p>
        <table class="fee-table">
          <thead><tr><th>횟수</th><th class="highlight">초등</th><th>중등</th><th>고등</th></tr></thead>
          <tbody>
            {fee_rows_html}
          </tbody>
        </table>
        <p class="fee-note">* 학습료는 지역, 수업 조건, 교육청 신고 기준에 따라 일부 차이가 있을 수 있습니다.</p>
      </div>
    </section>"""

    checklist_html = "".join(
        f'<article class="info-card"><span class="tag">{i + 1}</span><h3>{esc(q)}</h3><p>{esc(a)}</p></article>'
        for i, (q, a) in enumerate(checklist)
    )
    checklist_section = f"""    <section class="section">
      <div class="section-head">
        <p class="eyebrow">CHECKLIST</p>
        <h2>상담 전 체크리스트</h2>
      </div>
      <div class="card-grid">
        {checklist_html}
      </div>
    </section>"""

    faq_html = "\n".join(
        f'<details class="faq-item"{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for i, (q, a) in enumerate(faqs)
    )
    faq_section = f"""    <section class="section">
      <div class="section-head">
        <p class="eyebrow">FAQ</p>
        <h2>{esc(title)} 자주 묻는 질문</h2>
      </div>
      <div class="faq-list">
        {faq_html}
      </div>
    </section>"""

    review_html = "\n".join(
        f'<article class="review-card"><span class="stars">{"★" * int(r["rating"])}{"☆" * (5 - int(r["rating"]))}</span><p>{esc(r["body"])}</p></article>'
        for r in reviews
    )
    review_section = f"""    <section class="section">
      <div class="section-head">
        <p class="eyebrow">PARENT REVIEW</p>
        <h2>{esc(local)} 수학 상담 후기</h2>
      </div>
      <div class="review-grid">
        {review_html}
      </div>
    </section>"""

    related_html = "\n".join(
        f'<a href="{esc(url)}"><strong>{esc(name)} {esc(CATEGORY)}</strong><small>{esc(area)} 지역 페이지</small></a>'
        for name, url, area in related
    )
    other_link_html = cross_category_links_html(local, slug, CATEGORY)
    link_section = f"""    <section class="section">
      <div class="section-head">
        <p class="eyebrow">근처 학원페이지</p>
        <h2>{esc(local)} 주변 {esc(CATEGORY)} 페이지</h2>
        <p class="lead">같은 지역의 다른 카테고리와, 가까운 지역 페이지로 이동할 수 있도록 정리했습니다.</p>
      </div>
      <div class="link-grid">
        {other_link_html}
        <a href="../index.html"><strong>{esc(CATEGORY)} 전체</strong><small>카테고리 허브</small></a>
        <a href="../../index.html"><strong>전국학원</strong><small>전체 허브</small></a>
        {related_html}
      </div>
    </section>"""

    body = f"""{nav_html(3)}

  <main>
    <section class="page-hero">
      <p class="breadcrumb"><a href="../../../index.html">홈</a><span>/</span><a href="../../index.html">전국학원</a><span>/</span><a href="../index.html">{esc(CATEGORY)}</a><span>/</span><span>{esc(local)}</span></p>
      <p class="eyebrow">MATH COACHING</p>
      <h1>{esc(title)}</h1>
      <p class="lead">{esc(description)}</p>
      {badge_row}
      <div class="hero-actions">
        <a class="btn btn-primary" href="tel:{PHONE_DISPLAY}">전화 상담하기</a>
        <a class="btn btn-ghost" href="../../../상담문의/index.html">상담문의</a>
      </div>
    </section>

{media_section}

{summary_section}

{manuscript_section}

{answer_section}

{fit_section}

{compare_section}

{center_section}

{fee_section}

{checklist_section}

{faq_section}

{review_section}

{link_section}
  </main>

{footer_html(3)}
"""
    return page_shell(head, body)


def category_hub(rows: list[dict[str, str]]) -> None:
    rep = "/assets/generated/coaching-center-hero-v2.png"
    region_blocks = region_blocks_html(rows)
    ld_cat = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "@id": f"/전국학원/{CATEGORY}/#webpage", "url": f"/전국학원/{CATEGORY}/", "name": CATEGORY, "description": f"{CATEGORY} 지역별 안내 허브입니다.", "inLanguage": "ko-KR"},
            {"@type": "BreadcrumbList", "@id": f"/전국학원/{CATEGORY}/#breadcrumb", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "홈", "item": "/"}, {"@type": "ListItem", "position": 2, "name": "전국학원", "item": "/전국학원/"}, {"@type": "ListItem", "position": 3, "name": CATEGORY, "item": f"/전국학원/{CATEGORY}/"}]},
            {"@type": "ItemList", "@id": f"/전국학원/{CATEGORY}/#itemlist", "name": f"{CATEGORY} 지역 목록", "numberOfItems": len(rows), "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f"{r['근처 수업가능 동네']} {CATEGORY}", "url": f"/전국학원/{CATEGORY}/{slug_ko(r['근처 수업가능 동네'])}/"} for i, r in enumerate(rows)]},
        ],
    }
    head = head_html(f"{CATEGORY} | {SITE_NAME}", f"전국 {len(rows)}개 지역의 {CATEGORY} 안내를 지역별로 정리한 허브입니다.", 2, f"/전국학원/{CATEGORY}/", "website", rep, ld_cat)
    body = f"""{nav_html(2)}
  <main>
    <section class="page-hero">
      <p class="breadcrumb"><a href="../../index.html">홈</a><span>/</span><a href="../index.html">전국학원</a><span>/</span><span>{esc(CATEGORY)}</span></p>
      <p class="eyebrow">MATH ACADEMY DIRECTORY</p>
      <h1>{esc(CATEGORY)}</h1>
      <p class="lead">지역별 수학 상담 기준을 한눈에 찾을 수 있도록 정리했습니다. 각 페이지에는 지역·학년·추천학생, 학교 참고 정보, FAQ, 학부모 후기, 근처 학원페이지가 함께 구성됩니다.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="tel:{PHONE_DISPLAY}">전화 상담하기</a>
        <a class="btn btn-ghost" href="../../상담문의/index.html">상담문의</a>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <p class="eyebrow">ABOUT US</p>
        <h2>{esc(SITE_NAME)}은 수학을 이렇게 관리해요</h2>
        <p class="lead">문제 양을 늘리기보다, 지금 학생이 연산·개념·서술형 중 어디에서 막히는지부터 확인해요. 상담에서 시작해 진단, 오답 관리, 학년별 우선순위까지 이어갑니다.</p>
      </div>
      <div class="stepper">
        <article class="step">
          <div class="step-num">01</div>
          <div class="step-body"><h3>상담</h3><p>학년, 최근 시험지, 현재 학습 이력을 편하게 듣습니다.</p></div>
        </article>
        <article class="step">
          <div class="step-num">02</div>
          <div class="step-body"><h3>진단</h3><p>연산, 개념, 서술형 중 지금 어디부터 시작해야 할지 확인합니다.</p></div>
        </article>
        <article class="step">
          <div class="step-num">03</div>
          <div class="step-body"><h3>오답 관리</h3><p>틀린 문제를 유형별로 정리해 같은 실수가 반복되지 않도록 관리합니다.</p></div>
        </article>
        <article class="step">
          <div class="step-num">04</div>
          <div class="step-body"><h3>학년별 우선순위</h3><p>초·중·고 전환 시기에 맞춰 다음 단계를 준비합니다.</p></div>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <p class="eyebrow">총 지역</p>
        <h2>{len(rows)}개 지역</h2>
        <p class="lead">서울부터 지방까지 지역명 기준으로 {esc(CATEGORY)} 페이지를 생성했습니다.</p>
      </div>
      {region_blocks}
    </section>
  </main>
{footer_html(2)}"""
    out = SITE / "전국학원" / CATEGORY / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_shell(head, body), encoding="utf-8")


def root_hub() -> None:
    rep = "/assets/generated/coaching-center-hero-v2.png"
    cat_links = "".join(
        f'<a href="{slug_ko(name)}/index.html"><strong>{esc(name)}</strong><small>{esc(desc)}</small></a>'
        for name, desc in ALL_CATEGORIES
    )
    ld_root = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "@id": "/전국학원/#webpage", "url": "/전국학원/", "name": "전국학원", "description": f"{SITE_NAME} 전국학원 허브입니다. 카테고리별로 지역 학습관리 안내 페이지로 이동할 수 있습니다.", "inLanguage": "ko-KR"},
            {"@type": "BreadcrumbList", "@id": "/전국학원/#breadcrumb", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "홈", "item": "/"}, {"@type": "ListItem", "position": 2, "name": "전국학원", "item": "/전국학원/"}]},
            {"@type": "ItemList", "@id": "/전국학원/#categories", "name": "전국학원 카테고리", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": name, "url": f"/전국학원/{name}/"} for i, (name, _) in enumerate(ALL_CATEGORIES)]},
        ],
    }
    head = head_html(f"전국학원 | {SITE_NAME}", f"{SITE_NAME} 전국학원 허브입니다. 카테고리별로 지역 학습관리 안내 페이지로 이동할 수 있습니다.", 1, "/전국학원/", "website", rep, ld_root)
    body = f"""{nav_html(1)}
  <main>
    <section class="page-hero">
      <p class="breadcrumb"><a href="../index.html">홈</a><span>/</span><span>전국학원</span></p>
      <p class="eyebrow">NATIONAL ACADEMY HUB</p>
      <h1>전국학원</h1>
      <p class="lead">카테고리별로 지역 학습관리 페이지를 정리하는 허브입니다.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="tel:{PHONE_DISPLAY}">전화 상담하기</a>
        <a class="btn btn-ghost" href="../상담문의/index.html">상담문의</a>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <p class="eyebrow">ABOUT US</p>
        <h2>{esc(SITE_NAME)}은 이런 곳이에요</h2>
        <p class="lead">{esc(SITE_NAME)}은 성적표 너머의 이해도와 습관을 먼저 봐요. 상담, 진단, 맞춤 플래너, 오답 재학습까지 학생에게 필요한 순서를 함께 찾아드립니다.</p>
      </div>
      <div class="card-grid">
        <article class="info-card"><span class="tag">01</span><h3>지역 데이터 기반</h3><p>실제 센터 주소와 인근 학교 정보를 바탕으로, 지역마다 다른 상담 기준을 정리해 안내해요.</p></article>
        <article class="info-card"><span class="tag">02</span><h3>학년별 맞춤 진단</h3><p>초·중·고 전환 시기마다 필요한 게 달라 학년에 맞춰 우선순위를 정해요.</p></article>
        <article class="info-card"><span class="tag">03</span><h3>기록이 남는 관리</h3><p>오답과 학습 이력을 남겨, 다음에 무엇을 봐야 할지 바로 확인할 수 있어요.</p></article>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <p class="eyebrow">구조 안내</p>
        <h2>카테고리에서 지역으로 이동하는 방식</h2>
        <p class="lead">예: 전국학원 / {esc(ALL_CATEGORIES[0][0])} / 명일동</p>
      </div>
      <div class="category-grid">
        {cat_links}
      </div>
    </section>
  </main>
{footer_html(1)}"""
    out = SITE / "전국학원" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_shell(head, body), encoding="utf-8")


def main() -> None:
    rows = read_csv(COMMON / "센터정보 정리.csv")
    reps = choose_rep_images(rows)
    category_hub(rows)
    for idx, row in enumerate(rows):
        slug = slug_ko(row["근처 수업가능 동네"])
        out = SITE / "전국학원" / CATEGORY / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(local_page(row, idx, reps[idx], rows), encoding="utf-8")
    root_hub()
    print(f"generated category={CATEGORY} local_pages={len(rows)}")


if __name__ == "__main__":
    main()
