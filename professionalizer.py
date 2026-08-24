"""
Core logic for text-professionalizer.
Separated from the CLI/UI layer so it can be reused by both.
"""

import os
from anthropic import Anthropic, APIError, APIConnectionError

TONE_PROMPTS = {
    "formal": (
        "Rewrite the given text as clear, formal, professional business "
        "communication. Preserve the original meaning and language "
        "(e.g. Greek input stays Greek). Output only the rewritten text, "
        "with no preamble, no explanation, and no quotation marks."
    ),
    "friendly": (
        "Rewrite the given text as warm, approachable, but still "
        "professional communication - suitable for a colleague you know "
        "well. Preserve the original meaning and language. Output only "
        "the rewritten text, with no preamble or explanation."
    ),
    "concise": (
        "Rewrite the given text as short, direct, professional "
        "communication. Cut any unnecessary words while preserving the "
        "core meaning and the original language. Output only the "
        "rewritten text, with no preamble or explanation."
    ),
}


class ProfessionalizerError(Exception):
    """Raised for any user-facing failure in the professionalize() call."""


def professionalize(text: str, tone: str = "formal", api_key: str | None = None) -> str:
    """
    Convert informal draft text into polished business communication.

    Args:
        text: The informal input text. Must be non-empty.
        tone: One of "formal", "friendly", "concise".
        api_key: Anthropic API key. Falls back to ANTHROPIC_API_KEY env var.

    Returns:
        The rewritten text.

    Raises:
        ProfessionalizerError: on empty input, bad tone, missing key,
        or API failure - always with a message safe to show the user.
    """
    if not text or not text.strip():
        raise ProfessionalizerError("Input text cannot be empty.")

    if tone not in TONE_PROMPTS:
        raise ProfessionalizerError(
            f"Unknown tone '{tone}'. Choose one of: {', '.join(TONE_PROMPTS)}."
        )

    key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise ProfessionalizerError(
            "No ANTHROPIC_API_KEY found. Set it as an environment "
            "variable or pass it in directly."
        )

    client = Anthropic(api_key=key)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=TONE_PROMPTS[tone],
            messages=[{"role": "user", "content": text.strip()}],
        )
    except APIConnectionError as exc:
        raise ProfessionalizerError(
            "Could not connect to the Anthropic API. Check your network connection."
        ) from exc
    except APIError as exc:
        raise ProfessionalizerError(f"The API returned an error: {exc}") from exc

    return response.content[0].text.strip()
