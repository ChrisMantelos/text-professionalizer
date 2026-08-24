"""
CLI entry point for text-professionalizer.
Run: python main.py
"""

import sys
from professionalizer import professionalize, ProfessionalizerError, TONE_PROMPTS


def main() -> None:
    print("=== Text Professionalizer ===")
    print(f"Available tones: {', '.join(TONE_PROMPTS)}\n")

    text = input("Enter your draft text:\n> ").strip()
    tone = input(f"Tone [{'/'.join(TONE_PROMPTS)}] (Enter = formal): ").strip() or "formal"

    try:
        result = professionalize(text, tone=tone)
    except ProfessionalizerError as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        sys.exit(1)

    print("\n--- Result ---")
    print(result)


if __name__ == "__main__":
    main()
