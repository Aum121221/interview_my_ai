def evaluate_format_compliance(
    answer: str,
    expected_format: str,
) -> dict:
    """Check whether the final answer follows the requested format."""

    if not answer or not str(answer).strip():
        return {
            "status": "FAIL",
            "findings": ["Final answer is missing."],
        }

    if not expected_format or not str(expected_format).strip():
        return {
            "status": "WARNING",
            "findings": ["No expected answer format was provided."],
        }

    answer = str(answer).strip()
    expected_format = str(expected_format).strip().upper()

    if expected_format == "GENERAL_TEXT":
        return {
            "status": "PASS",
            "findings": [],
        }

    if expected_format == "BULLET_LIST":
        valid = any(
            line.strip().startswith(("-", "*", "•"))
            for line in answer.splitlines()
        )
    elif expected_format == "CODE":
        valid = "```" in answer
    elif expected_format == "JSON":
        valid = answer.startswith("{") and answer.endswith("}")
    elif expected_format == "TABLE":
        lines = answer.splitlines()
        valid = "|" in answer and len(lines) >= 2
    else:
        return {
            "status": "WARNING",
            "findings": [
                f"Unknown expected format: {expected_format}"
            ],
        }

    if not valid:
        return {
            "status": "WARNING",
            "findings": [
                f"Answer does not appear to follow the expected "
                f"{expected_format} format."
            ],
        }

    return {
        "status": "PASS",
        "findings": [],
    }