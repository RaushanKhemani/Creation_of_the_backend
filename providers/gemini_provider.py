import httpx

from providers.base import ProviderError, ProviderResult


class GeminiClient:
    async def generate(self, prompt: str, api_key: str, model_name: str, timeout_seconds: int) -> ProviderResult:
        if not api_key:
            raise ProviderError("Missing provider API key")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7},
        }
        headers = {"Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            response = await client.post(url, json=payload, headers=headers)

        if response.status_code >= 400:
            raise ProviderError(f"Provider error {response.status_code}: {response.text[:200]}")

        data = response.json()
        candidates = data.get("candidates") or []
        if not candidates:
            raise ProviderError("Provider returned no candidates")

        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts).strip()
        usage = data.get("usageMetadata", {})

        return ProviderResult(
            text=text,
            model_name=model_name,
            tokens_in=int(usage.get("promptTokenCount", max(1, len(prompt) // 4))),
            tokens_out=int(usage.get("candidatesTokenCount", max(1, len(text) // 4))),
        )

