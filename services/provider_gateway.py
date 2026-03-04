from providers.base import ProviderResult
from providers.registry import get_provider_client


class ProviderGateway:
    async def generate(self, provider_key: str, prompt: str, api_key: str | None = None) -> ProviderResult:
        client = get_provider_client(provider_key)
        return await client.generate(prompt, api_key)
