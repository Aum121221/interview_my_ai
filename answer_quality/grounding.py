def evaluate_grounding(answer: str, evidence: str) -> dict:
    """Check whether the answer has support in the evidence."""

    if not answer or not str(answer).strip():
        return {
            "status": "FAIL",
            "findings": ["Final answer is missing."],
        }

    if not evidence or not str(evidence).strip():
        return {
            "status": "WARNING",
            "findings": ["No candidate evidence was available."],
        }

    answer_words = set(str(answer).lower().split())
    evidence_words = set(str(evidence).lower().split())

    overlap = answer_words & evidence_words

    if not overlap:
        return {
            "status": "WARNING",
            "findings": ["Answer has no obvious overlap with evidence."],
        }

    return {
        "status": "PASS",
        "findings": [],
    }