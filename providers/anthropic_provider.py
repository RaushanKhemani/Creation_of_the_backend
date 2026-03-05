import httpx

from providers.base import ProviderError, ProviderResult


class AnthropicClient:
    async def generate(self, prompt: str, api_key: str, model_name: str, timeout_seconds: int) -> ProviderResult:
        if not api_key:
            raise ProviderError("Missing provider API key")

        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": model_name,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            response = await client.post(url, json=payload, headers=headers)

        if response.status_code >= 400:
            raise ProviderError(f"Provider error {response.status_code}: {response.text[:200]}")

        data = response.json()
        content = data.get("content") or []
        text_parts = [item.get("text", "") for item in content if item.get("type") == "text"]
        text = "\n".join(part for part in text_parts if part).strip()
        usage = data.get("usage", {})

        return ProviderResult(
            text=text,
            model_name=data.get("model", model_name),
            tokens_in=int(usage.get("input_tokens", max(1, len(prompt) // 4))),
            tokens_out=int(usage.get("output_tokens", max(1, len(text) // 4))),
        )

