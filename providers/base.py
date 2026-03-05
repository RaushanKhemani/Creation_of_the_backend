from dataclasses import dataclass


@dataclass
class ProviderResult:
    text: str
    model_name: str
    tokens_in: int
    tokens_out: int


class ProviderError(Exception):
    pass
