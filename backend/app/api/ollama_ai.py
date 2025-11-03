import httpx
from fastapi import APIRouter, HTTPException
import json
import re

router = APIRouter()

OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL_NAME = "llama3"

# Cache simples para traduções repetidas
TRANSLATION_CACHE = {}


def clean_summary(text: str) -> str:
    """
    Remove formatações e caracteres especiais da resposta da IA.
    """
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"[_`#>~:-]", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


async def translate_to_english(client, text: str) -> str:
    """
    Usa o modelo do Ollama para traduzir o texto para inglês puro.
    """
    if not text:
        return text

    if text in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[text]

    translate_prompt = (
        f"Translate this text to English only. "
        f"Output the translation only, no explanations or comments:\n\n{text}"
    )

    try:
        response = await client.post(
            OLLAMA_URL,
            headers={"Content-Type": "application/json"},
            json={"model": MODEL_NAME, "prompt": translate_prompt, "stream": False},
        )
        if response.status_code == 200:
            data = json.loads(response.text)
            translated = clean_summary(data.get("response", "").strip())
            TRANSLATION_CACHE[text] = translated
            return translated
    except Exception:
        pass

    return text


@router.post("/analyze")
async def analyze(payload: dict):
    """
    Recebe o resultado do fact-check (claim + sources)
    e retorna resumos da IA para cada fonte, com tradução e limpeza.
    """
    claim = payload.get("claim")
    sources = payload.get("sources")

    if not claim or not sources:
        raise HTTPException(status_code=400, detail="Missing 'claim' or 'sources'")

    summaries = []

    async with httpx.AsyncClient(timeout=httpx.Timeout(180.0)) as client:
        for s in sources:
            publisher = s.get("publisher", "Unknown source")
            title = s.get("title", "")
            url = s.get("url", "")
            rating = s.get("rating", "Not rated")

            # Limpeza básica antes da tradução
            title = re.sub(r"[^\w\s.,!?-]", "", title).strip()
            rating = rating.replace(":", "").capitalize()

            # 🔹 Tradução automática
            title_en = await translate_to_english(client, title)
            publisher_en = await translate_to_english(client, publisher)
            rating_en = await translate_to_english(client, rating)

            # 🔹 Prompt refinado
            prompt = f"""
You are an AI fact-checking assistant.
Summarize the verified article below in 2–3 sentences of clear, neutral English.

Claim: {claim}
Source: {publisher_en}
Title: {title_en}
Rating: {rating_en}
URL: {url}

Write only the summary in plain English.
Do not include headers, bullet points, or explanations.
"""

            try:
                response = await client.post(
                    OLLAMA_URL,
                    headers={"Content-Type": "application/json"},
                    json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Ollama error ({response.status_code}): {response.text}",
                    )

                data = json.loads(response.text)
                summary = clean_summary(data.get("response", "").strip())

                summaries.append({
                    "publisher": publisher_en,
                    "title": title_en,
                    "url": url,
                    "rating": rating_en,
                    "summary": summary,
                })

                print(f"✅ [AI] Summary generated for {publisher_en}")

            except Exception as e:
                print(f"❌ [AI] Error summarizing {publisher_en}: {e}")
                summaries.append({
                    "publisher": publisher_en,
                    "title": title_en,
                    "url": url,
                    "rating": rating_en,
                    "summary": f"⚠️ Error connecting to AI: {str(e)}",
                })

    return {"claim": claim, "summaries": summaries}
