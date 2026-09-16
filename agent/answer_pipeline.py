import time

from agent.factory import create_candidate_agent
from answer_quality.evaluator import evaluate_final_answer


def safe_run(name, func, *args):
    """Run one operation and report its status."""
    try:
        result = func(*args)
        print(f"{name}: PASS")
        return result
    except Exception as e:
        print(f"{name}: FAIL -> {e}")
        return None


class AnswerTrace:
    """Collect and print runtime events."""

    def __init__(self, question: str):
        self.question = question
        self.events = []

    def record(self, stage: str, details: dict):
        self.events.append({"stage": stage, **details})
        print(f"{stage}: {details.get('status', 'WARNING')}")

    def record_llm(self, agent):
        model = getattr(agent, "model", None)

        for step in getattr(agent.memory, "steps", []):
            usage = getattr(step, "token_usage", None)

            if usage:
                self.record(
                    "LLM",
                    {
                        "status": "PASS",
                        "model": getattr(model, "model_id", None),
                        "input_tokens": getattr(
                            usage, "input_tokens", None
                        ),
                        "output_tokens": getattr(
                            usage, "output_tokens", None
                        ),
                    },
                )

    def report(self):
        print("\n" + "=" * 60)
        print("ANSWER PIPELINE TRACE")
        print("=" * 60)
        print(f"Question: {self.question}")
        print("-" * 60)

        for i, event in enumerate(self.events, 1):
            print(
                f"[{i:02d}] "
                f"{event['stage']:<12} "
                f"{event['status']}"
            )

            for key, value in event.items():
                if key not in ("stage", "status"):
                    print(f"     {key}: {value}")

        print("=" * 60)


def check_input(question: str) -> str:
    """Validate and normalize the recruiter question."""
    assert question and question.strip(), (
        "Recruiter question is empty"
    )
    return " ".join(question.split())


def check_agent(trace: AnswerTrace):
    """Create the candidate agent."""
    agent = create_candidate_agent(
        trace_callback=trace.record
    )
    assert agent is not None, "Agent was not created"
    return agent


def run_agent(agent, question: str):
    """Run one real agent execution."""
    return agent.run(question, reset=True)


def check_answer(answer: str) -> str:
    """Validate the final answer."""
    assert answer is not None, "Agent returned None"

    answer = str(answer).strip()

    assert answer, "Final answer is empty"

    return answer


def run_pipeline(question: str):
    """Run one real answer execution and record its events."""

    start = time.perf_counter()
    trace = AnswerTrace(question)

    print("=" * 60)
    print("INTERVIEW MY AI - ANSWER PIPELINE")
    print("=" * 60)
    print(f"Question:\n{question}")
    print("=" * 60)

    # 01 INPUT
    question = safe_run("Input", check_input, question)
    if question is None:
        return None

    # 02 AGENT
    agent = safe_run("Agent", check_agent, trace)
    if agent is None:
        return None

    # 03 → 06 REAL EXECUTION
    answer = safe_run(
        "Agent Run",
        run_agent,
        agent,
        question,
    )

    if answer is None:
        return None

    # 06 LLM
    trace.record_llm(agent)

        # 07 ANSWER
    answer = safe_run(
        "Answer",
        check_answer,
        answer,
    )

    if answer is None:
        return None

    # 08 QUALITY
    evidence = []

    for step in getattr(agent.memory, "steps", []):
        observations = getattr(step, "observations", None)

        if observations:
            evidence.extend(
                str(observation)
                for observation in observations
                if observation
            )

    evidence = "\n\n".join(evidence)

    trace.record(
        "QUALITY",
        evaluate_final_answer(
            answer=answer,
            question=question,
            evidence=evidence,
        ),
    )

    trace.report()

    print("\nFinal answer:")
    print(answer)

    print(
        f"\nPipeline finished in "
        f"{time.perf_counter() - start:.2f}s"
    )

    return answer


if __name__ == "__main__":
    run_pipeline(
        "Tell me about my Sudoku solver project."
    )