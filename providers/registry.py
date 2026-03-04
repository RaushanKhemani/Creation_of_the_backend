from providers.mock_provider import MockProviderClient


def get_provider_client(provider_key: str):
    normalized = provider_key.strip().lower()
    supported = {"chatgpt", "gemini", "grok", "claude", "groq", "copilot"}
    if normalized not in supported:
        raise ValueError("Unsupported provider key")
    return MockProviderClient(normalized)
