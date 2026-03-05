import httpx

from providers.base import ProviderError, ProviderResult


class OpenAICompatibleClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    async def generate(self, prompt: str, api_key: str, model_name: str, timeout_seconds: int) -> ProviderResult:
        if not api_key:
            raise ProviderError("Missing provider API key")

        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            response = await client.post(url, json=payload, headers=headers)

        if response.status_code >= 400:
            raise ProviderError(f"Provider error {response.status_code}: {response.text[:200]}")

        data = response.json()
        choices = data.get("choices") or []
        if not choices:
            raise ProviderError("Provider returned empty choices")

        message = choices[0].get("message", {})
        text = message.get("content", "")
        usage = data.get("usage", {})

        return ProviderResult(
            text=text,
            model_name=data.get("model", model_name),
            tokens_in=int(usage.get("prompt_tokens", max(1, len(prompt) // 4))),
            tokens_out=int(usage.get("completion_tokens", max(1, len(text) // 4))),
        )

