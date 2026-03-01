from schemas.provider import ProviderInfo


def get_provider_catalog() -> list[ProviderInfo]:
    # This is the initial static catalog; replace with DB-backed data later.
    return [
        ProviderInfo(
            key="chatgpt",
            name="ChatGPT",
            category="general_assistant",
            enabled=True,
            notes="Great for planning and broad Q&A",
        ),
        ProviderInfo(
            key="copilot",
            name="GitHub Copilot",
            category="coding",
            enabled=True,
            notes="Best for coding workflows",
        ),
        ProviderInfo(
            key="gemini",
            name="Gemini",
            category="coding",
            enabled=True,
            notes="Alternative coding and multimodal workflows",
        ),
        ProviderInfo(
            key="grok",
            name="Grok",
            category="design_brainstorming",
            enabled=True,
            notes="Useful for idea exploration",
        ),
    ]
