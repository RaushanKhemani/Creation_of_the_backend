from dataclasses import dataclass


@dataclass
class ProviderResult:
    text: str
    tokens_in: int | None = None
    tokens_out: int | None = None
    source: str = "simulated"


class ProviderGateway:
    def generate(self, provider_key: str, prompt: str) -> ProviderResult:
        provider_key = provider_key.strip().lower()

        if provider_key == "chatgpt":
            text = f"[ChatGPT] {prompt}"
        elif provider_key == "copilot":
            text = f"[Copilot] Suggested code path for: {prompt}"
        elif provider_key == "gemini":
            text = f"[Gemini] Structured response for: {prompt}"
        elif provider_key == "grok":
            text = f"[Grok] Creative angle on: {prompt}"
        else:
            raise ValueError("Unsupported provider key")

        tokens_in = max(1, len(prompt) // 4)
        tokens_out = max(1, len(text) // 4)
        return ProviderResult(text=text, tokens_in=tokens_in, tokens_out=tokens_out, source="simulated")
