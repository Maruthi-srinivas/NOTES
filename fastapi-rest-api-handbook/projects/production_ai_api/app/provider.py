from collections.abc import AsyncIterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Completion:
    text: str
    prompt_tokens: int
    completion_tokens: int


class MockProvider:
    """Deterministic stand-in. No network and no API key."""

    name = "mock"

    async def complete(self, prompt: str) -> Completion:
        prompt_tokens = max(1, len(prompt.split()))
        text = "mock: " + " ".join(prompt.split()[:40])
        return Completion(text=text, prompt_tokens=prompt_tokens, completion_tokens=max(1, len(text.split())))

    async def stream(self, prompt: str) -> AsyncIterator[str]:
        completion = await self.complete(prompt)
        for word in completion.text.split():
            yield word + " "


def guard_output(text: str) -> str:
    kept = [line for line in text.splitlines() if not line.strip().lower().startswith("tool:")]
    return "\n".join(kept).strip()
