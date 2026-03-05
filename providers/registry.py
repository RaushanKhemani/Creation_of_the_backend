from config import get_settings
from providers.anthropic_provider import AnthropicClient
from providers.gemini_provider import GeminiClient
from providers.openai_compatible import OpenAICompatibleClient


def get_provider_client(provider_key: str):
    normalized = provider_key.strip().lower()
    settings = get_settings()

    if normalized == "chatgpt":
        return OpenAICompatibleClient("https://api.openai.com/v1"), settings.openai_model
    if normalized == "gemini":
        return GeminiClient(), settings.gemini_model
    if normalized == "claude":
        return AnthropicClient(), settings.anthropic_model
    if normalized == "grok":
        return OpenAICompatibleClient("https://api.x.ai/v1"), settings.xai_model
    if normalized == "groq":
        return OpenAICompatibleClient("https://api.groq.com/openai/v1"), settings.groq_model
    if normalized == "copilot":
        raise ValueError("Copilot provider is not yet available via this backend API")

    raise ValueError("Unsupported provider key")
