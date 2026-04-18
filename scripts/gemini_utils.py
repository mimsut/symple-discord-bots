"""Gemini 공통 유틸 — 재시도 로직 포함"""
import time
import google.generativeai as genai


def get_model(api_key: str, model: str = "gemini-1.5-flash"):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model)


def generate(model, prompt: str, max_retries: int = 5) -> str:
    for attempt in range(max_retries):
        try:
            resp = model.generate_content(prompt)
            return resp.text.strip()
        except Exception as e:
            err = str(e)
            if any(k in err for k in ("429", "quota", "RESOURCE_EXHAUSTED", "rate")):
                wait = 30 * (attempt + 1)
                print(f"[Gemini] rate limit (attempt {attempt + 1}/{max_retries}), {wait}s 대기...")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Gemini max retries exceeded")
