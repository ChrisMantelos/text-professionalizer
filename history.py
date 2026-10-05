def add_to_history(history: list[dict], original: str, tone: str, result: str, max_items: int = 5) -> list[dict]:
    entry = {"original": original, "tone": tone, "result": result}
    return ([entry] + list(history))[:max_items]
