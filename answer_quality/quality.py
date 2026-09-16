def evaluate_answer(answer: str) -> dict:
    """Evaluate basic deterministic V1 answer quality."""

    if answer is None:
        return {
            "status": "FAIL",
            "findings": ["Final answer is missing."],
        }

    answer = str(answer).strip()

    if not answer:
        return {
            "status": "FAIL",
            "findings": ["Final answer is empty."],
        }

    findings = []

    if len(answer) < 20:
        findings.append("Answer may be too short.")

    status = "WARNING" if findings else "PASS"

    return {
        "status": status,
        "findings": findings,
    }