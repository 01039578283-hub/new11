from __future__ import annotations

import random

import generate_math_academy_pages as shared

SITE = shared.SITE
COMMON = shared.COMMON
SITE_NAME = shared.SITE_NAME
PHONE_DISPLAY = shared.PHONE_DISPLAY
PHONE_LINK = shared.PHONE_LINK
PUBLISH_DATE = shared.PUBLISH_DATE
CATEGORY = "영수학원"

ALL_CATEGORIES = shared.ALL_CATEGORIES
cross_category_links_html = shared.cross_category_links_html

esc = shared.esc
slug_ko = shared.slug_ko
split_items = shared.split_items
seed_for = shared.seed_for
school_type = shared.school_type
eul_reul = shared.eul_reul
eun_neun = shared.eun_neun
nav_html = shared.nav_html
footer_html = shared.footer_html
head_html = shared.head_html
page_shell = shared.page_shell
find_map = shared.find_map
pick = shared.pick
fmt_pair = shared.fmt_pair
school_names = shared.school_names
region_blocks_html = shared.region_blocks_html
FEE_TABLE_SEOUL = shared.FEE_TABLE_SEOUL
FEE_TABLE_OTHER = shared.FEE_TABLE_OTHER


# ---------------------------------------------------------------------------
# content banks (freshly written for 온담학습 / 영수학원 — this category spans
# all grade levels (초등~고등), themed around 영어 어휘·독해·문제풀이와 수학 개념·풀이·듣기말하기·서술형·서술형.
# Informed by 상담방식.txt, FAQ.txt (영어 관련 문항), 학부모 후기.txt,
# 경쟁사분석, and "영수학원 원고.xlsx" (themes reused, wording rewritten,
# not copied verbatim). Verified 0 string overlap with 수학학원 banks.
# ---------------------------------------------------------------------------

FAQ_OPENER_BANK: list[tuple[str, str]] = [
    ("{title}은 초등 몇 학년부터 다닐 수 있나요?",
     "초등학생부터 고등학생까지 학년과 목표에 맞춰 진단 방식을 다르게 상담해 드립니다."),
    ("{title}에서는 처음부터 영어 문법·수학 개념을 배우나요?",
     "학생의 현재 영어 이해도와 수학 개념 수준에 따라 영어 문법·수학 개념부터 시작할 수도, 독해·문제풀이 위주로 진행할 수도 있습니다."),
    ("{title}은 몇 명이 함께 수업받나요?",
     "선생님이 학생 개개인의 이해도를 확인할 수 있는 인원으로 반을 구성합니다."),
    ("{title} 상담 전에 따로 준비해야 할 것이 있나요?",
     "특별히 준비하실 것은 없습니다. 최근 영어 시험지나 학습 이력이 있으면 참고가 됩니다."),
    ("{title}은 원어민 수업도 있나요?",
     "지점별 운영 방식에 따라 다를 수 있어 상담 시 자세히 안내해 드립니다."),
    ("{title}에 등록하기 전에 실력 진단이 꼭 필요한가요?",
     "필수는 아니지만, 학생의 현재 영어 이해도와 수학 개념 수준을 파악하는 데 도움이 됩니다."),
]

FAQ_BANK: list[tuple[str, str]] = [
    ("서술형(영작) 문제를 어려워하는 학생은 어떻게 지도하나요?",
     "짧은 문장부터 스스로 완성하는 연습을 반복해 서술형에 대한 부담을 줄여갑니다."),
    ("영어 단어 암기와 수학 개념 복습을 힘들어하는 학생은 어떻게 지도하나요?",
     "한 번에 많이 외우기보다 문장 속에서 반복해서 만나게 해 자연스럽게 익히도록 돕습니다."),
    ("영어 듣기·말하기와 수학 서술형도 함께 챙겨주나요?",
     "영어는 듣고 말하는 연습을 병행하고, 수학은 풀이 과정을 말과 글로 설명하는 서술형 연습을 함께 진행합니다."),
    ("영어와 수학을 처음부터 잡아야 하는 학생도 수업이 가능한가요?",
     "네, 영어는 기초 어휘와 문장 구조부터, 수학은 연산과 개념부터 차근차근 시작하며 부담 없이 적응하도록 진행합니다."),
    ("{local}에서 다니는 학교의 영어 진도와 맞춰주나요?",
     "학교 진도를 참고하되, 학생의 실제 이해 수준에 맞춰 학습 순서를 조정합니다."),
    ("숙제량은 얼마나 되나요?",
     "학년과 진도에 맞춰 영어 단어 암기, 수학 개념 복습, 독해·문제풀이 과제 위주로 부담이 크지 않은 선에서 나갑니다."),
    ("영어와 수학을 지루해하는 학생도 흥미를 붙일 수 있을까요?",
     "쉬운 지문부터 단계적으로 접근해 성취감을 자주 느끼도록 수업을 구성합니다."),
    ("고등학교 영어·수학을 대비해 지금부터 무엇을 준비해야 하나요?",
     "현재 학년 영어 이해도와 수학 개념력이 탄탄한지 먼저 확인한 뒤, 필요한 심화를 단계적으로 진행합니다."),
    ("영어 단어는 아는데 독해가 막히거나, 수학 개념은 아는데 문제풀이가 막힌다면?",
     "영어는 문장을 끊어 읽는 연습이, 수학은 조건을 식으로 옮기는 연습이 필요합니다."),
    ("혼자 공부하다가 학원을 고민 중이라면 어떻게 해야 하나요?",
     "스스로 채점만 하면 놓치는 오답 원인이 많아, 함께 짚어드리는 과정이 필요합니다."),
    ("레벨테스트에서 영어 어휘력과 수학 개념 이해도가 약하게 나오면 어떻게 하나요?",
     "기초 어휘부터 단계적으로 채워가는 계획을 세워 안내해 드립니다."),
    ("고등학생인데 지금부터 시작해도 따라갈 수 있을까요?",
     "가능합니다. 지금 부족한 부분부터 우선순위를 정해 채워가면 충분히 따라갈 수 있습니다."),
    ("수능형 독해·문제풀이와 내신 대비를 함께 할 수 있나요?",
     "학년과 목표에 따라 내신과 수능형 지문의 비중을 조정해 함께 준비합니다."),
    ("다른 학원에서 옮기는데 진도가 다르면 어떻게 되나요?",
     "다니던 학원의 진도와 교재를 확인한 뒤, 지금 실력에 맞춰 시작 지점을 새로 정해 드립니다."),
    ("영어 문법과 수학 개념 용어를 어려워하는 학생은 어떻게 지도하나요?",
     "용어만 외우기보다 영어는 예문으로, 수학은 대표 문제로 개념이 적용되는 과정을 반복해 보여줍니다."),
    ("영어 표현과 수학 서술형이 모두 걱정되는 학생도 괜찮을까요?",
     "영어는 짧은 문장 표현부터, 수학은 풀이 과정을 설명하는 연습부터 부담 없이 시작합니다."),
    ("{title}은 시험 기간에 수업 방식이 달라지나요?",
     "학교별 시험 범위에 맞춰 영어 문법·수학 개념·독해·문제풀이 정리와 예상 문제 위주로 수업을 재구성합니다."),
    ("틀린 문제는 따로 정리해 주시나요?",
     "틀린 문제를 영어 문법·수학 개념·독해·문제풀이·어휘 유형별로 정리해 다시 풀어볼 수 있도록 관리합니다."),
]

ANSWER_BANK: list[tuple[str, str]] = [
    ("학생이 단어는 아는데 문장 해석이 안 된다면?",
     "단어 뜻과 문장 속 쓰임은 다른 문제입니다. 영어는 문장을 끊어 읽고, 수학은 조건을 정리하는 연습이 도움이 됩니다."),
    ("영어 문법·수학 개념은 아는 것 같은데 독해·문제풀이에서 적용을 못한다면?",
     "규칙을 아는 것과 문장에 적용하는 것은 다른 능력입니다. 예문으로 연결하는 훈련이 필요합니다."),
    ("영수학원을 옮겨도 실력이 그대로인 것 같다면?",
     "영어 단어량이나 수학 문제량만 늘리는 것으로는 부족할 수 있습니다. 지금 어디서 막히는지부터 다시 확인하는 것이 먼저입니다."),
    ("듣기는 곧잘 하는데 말하기를 부끄러워한다면?",
     "실수해도 괜찮은 분위기에서 짧은 문장부터 소리 내어 말해보는 연습을 반복하면 점차 편해집니다."),
    ("고등학교 입학을 앞두고 무엇부터 챙겨야 할지 막막하다면?",
     "현재 학년 영어 이해도와 수학 개념력이 잘 다져져 있는지 먼저 점검하고, 다음 단계에 필요한 학습 습관을 단계적으로 준비합니다."),
    ("혼자 문제집만 풀다가 학원을 고민 중이라면?",
     "혼자 채점만 해서는 무엇을 놓쳤는지 알기 어려워, 함께 원인을 확인하는 과정이 필요합니다."),
    ("영어·수학 자신감이 없어 보이는 학생이라면?",
     "부담이 적은 단계부터 성취를 반복 경험하게 해 자신감을 천천히 쌓아가는 것이 중요합니다."),
    ("영수학원을 고를 때 가장 먼저 볼 기준은?",
     "화려한 커리큘럼보다 학생이 지금 어디서 막히는지 구체적으로 확인해 주는지를 먼저 보시는 것이 좋습니다."),
    ("고등 영어·수학을 고민 중인데 지금부터 무엇을 챙겨야 할까요?",
     "영어 이해도와 수학 개념의 기초 체력을 먼저 다지고, 이후 실전 유형을 단계적으로 늘려가는 순서를 권합니다."),
    ("나이 차이가 있는 형제자매를 함께 등록해도 괜찮을까요?",
     "학년과 실력 차이가 있으면 각자 다른 단원을 배우게 되므로, 개별로 진단한 뒤 맞춤 계획을 따로 안내해 드립니다."),
]

CHECKLIST_BANK: list[tuple[str, str]] = [
    ("영어 독해와 수학 풀이 수준", "학년에 맞는 핵심 영어 이해도와 수학 개념력을 어느 정도 갖추고 있는지 살펴봅니다."),
    ("직전 성적표", "몇 점을 받았는지보다 어떤 문항에서 반복해 틀렸는지가 더 중요합니다."),
    ("다니는 학교 진도", "{local} 학생이 배우는 학교 교재와 시험 출제 방식을 참고합니다."),
    ("오답 관리 방식", "지금까지 틀린 문제를 어떻게 다시 봐왔는지 여쭤봅니다."),
    ("듣기·말하기 수준", "발음과 억양, 짧은 대화 이해 수준을 확인합니다."),
    ("현재 다니는 학원·교재", "지금 사용 중인 교재와 진도를 알려주시면 시작점을 잡기 쉽습니다."),
    ("목표 시험", "내신, 수능, 어학 시험 등 지금 우선순위를 정합니다."),
    ("연락 가능 시간", "평소 통화나 상담이 편하신 시간을 미리 알려주세요."),
]

REVIEW_BANK: list[str] = [
    "영어와 수학을 따로따로 보지 않고 아이의 약한 과목부터 순서를 잡아줘서 도움이 됐습니다.",
    "영어 단어는 잘 외우는데 수학 풀이가 약한 아이였는데, 두 과목을 함께 점검해 주니 흐름이 보였습니다.",
    "시험 기간에 영어 범위와 수학 단원을 같이 정리해 주셔서 계획 세우기가 훨씬 편했습니다.",
    "수학 오답과 영어 독해 실수를 한 번에 확인해 주니 아이가 무엇을 고쳐야 하는지 이해하더라고요.",
    "영어는 문장 해석, 수학은 풀이 과정 설명까지 같이 봐주셔서 학습 태도가 안정됐습니다.",
    "과목별 숙제량을 무리하게 늘리지 않고 아이가 해낼 수 있는 분량으로 조절해 주셔서 좋았습니다.",
    "영어와 수학을 모두 어려워하던 아이가 작은 단위로 성공 경험을 쌓으면서 자신감을 되찾았습니다.",
    "상담 때 두 과목의 현재 위치를 분리해서 설명해 주셔서 어떤 과목부터 잡아야 할지 알 수 있었습니다.",
    "학교 시험 범위에 맞춰 영어 문법과 수학 개념을 같이 정리해 주셔서 시험 준비가 덜 흔들렸습니다.",
    "문제만 많이 푸는 방식이 아니라, 영어는 해석 근거를, 수학은 풀이 이유를 말하게 해주셔서 만족합니다.",
    "아이가 집에서 공부할 때 영어와 수학 중 무엇부터 해야 할지 몰라했는데 플래너가 생겨 편해졌습니다.",
    "영어 단어 체크와 수학 오답 복습이 같이 돌아가니 학습 리듬이 훨씬 규칙적으로 잡혔습니다.",
    "두 과목을 같이 상담받을 수 있어서 학부모 입장에서도 아이 상태를 한 번에 파악하기 좋았습니다.",
    "영어 독해는 천천히 끊어 읽고, 수학은 조건을 정리하는 방식으로 지도해 주셔서 이해가 쉬웠다고 합니다.",
    "수업 후 아이가 영어와 수학에서 각각 무엇을 복습해야 하는지 말할 수 있게 된 점이 가장 좋았습니다.",
    "고등 대비를 고민했는데 영어 어휘와 수학 개념 중 먼저 채울 부분을 알려주셔서 방향이 잡혔습니다.",
    "소수로 진행되어 질문하기 편했고, 영어와 수학 질문을 같은 흐름에서 정리해 주셔서 좋았습니다.",
    "틀린 문제를 그냥 넘기지 않고 영어·수학 실수 유형을 따로 기록해 주셔서 반복 실수가 줄었습니다.",
    "학원을 옮기기 전 진도 차이가 걱정됐는데 두 과목 모두 시작 지점을 다시 잡아주셔서 안심했습니다.",
    "영어는 단어만, 수학은 문제만 시키는 느낌이 아니라 아이에게 필요한 이유를 설명해 주는 수업이었습니다.",
    "중간고사 전에는 영어 본문과 수학 단원을 같이 묶어 계획을 세워주셔서 관리가 촘촘했습니다.",
    "아이가 수학 풀이를 말로 설명하고 영어 문장을 직접 끊어 읽는 연습을 하면서 태도가 달라졌습니다.",
    "상담이 과장되지 않고 현실적인 편이라, 아이에게 필요한 영어·수학 보완점을 차분히 볼 수 있었습니다.",
    "처음에는 두 과목을 같이 하는 게 부담스러울까 걱정했는데, 오히려 우선순위를 잡아줘서 편해졌습니다.",
    "영어와 수학을 한꺼번에 챙기되 과목별 약점은 따로 봐주셔서 균형감 있게 느껴졌습니다.",
    "학년이 올라가기 전에 영어 독해와 수학 개념을 같이 점검할 수 있어 마음이 놓였습니다.",
    "아이에게 맞는 속도로 진행되어 두 과목 모두 부담이 덜하다고 말합니다.",
    "복습해야 할 영어 단어와 다시 풀어야 할 수학 문제를 구분해 주니 집에서도 관리하기 쉬웠습니다.",
    "성적만 보고 판단하지 않고 공부 습관과 과목별 이해도를 함께 봐주셔서 믿음이 갔습니다.",
    "영어와 수학의 약점이 서로 다르다는 걸 상담에서 자세히 설명해 주셔서 도움이 됐습니다.",
]

COMPARE_ROWS: list[dict[str, tuple[str, str]]] = [
    {"label": "실력 진단", "A": ("나이만 보고 반 배정", "영어 독해와 수학 풀이 수준부터 확인"),
     "B": ("점수만 보고 끝", "어디서 막혔는지 구체적으로 확인")},
    {"label": "영어 문법·수학 개념 지도", "A": ("용어 암기 위주", "예문으로 규칙 적용 훈련"),
     "B": ("한 번 설명하고 넘어감", "이해될 때까지 반복 설명")},
    {"label": "표현·서술형 훈련", "A": ("풀이 결과만 확인", "영어 표현과 수학 풀이 설명까지 진행"),
     "B": ("설명 연습이 부족함", "짧은 문장 표현과 풀이 설명을 함께 연습")},
    {"label": "가정 안내", "A": ("결과만 통보하고 끝", "이해도·태도 변화까지 설명"),
     "B": ("정해진 주기로만 연락", "궁금할 때 바로 상담 가능")},
]

SUMMARY_INTROS: list[str] = [
    "{local} 학생에게 필요한 영어·수학 통합관리는 단어량을 늘리는 것보다 지금 영어 이해도와 수학 개념 중 어디가 부족한지 먼저 확인하는 것입니다.",
    "{local}에서 영수학원을 고르실 때는 영어 어휘·독해·문제풀이와 수학 개념·풀이 중 지금 필요한 부분이 무엇인지부터 살펴보시는 것이 좋습니다.",
    "{local} 학생마다 영어와 수학을 어려워하는 지점과 학년별 목표가 다르기 때문에, 같은 학년이라도 먼저 봐야 할 부분은 달라질 수 있습니다.",
]

MANUSCRIPT_INTRO: list[str] = [
    "영어는 학년이 올라갈수록 영어 이해도와 수학 개념의 기초가 다음 단계의 영어 문법·수학 개념과 서술형까지 영향을 미칩니다. 지금 단계에서 부족한 부분을 채우지 않으면 다음 학년에서 계속 부담이 쌓일 수 있습니다.",
    "영어는 단어를 아는 것에서 문장 해석으로, 수학은 개념을 아는 것에서 풀이 적용으로 넘어가는 과정이 필요합니다.",
    "말하기를 부끄러워하는 학생일수록 실수해도 괜찮은 분위기에서 반복해서 소리 내어 말해보는 연습이 중요합니다.",
    "고등 영어는 중등 영어의 영어 이해도와 수학 개념 기초 위에 세워집니다. 지금 어휘와 문장 구조를 다져두면 이후 심화 지문을 배울 때 훨씬 수월해집니다.",
    "학생마다 영어에서 막히는 지점이 다릅니다. 어휘인지, 영어 문법·수학 개념인지, 독해·문제풀이인지부터 구분하면 훨씬 효율적으로 도울 수 있습니다.",
    "영어 문법·수학 개념·독해·문제풀이·어휘 중 어디서 실수가 반복되는지 나누어 살펴보면, 막연히 문제를 더 푸는 것보다 훨씬 효율적으로 개선할 수 있습니다.",
]

MANUSCRIPT_OUTRO: list[str] = [
    "학원을 고르실 때는 화려한 커리큘럼보다, 학생의 현재 영어 이해도와 수학 개념 수준을 얼마나 구체적으로 봐주는지를 기준으로 삼으시길 권합니다.",
    "영어는 스스로 문장을 해석할 수 있는지, 수학은 풀이 과정을 설명할 수 있는지를 함께 확인하는 것이 중요합니다.",
    "상담에서는 곧바로 결정하지 않으셔도 됩니다. 지금 학생에게 필요한 방향을 먼저 편하게 들어보시길 권합니다.",
    "영어·수학 학습은 한 번에 완성되지 않습니다. 영어 어휘·독해·문제풀이와 수학 개념·풀이를 오가며 조금씩 쌓아가는 과정이라는 점을 기억해 주세요.",
    "무엇보다 학생이 영어를 부담스러워하지 않는지가 꾸준한 학습으로 이어지는 데 가장 중요합니다.",
    "지금 당장의 영어 단어와 수학 개념 점검 점수보다, 스스로 문장을 해석해 보려는 습관이 자리 잡고 있는지를 함께 지켜봐 주시길 바랍니다.",
]


def local_page(row: dict[str, str], idx: int, rep_image: str, all_rows: list[dict[str, str]]) -> str:
    local = row["근처 수업가능 동네"].strip()
    slug = slug_ko(local)
    region = row.get("지역", "").strip()
    district = row.get("시or구", "").strip()
    center = row.get("센터명", "").strip() or f"{local} 학습관리"
    address = row.get("센터 주소", "").strip()
    title = f"{local} {CATEGORY}"
    description = f"{region} {district} {local} 학생을 위한 {CATEGORY} 안내입니다. 영어 어휘·독해·문제풀이와 수학 개념·풀이 진단, 오답 관리, 학년별 학습 우선순위를 상담 전에 확인할 수 있습니다."
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

    opener = fmt_pair(pick(FAQ_OPENER_BANK, 1, local, "ea-faq-opener")[0],
                       local=local, district=district, title=title, region=region)
    faqs = [opener] + [fmt_pair(p, local=local, district=district, title=title, region=region)
                        for p in pick(FAQ_BANK, 5, local, "ea-faq")]
    answers = [fmt_pair(p, local=local, district=district, title=title, region=region)
               for p in pick(ANSWER_BANK, 4, local, "ea-answer")]
    checklist = [fmt_pair(p, local=local, district=district, title=title, region=region)
                 for p in pick(CHECKLIST_BANK, 4, local, "ea-checklist")]
    review_lines = pick(REVIEW_BANK, 6, local, "ea-review", str(idx))
    summary_intro = pick(SUMMARY_INTROS, 1, local, "ea-summary")[0].format(local=local)
    manu_intro = pick(MANUSCRIPT_INTRO, 1, local, "ea-manu-intro")[0]
    manu_outro = pick(MANUSCRIPT_OUTRO, 1, local, "ea-manu-outro")[0]
    location_ref = address if address else "상담 시 안내되는 위치"
    variant = "A" if seed_for(local, "ea-compare") % 2 == 0 else "B"

    rng = random.Random(seed_for(local, "ea-review-rating"))
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
        {"@type": "Thing", "name": "영수학원"},
        {"@type": "Thing", "name": "어휘"},
        {"@type": "Thing", "name": "영어 문법·수학 개념"},
        {"@type": "Thing", "name": "독해·문제풀이"},
        {"@type": "Thing", "name": "듣기 말하기"},
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
                "alternateName": [SITE_NAME, center, f"{local} 영어·수학 학습관리"],
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
                "knowsAbout": ["어휘", "영어 문법·수학 개념", "독해·문제풀이", "듣기 말하기", "학습 습관 관리", "학습 상담"],
                "makesOffer": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"{local} 영어 진단 상담", "serviceType": "TutoringService"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"{local} 어휘·영어 문법·수학 개념 관리", "serviceType": "TutoringService"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"{local} 독해·문제풀이·듣기말하기·서술형 관리", "serviceType": "TutoringService"}},
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
                "description": f"{local} 학생의 영어 어휘·독해·문제풀이와 수학 개념·풀이, 듣기·말하기와 수학 서술형을 함께 진단하고 학년별 우선순위에 맞춰 관리합니다.",
                "provider": {"@id": org_id},
                "areaServed": {"@type": "Place", "name": local},
                "audience": {"@type": "EducationalAudience", "educationalRole": "student"},
                "about": about,
                "mentions": mentions,
                "makesOffer": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"{local} 어휘·영어 문법·수학 개념 진단"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"{local} 독해·문제풀이 관리"}},
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"{local} 듣기말하기·서술형 관리"}},
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

    badge_row = f'<div class="badge-row"><span>{esc(region)}</span><span>{esc(district)}</span><span>{esc(CATEGORY)}</span><span>영어 어휘·독해·문제풀이와 수학 개념·풀이</span></div>'

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
        <article class="info-card"><span class="tag">01</span><h3>어휘·독해·문제풀이 진단</h3><p>영어 어휘력과 수학 개념 이해도, 영어 문법·수학 개념 적용, 독해·문제풀이 중 지금 어디가 부족한지 먼저 나누어 확인합니다.</p></article>
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
        <article class="info-card"><span class="tag">지역</span><h3>{esc(region)} {esc(district)} {esc(local)}</h3><p>{esc(local)} 생활권 학생의 학교 진도와 눈높이에 맞춰 영어·수학 통합관리 방향을 상담합니다.</p></article>
        <article class="info-card"><span class="tag">학년</span><h3>초1~고3, 전 학년 상담 가능</h3><p>학년과 목표에 따라 영어 어휘·독해·문제풀이와 수학 개념·풀이 중 시작 지점을 다르게 잡습니다.</p></article>
        <article class="info-card"><span class="tag">추천</span><h3>이런 학생에게 추천</h3><p>단어는 아는데 독해·문제풀이가 약한 학생, 영어 문법·수학 개념을 적용하지 못하는 학생, 영어와 수학을 기초부터 잡아야 하는 학생에게 적합합니다.</p></article>
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
        <h2>{esc(local)} 영수학원, 무엇이 다른가요</h2>
        <p class="lead">일반적인 학원 운영 방식과 {esc(SITE_NAME)}의 영어와 수학을 함께 보는 통합관리 방식을 같은 기준으로 비교했습니다.</p>
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
        <h2>{esc(local)} 영수 상담 후기</h2>
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
      <p class="eyebrow">ENGLISH & MATH COACHING</p>
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
    rep = "/assets/generated/site6-hero.png"
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
      <p class="eyebrow">ENGLISH & MATH ACADEMY DIRECTORY</p>
      <h1>{esc(CATEGORY)}</h1>
      <p class="lead">지역별 영수 상담 기준을 한눈에 찾을 수 있도록 정리했습니다. 각 페이지에는 지역·학년·추천학생, 학교 참고 정보, FAQ, 학부모 후기, 근처 학원페이지가 함께 구성됩니다.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="tel:{PHONE_DISPLAY}">전화 상담하기</a>
        <a class="btn btn-ghost" href="../../상담문의/index.html">상담문의</a>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <p class="eyebrow">ABOUT US</p>
        <h2>{esc(SITE_NAME)}은 영어와 수학을 함께 관리해요</h2>
        <p class="lead">영어 단어량이나 수학 문제량만 늘리기보다, 지금 학생이 영어 어휘·독해·문제풀이와 수학 개념·풀이 중 어디에서 막히는지부터 확인해요. 상담에서 시작해 진단, 오답 관리, 학년별 우선순위까지 이어갑니다.</p>
      </div>
      <div class="stepper">
        <article class="step">
          <div class="step-num">01</div>
          <div class="step-body"><h3>상담</h3><p>학년, 최근 시험지, 현재 학습 이력을 편하게 듣습니다.</p></div>
        </article>
        <article class="step">
          <div class="step-num">02</div>
          <div class="step-body"><h3>진단</h3><p>영어 어휘·독해·문제풀이와 수학 개념·풀이 중 지금 어디부터 시작해야 할지 확인합니다.</p></div>
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


def main() -> None:
    rows = shared.read_csv(COMMON / "센터정보 정리.csv")
    reps = shared.choose_rep_images(rows)
    category_hub(rows)
    for idx, row in enumerate(rows):
        slug = slug_ko(row["근처 수업가능 동네"])
        out = SITE / "전국학원" / CATEGORY / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(local_page(row, idx, reps[idx], rows), encoding="utf-8")
    shared.root_hub()
    print(f"generated category={CATEGORY} local_pages={len(rows)}")


if __name__ == "__main__":
    main()
