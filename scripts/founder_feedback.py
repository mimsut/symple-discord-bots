#!/usr/bin/env python3
import os, requests, sys
sys.path.insert(0, os.path.dirname(__file__))
from gemini_utils import get_client, generate
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST)
today_str = today.strftime("%Y년 %m월 %d일")
seed = today.strftime("%Y-%m-%d")
day_of_year = today.timetuple().tm_yday

ANGLES = [
    "리텐션과 제품-시장 적합성", "B2B 영업 전략과 ICP 정의", "가격 책정과 가치 증명",
    "창업자 번아웃과 시스템 구축", "미국 시장 진입 전략", "투자자 유치 vs 고객 매출",
    "데이터 기반 의사결정", "팀 빌딩과 첫 채용", "피봇 결정의 기준",
    "경쟁사 대비 차별화 포인트",
]
angle = ANGLES[day_of_year % len(ANGLES)]

client = get_client()
text = generate(client, f"""날짜: {today_str} | 오늘의 각도: {angle}
당신은 Paul Graham + Sam Altman 스타일의 냉혹하게 솔직한 YC 파트너입니다.
오늘은 반드시 "{angle}" 관점에서만 직언하세요. 매일 다른 주제로 다뤄야 합니다.

SYMPLE: CBT 기반 멘탈헬스 앱 Duck's Dream. 한국 B2C → 미국 B2B2C 기업 웰니스 피벗 중.
창업자: 김민수, 연세대 심리학 학·석사 4년 (18학점 남음).
성과: 토스 미니앱 신규 4위, 텀블벅 크라우드펀딩, 대한디지털치료학회 우수포스터, SF MARU 3주, 정주영창업경진대회.

시드({seed})를 기반으로 매일 다른 주제와 각도에서 직언을 작성하세요.

아래 형식 그대로만 출력 (1800자 이내):

⚡ **민수에게 — YC 파트너의 직언 | {today_str}**

🔴 **지금 가장 큰 실수**
[냉혹한 직언. SYMPLE 상황에 맞는 실제 업계 수치·벤치마크 포함.]

🙈 **지금 회피하는 것**
[민수가 직면해야 할 불편한 진실 1가지. 구체적으로.]

⏰ **48시간 내 해야 할 것**
→ [구체적이고 실행 가능한 행동.]

📊 **당장 대답할 수 있어야 하는 숫자**
"[실제 업계 벤치마크 포함한 핵심 지표 질문]"

💪 **마지막으로**
[진심 어린 응원 한 문장.]""")

r = requests.post(os.environ["DISCORD_YC_FEEDBACK"], json={"content": text[:2000]}, timeout=30)
print(f"founder_feedback → {r.status_code}")
