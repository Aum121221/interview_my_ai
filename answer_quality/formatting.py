def observe_answer_format(answer: str) -> str:
    """Observe the basic structure of a final answer."""

    answer = str(answer).strip()

    if not answer:
        return "EMPTY"

    if answer.startswith("{") and answer.endswith("}"):
        return "JSON"

    if "```" in answer:
        return "CODE"

    lines = answer.splitlines()

    if any(
        line.strip().startswith(("-", "*", "•"))
        for line in lines
    ):
        return "BULLET_LIST"

    if "|" in answer and len(lines) >= 2:
        return "TABLE"

    return "GENERAL_TEXT"