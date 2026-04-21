"""AI 공통 유틸 — Groq (무료, 카드 없음, 6000 req/day)"""
import os, time
from groq import Groq


def get_client():
    return Groq(api_key=os.environ["GROQ_API_KEY"])


MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

def generate(client, prompt: str, max_tokens: int = 2000, max_retries: int = 4) -> str:
    for model in MODELS:
        for attempt in range(max_retries):
            try:
                chat = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.8,
                )
                return chat.choices[0].message.content.strip()
            except Exception as e:
                err = str(e)
                if any(k in err for k in ("429", "rate", "limit", "RESOURCE")):
                    wait = 60 * (attempt + 1)
                    print(f"[Groq/{model}] rate limit (attempt {attempt+1}/{max_retries}), {wait}s 대기...")
                    time.sleep(wait)
                else:
                    raise
        print(f"[Groq] {model} rate limit 초과 → 다음 모델로 전환")
    raise RuntimeError("Groq max retries exceeded (all models)")
