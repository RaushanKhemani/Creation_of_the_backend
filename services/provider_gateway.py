from providers.base import ProviderResult
from providers.registry import get_provider_client


class ProviderGateway:
    async def generate(
        self,
        provider_key: str,
        prompt: str,
        api_key: str | None = None,
        *,
        timeout_seconds: int = 20,
    ) -> ProviderResult:
        if not api_key:
            raise ValueError("Missing API key for selected provider")
        client, model_name = get_provider_client(provider_key)
        return await client.generate(prompt, api_key, model_name, timeout_seconds)
