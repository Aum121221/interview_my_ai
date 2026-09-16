from answer_quality.formatting import observe_answer_format
from answer_quality.quality import evaluate_answer
from answer_quality.grounding import evaluate_grounding
from answer_quality.format_compliance import evaluate_format_compliance


def evaluate_final_answer(
    answer: str,
    question: str | None = None,
    evidence: str | None = None,
    expected_format: str | None = None,
) -> dict:
    """Evaluate the final answer using deterministic V1 checks."""

    quality = evaluate_answer(answer)

    result = {
        "status": quality["status"],
        "findings": quality["findings"],
        "format": observe_answer_format(answer),
        "length": len(str(answer).strip()) if answer else 0,
    }

    if evidence is not None:
        result["grounding"] = evaluate_grounding(
            answer=answer,
            evidence=evidence,
        )

    if expected_format is not None:
        result["format_compliance"] = evaluate_format_compliance(
            answer=answer,
            expected_format=expected_format,
        )

    return result