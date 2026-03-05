import asyncio

from providers.base import ProviderResult


class MockProviderClient:
    def __init__(self, provider_key: str) -> None:
        self.provider_key = provider_key

    async def generate(self, prompt: str, _: str | None = None) -> ProviderResult:
        await asyncio.sleep(0.05)
        normalized = prompt.strip().lower()
        if normalized in {"hi", "hello", "hey", "hii"}:
            text = f"[{self.provider_key}] Hello. How are you today?"
        else:
            text = f"[{self.provider_key}] {prompt}"
        tokens_in = max(1, len(prompt) // 4)
        tokens_out = max(1, len(text) // 4)
        return ProviderResult(
            text=text,
            model_name=f"{self.provider_key}-simulated-v1",
            tokens_in=tokens_in,
            tokens_out=tokens_out,
        )
