from __future__ import annotations

import html
import json
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path


SITE = Path(__file__).resolve().parents[1]
CATEGORIES = ("고등영어학원", "고등수학학원", "중등수학학원", "중등영어학원", "초4수학학원", "초4영어학원", "초5수학학원", "초5영어학원")
CATEGORY_LABELS = {
    "고등영어학원": "고등 영어학원",
    "고등수학학원": "고등 수학학원",
    "중등수학학원": "중등 수학학원",
    "중등영어학원": "중등 영어학원",
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
    "설명용 유형",
    "실제 수강생",
    "입력만으로",
    "데이터에 없",
    "이 글에서 임의",
    "확인할 수 있는지 확인",
    "방법도 있다는 점도",
    "다음으로 이때",
    "중등 수학학원을 찾는 학부모라면 중등 수학학원을",
    "수업을 비교한다면 중등 수학학원을 비교할 때",
    "상담이라면 중등 수학학원을 비교할 때",
    "오현초호매실중",
)
MIDDLE_MATH_BANNED = (
    "경우라는 상황에는",
    "경우라는 고민",
    "필요하다는 사실을 기준으로 삼아야",
    "의미가 달라지는지를 기록해 둘 수 있습니다",
    "충청 새롬중앙로",
    "막힌 단계로 돌아갈 수 있는 편이 좋습니다",
    "돌아갈 수 있을 필요가 있습니다",
    "준비할 수 있도록 준비할 필요가 있습니다",
    "답변을 기록한 뒤 기록해 두세요",
    "상담 전에는 상담 뒤에는",
    "흐름이 필요가 있습니다",
    "질문하면 되는지를 질문해 볼 수 있습니다",
    "옮겨도 될 수 있습니다",
    "우선 그다음",
    "질문할 수 있는지 확인해 보세요",
    "결정 전에는 상담 뒤에는",
    "그다음 이 상태",
    "질문하면 될 수 있습니다",
    "질문하면 된다는 점도",
    "질문하는 편이 구체적",
    "된다는 사실을 기준으로 삼을 수 있습니다",
    "확인할 수 있도록 준비할 필요가 있습니다",
    "질문할 수 있도록 질문을 정리해 보세요",
    "확인할 수 있도록 질문을 정리해 보세요",
    "나눌 수 있도록 질문을 정리해 보세요",
    "나눌 수 있도록 순서를 정해 보세요",
    "나눌 수 있도록 준비할 필요가 있습니다",
    "상담 전에는 현재 상태에는",
    "상황에 따라 예를 들어",
    "구체적으로는 이때",
    "다만 필요하다면",
    "답변을 기록하며 질문을 정리하세요",
    "방법도 있는지를 질문해 볼 수 있습니다",
    "가정에서는 상담 뒤에는",
    "예를 들면 필요하다면",
    "이 안내가 사용하는 지역 범위는",
    "적어 본 뒤 기록해 두세요",
    "기초 확인 범위와 피드백 방법을 구체적인 질문을 준비하는 편이 좋습니다",
    "상담 전에는 중등 수학에서는",
    "비교할 때에는 중등 수학에서는",
    "비교할 때에는 상담 뒤에는",
    "가정에서는 현재 상태에는",
    "편이 한 방법입니다",
    "편이 권할 만합니다",
    "편이 확인 기준으로 쓰기 좋습니다",
    "나누면 한 방법입니다",
    "나누면 권할 만합니다",
    "나누면 확인 기준으로 쓰기 좋습니다",
    "것이 권할 만합니다",
    "것이 확인 기준으로 쓰기 좋습니다",
    "될 수 있는 조건을 살펴야 합니다",
    "되는 이유를 함께 확인해야 합니다",
    "혼자 풀 수 있는 범위와 도움을 받아야 하는 범위를 나누는 질문부터 시작할 수",
    "그다음에는 이 상태를 어떤 방식으로 진단하고 학습 계획에 반영하는지 질문하면",
    "https://naver",
    "맞은편또는",
    "옆에있습니다",
    "건물4층",
    "첫번째",
    "별도 질문으로 남깁니다",
    "상담 자료가 된다는 점을 기록해 둘 수 있습니다",
    "상담 자료가 되는지 확인해 볼 필요가 있습니다",
    "질문할 수 있으니 학생 상태에 맞게 적용해 보세요",
    "나눌 수 있으니 학생 상태에 맞게 적용해 보세요",
    "다음 진도 전에 과제량을 늘리기 전에",
    "구체적인 사실을 추정하지 말고",
    "안내에 없는 정보이므로",
    "학교 진도와 현재 약점의 순서를 나누어",
    "함께 확인한 뒤 다시 확인",
    "물어본 뒤 기록해 두세요",
    "기록을 토대로 틀린 문제를 계산·개념·조건 해석으로 나누어 기록합니다",
    "학생 상태에 맞게 적용해 보세요",
    "질문할 수 있는 조건을 확인",
    "준비할 수 있는 조건을 확인",
    "방법도 있다는 점",
    "점을 함께 살펴야 합니다",
    "할 수 있도록 질문을 정리",
    "실제 계획은",
    "상담 자료가 된다는 점",
    "## ",
    "설명 뒤 독립 작성한 풀이",
    "왜 그 작성한 풀이",
    "확인할 우선순위는 점수표 하나가 아니라",
    "구체적으로는 부족한 부분은",
    "눈으로 확인할 수 있는 항목을 정할 수",
    "되는 흐름을 확인해 보세요",
    "되는 과정을 살펴보는 것이 좋습니다",
    "의미가 달라질 수 있는 조건을 확인해야 합니다",
    "의미가 달라지는지를 기록",
    "충북북도",
    "충남남도",
    "경북북도",
    "전북북도",
    "전남남도",
    "할 수 있으니 확인해 보세요",
    "할 수 있도록 순서를 정해 보세요",
    "구체적으로는 학습 방향은",
    "관리의 범위도 분명해질 수 있는 조건을 확인해야 합니다",
    "의미가 달라질 수 있는 조건을 확인해야 하며",
    "확인하는 편이 구체적이라는 점도 함께 살펴야 합니다",
    "확인하는 편이 구체적이라는 사실을 먼저 확인해야 합니다",
    "구체적인지 살펴본 뒤 기록해 두세요",
    "필요하면 각 단계를 모두 같은 날 끝내려 하기보다 필요하면",
    "작성한 풀이를 멈춘 순간",
    "의미가 달라지는 과정을 살펴보는 것이 좋습니다",
    "의미가 달라지도록 기준을 세워야 합니다",
    "우선순위는 같은 유형을",
    "우선순위는 과제량을",
    "CU맞은편",
    "cu건물",
    "건물5층",
    "중학생 수학 상담에서는 수학",
    "수업을 비교한다면 수업",
    "수업을 비교한다면 비교할 때",
    "상담에서 첫 상담 뒤에는",
    "층,.",
    "봉담2기본적으로",
    "준비 순서를 정해 보세요",
    "옮겨도 되는지를 질문해 볼 수 있습니다",
    "기록해 두세요, 기본적으로",
    "흐름이 필요한지 확인해 보아야 합니다",
    "확인하는 편이 구체적",
    "분리해 적게 하는 방법이 있는지 질문해 볼 수 있습니다",
    "차이가 무엇인지 확인해야 합니다",
    "의미가 달라지는 과정을",
    "의미가 달라지도록",
    "우선순위는 학교 진도와 현재 약점의 우선순위를",
    "분리해 적게 하는 방법도 좋습니다",
    "구체적으로는 상담에서는",
    "질문할 수 있는지 살펴보세요",
    "확인할 수 있는지 살펴보세요",
    "확인할 수 있다는 점을 참고하세요",
    "직접 점검할 필요가 있는지를 기록해 두는 편이 좋습니다",
    "확인하는지에 따라 의미가 달라지는지 살펴야 합니다",
    "확인하는지에 따라 의미가 달라지는지 살펴야 하며",
    "분리해 적게 하는 방법도 있음을 기억해 둘 필요가 있습니다",
    "분리해 적게 하는 방법이 있는지도 함께 확인해야 합니다",
    "그다음에는 이 상태를",
    "것을 확인 기준으로 삼을 수 있습니다",
    "적어 보면서 차이를 확인하세요",
    "가정에서는 몇 쪽을 풀었는지보다 새로 이해한 개념과 반복된 실수를 확인할 필요가 있습니다",
    "눈으로 확인할 수 있는 항목을 구체적인 항목을 정해 보세요",
    "관리의 범위도 분명해질 수 있으므로 주의 깊게 살펴야 합니다",
    "구체적으로는 상담할 때에는",
    "존재 여부, 이용 대상, 이용 시간이나 조건, 별도 비용 여부, 안전과 관리 기준을",
    "그다음 주소만 보고",
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
MIDDLE_ENGLISH_BANNED = (
    "입시수학학원",
    "영어 수학",
    "과목 참고어",
    "입력된 소재",
    "입력 표기",
    "보조 문맥",
    "확인된 확인 주소",
    "확인된 추가 확인 항목",
    "상담용 확인 소재이며 실제 제공 여부를 뜻하지 않습니다",
    "표현만으로 확인할 수 없습니다",
    "존재 여부나 적용 대상",
    "이 항목은 학부모",
    "“있나요”라는 한 질문",
    '"있나요"라는 한 질문',
    "적용 대상과 시점",
    "답변되지 않은 부분",
    "운영된다고 단정",
    "미확인 항목",
    "마지막으로 확인할 점은 다음과 같습니다",
    "에서는 좋은 질문은",
    "에서는 다음 점검 항목은",
    "에서는 이 순서는",
    "에서는 이 기록은",
    "에서는 이 안내는",
    "에서는 계획표는",
    "에서는 지역 정보는",
    "에서는 주소와 학교 표기는",
    "에서는 복습은",
    "에서는 상담 답변은",
    "에서는 과목 접근은",
    "에서는 학습 과정은",
    "에서는 학습 계획은",
    "에서는 가정 점검은",
    "에서는 현재 상태는",
    "에서는 관리라는 말은",
    "에서는 기초 확인은",
    "에서는 학습 방향은",
    "에서는 현재 어려움은",
    "에서는 피드백은",
    "에서는 질문은",
    "에서는 상담 메모는",
    "에서는 영어의 어려움은",
    "에서는 중등 영어학원 선택은",
    "에서는 대상 학년, 과목 범위, 진단 방식은",
    "에서는 과제를 했는지와 과제 내용을 이해했는지는",
    "에서는 실수와 개념 부족은",
    "만들어 쓰지 않으며",
    "실제 답변을 받아 빈칸을 채워야 합니다",
    "’가며",
    "중등 영어학원 선택에서는",
    "에서 대신 ",
    "진도를 넓히기보다 과제량보다",
    "질문을 이 네 갈래로",
    "선택에서 중등 영어학원 비교에서",
    "선택에서 중등 영어학원을 선택할 때는",
    "상담에서 상담 내용을 같은 항목으로",
    "상담 범위에서",
    "중등 영어학원 비교에서",
    "에서 중등 영어학원 안내에서",
    "관련 선택에서",
    "중등 영어 상담 선택에서",
    "중등 영어 수업 선택에서",
    "중등 영어 학습 과정 선택에서",
    "확인된 사실, 일반적인 학습 점검법, 상담에서 확인할 내용을 서로 구분해 읽어야 합니다",
    "이라는 표기는 지역 범위를 나타낼 뿐 학습 결과나 특정 수업 구성을 의미하지 않습니다",
    "라는 표기는 지역 범위를 나타낼 뿐 학습 결과나 특정 수업 구성을 의미하지 않습니다",
    "여러 이름이 있어도 나누거나 확장하지 않으며",
    "여러 이름이나 설명이 함께 적힌 형태라면 이를 근거 없이 나누거나 정식 명칭으로 바꾸지 않고 그대로 확인해야 합니다",
    "페이지의 이 표기는 학교와 학원의 제휴, 해당 학교 학생의 수강 사실, 특정 학교만을 위한 수업을 뜻하지 않습니다",
    "이 표기는 학교와 학원의 제휴나 실제 수강 관계를 뜻하지 않습니다",
    "특정 학원의 관리 방식이 존재한다는 뜻이 아닙니다",
    "특정 운영 사실이 아니라",
    "실제 운영을 단정하는 말이 아니라",
    "수업에서는",
    "상담에서는 학생이",
    "상담에서는 최근",
    "상담에서는 점수",
    " 관련 결정은",
    " 관련 상담할 때",
    " 관련 답변",
    "지역 표기는 검색 범위를 이해하는 데만 사용해야 하며",
    "확인된 정보의 역할을 나누면 과도한 해석을 피할 수 있습니다",
    "결과를 예측하기 위한 자료가 아니라 현재 질문을 구체화하기 위한 메모로 사용합니다",
    "확인된 사실, 일반적인 학습 점검법, 상담할 때 확인할 내용을 서로 구분해 읽어야 합니다",
    "특정 수업이 실제로 운영된다는 뜻이 아니라",
    "페이지의 지역성은",
    "확인용 주소는",
    "주소 표현을 바꾸거나 주변 상권과 교통을 예상해서는 안 됩니다",
    "주소만으로 이동 시간, 교통이나 주변 환경을 예상하지 않습니다",
    "지역 정보는 학습 기준을 대신하지 않으므로",
    "확인된 학교 관련 표기는",
    "이 순서는 실제 교재나 프로그램의 존재를 말하는 것이 아니라",
    "표기를 읽는 기준",
    "결정 전에 남길 세 가지 질문</h2><p>진단 기준, 연습 방식, 오답 복습, 피드백 범위",
    "범위에서만 사용하고 수업·시설·결과는 상담 전까지 미확인으로 남깁니다",
    "선택 과정에서 확인하지 못한 정보를 사실처럼 채우지 않는 태도가 중요합니다",
    "관련 확인에서 학교 표기가 비어",
    "관련 확인에서 수업 가능 학교가 따로 안내되지 않은 경우",
    "상담할 때는 상담 내용을",
    "상담할 때 상담 답변",
    "상담할 때 중등 영어학원을 선택할 때는",
    "두 기록을 함께 설명하면",
    "상담할 때는 결정 전에는",
    "중등 영어 수업 상담할 때",
    "중등 영어 학습 과정 상담할 때",
    "지역 중등 영어 학습 상담할 때",
    "상담할 때 학습 계획은 예상 진도보다",
    "관련 정보에는 확인된 지역·학교·주소만 옮기고, 시간표나 비용처럼 없는 내용은 빈칸으로 두었다가 직접 확인하세요",
    "이 순서는 특정 프로그램을 소개하는 내용이 아니라 상담 답변을 비교하기 위한 틀입니다",
    "지역 정보와 주소는 별도 칸에 두어 학습 기준과 섞이지 않게 하세요",
    "학교 표기가 비어 있으므로 주변 학교를 추측하지 않고",
    "상담할 때 중등 영어학원을 알아볼 때",
    "영어 학습 판단에 필요한 어휘·문법·독해의 연결만 보조적으로 설명합니다",
    "빈칸을 추측으로 채우지 않는 것이 신뢰성 있는 선택의 기본입니다",
    "답을 듣지 못한 항목은 추측하지 말고 미확인으로 남겨야 합니다",
    "주소와 학교 표기는 위치를 확인하기 위한 정보이며 학습 적합성을 대신 판단하지 않습니다",
    "중등 영어학원을 선택할 때도 이동이나 주변 환경을 추정하지 말고",
    "방식을 방식은",
    "구분해 기록하는 방식으로 기록하고",
    "구분해 기록하는 방식으로 기록하면",
    "학생을 가정하면",
    "진단, 연습, 복습, 피드백이 이어지는지를 질문할 수 있습니다",
    "상담할 때 상담할 때",
    "중등 영어학원을 비교할 때 중등 영어학원 안내에서",
    "중등 영어학원을 비교할 때 상담할 때",
    "중등 영어 학습 상담할 때",
    "학습 계획이 예상 진도보다 재확인 기준이 있어야 비교하기 쉽습니다",
    "학습 계획은 예상 진도보다 재확인 기준이 있어야 비교하기 쉽습니다",
    "틀린 문제를 바로 고친 경우와 며칠 뒤에도 설명한 경우를 같은 기록으로",
    "현재 사용하는 교재와 구체적인 수업 방식은 상담할 때 직접 확인하세요. 대신",
    "현재 사용하는 교재와 구체적인 수업 방식은 상담에서 직접 확인하세요. 대신",
    "이 순서를 기준으로 학생이 어느 단계에서 막히는지 살펴볼 수 있습니다",
    "관찰 기록은 결과 판단보다 상담할 때 어떤 지원이 필요한지 설명하는 관찰 기록으로 활용하세요",
    "상담 뒤 확인할 여섯 가지",
    "이 순서를 기준으로 학생의 현재 상태와 상담 답변을 비교해 보세요",
    "상담 답변에는 이 차이를 좁히는 연습과 복습 확인 방법이 구체적으로 담기는지 살펴보세요",
    "지역 중등 영어 학습",
    "중등 영어 학습 과정 FAQ",
    "중등 영어 학습 과정 결정",
    "중등 영어 학습 과정 선택",
    "중등 영어학원 선택은 체크가 많다는 이유보다 중요한 질문에 답이 있는지를 보고 판단하는 편이 좋습니다",
    "과제 수행 여부와 이해 정도를 별도로 살피는지와 피드백의 연결을 구체적으로 들어보는 편이 좋습니다",
    "는지와 피드백의 연결을 구체적으로 들어보는 편이 좋습니다",
    "짧게 확인하는 방식으로 짧게 기록한 뒤",
    "그 질문에 구체적인 확인 방법이 제시되는지 확인할 수 있습니다",
    "중등 영어 상담할 때는",
    "비교할 때 선택 전에는",
    "상담할 때 선택 전에는",
    "중등 영어학원 상담 답변이 이 전환 과정을 어떻게 살피는지 구체적으로 들을 수 있어야 합니다",
    "학교별 범위를 미리 가정하지 않고 학생이 가져온 최근 과제와 진도표를 토대로 학습 순서를 안내합니다",
    "복습은 같은 내용을 오래 보는 것보다 다시 확인할 시점과 방법을 정하는 데 의미가 있습니다",
    "학원을 결정할 때는 확인 순서를 지키는 것만으로도 더 차분해질 수 있습니다",
    "학생이라면 학생이",
    "학생이라면 학생 상태를",
    "는지라는 질문에 과정과 기준이 함께 설명되는지 확인하는 것이 좋습니다",
    "중등 영어 상담을 비교할 때",
    "학습 행동을 작은 단위로 살펴보고 상담 질문을 만드는 데만 사용합니다",
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
            if category in {"고등수학학원", "중등수학학원"}:
                for token in HIGH_MATH_BANNED:
                    if token in text:
                        errors.append(f"{rel}: subject mismatch remains: {token}")
            if category == "중등수학학원":
                for token in MIDDLE_MATH_BANNED:
                    if token in text:
                        errors.append(f"{rel}: middle-math wording remains: {token}")
            if category in {"고등영어학원", "중등영어학원"}:
                for token in HIGH_ENGLISH_BANNED:
                    if token in text:
                        errors.append(f"{rel}: subject mismatch remains: {token}")
            if category == "중등영어학원":
                local = title.removesuffix(" " + CATEGORY_LABELS[category]).strip()
                for token in MIDDLE_ENGLISH_BANNED:
                    if token in text:
                        errors.append(f"{rel}: middle-English wording remains: {token}")
                if re.search(r"상담할 때[^.!?]{0,240}상담할 때", text):
                    errors.append(f"{rel}: repeated consultation phrase in one sentence")
                if re.search(r"<p>\s*대신\s+", source):
                    errors.append(f"{rel}: orphan paragraph-leading contrast marker")
                if re.search(
                    r"<p>\s*이는\s+특정\s+(?:수업이 실제로 운영된다는 뜻|운영 사실)이 아니라",
                    source,
                ):
                    errors.append(f"{rel}: orphan paragraph-leading pronoun")
                if re.search(r"(?:경기|서울|인천|부산|대구|대전|광주|울산|세종|강원|충북|충남|전북|전남|경북|경남|제주)\s+([가-힣]+?)(?:시|군|구)\s+\1\s+", text):
                    errors.append(f"{rel}: duplicated administrative locality")
                if "전북 완주군 전주 장동" in text:
                    errors.append(f"{rel}: mixed administrative and search locality")
                if re.search(r"(?:[가-힣0-9]+(?:중|고|초)\.\s*){2,}", text):
                    errors.append(f"{rel}: orphan school-name sentence fragments")
                for marker in (
                    f"{local} 선택에서",
                    f"{local} 관련 판단에서",
                    f"{local} 관점에서",
                ):
                    if marker in text:
                        errors.append(f"{rel}: mechanical locality lead remains: {marker}")
            if category in {"고등수학학원", "고등영어학원", "중등수학학원", "중등영어학원"}:
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
            if category == "중등영어학원" and local.endswith("을"):
                damaged_local = local[:-1] + "를"
                if damaged_local in text:
                    errors.append(f"{rel}: damaged locality remains: {damaged_local}")
            if category == "중등영어학원" and local:
                last_code = ord(local[-1])
                local_has_batchim = (
                    0xAC00 <= last_code <= 0xD7A3
                    and (last_code - 0xAC00) % 28 != 0
                )
                if not local_has_batchim and f"{local}과 확인된 센터 주소" in text:
                    errors.append(f"{rel}: malformed locality conjunction")
                if f"{local}에서 대신 " in text:
                    errors.append(f"{rel}: orphan contrast marker")
            if re.search(
                rf"{re.escape(local)}에서\s+{re.escape(local)}(?=\s|은|는|이|가|을|를|의|에|에서|으로|와|과|도|만|[,.;!?]|$)",
                text,
            ):
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
            if category in {"고등수학학원", "고등영어학원", "중등수학학원", "중등영어학원"}:
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
