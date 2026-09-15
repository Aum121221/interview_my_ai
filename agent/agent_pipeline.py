import time

from agent.factory import create_candidate_agent
from agent.instructions import CANDIDATE_INSTRUCTIONS
from agent.tools import CandidateKnowledgeSearchTool


TEST_QUESTION = (
    "Tell me about my Sudoku solver project. "
    "What approach did I use, what challenges did I face, "
    "and what did I learn from it?"
)


def safe_run(name, func, *args):
    try:
        result = func(*args)
        print(f"{name}: PASS")
        return result

    except Exception as e:
        print(f"{name}: FAIL -> {e}")

        choice = input("Continue? (y/n): ").strip().lower()

        if choice == "y":
            return None

        print("Pipeline stopped.")
        exit(1)


def check_instructions():
    assert CANDIDATE_INSTRUCTIONS, (
        "Candidate instructions missing"
    )


def check_agent():
    agent = create_candidate_agent()

    assert agent is not None, (
        "Agent was not created"
    )

    return agent


def check_tool():
    tool = CandidateKnowledgeSearchTool()

    assert tool is not None, (
        "Tool was not created"
    )

    assert callable(tool.forward), (
        "Tool forward() is not callable"
    )

    return tool


def check_retrieval(tool, question):
    result = tool.forward(question)

    assert result is not None, (
        "Retrieval returned None"
    )

    return result


def check_agent_run(agent, question):
    answer = agent.run(
        question,
        reset=True,
    )

    assert answer is not None, (
        "Agent returned None"
    )

    return answer


def run_pipeline():
    start = time.perf_counter()

    print("=" * 60)
    print("INTERVIEW MY AI - AGENT PIPELINE")
    print("=" * 60)
    print(f"Test question:\n{TEST_QUESTION}")
    print("=" * 60)

    # 1. agent/instructions.py
    safe_run(
        "Instructions",
        check_instructions,
    )

    # 2. agent/core.py
    agent = safe_run(
        "Agent",
        check_agent,
    )

    # 3. agent/tools.py
    tool = safe_run(
        "Tool",
        check_tool,
    )

    # 4. ingestion/retrieval.py
    evidence = safe_run(
        "Retrieval",
        check_retrieval,
        tool,
        TEST_QUESTION,
    )

    if evidence is not None:
        print("\nRetrieved evidence:")
        print(evidence)

    # 5. Actual Agent → Retrieval → LLM flow
    answer = safe_run(
        "Agent Run / LLM",
        check_agent_run,
        agent,
        TEST_QUESTION,
    )

    if answer is not None:
        print("\nFinal answer:")
        print(answer)

    print()
    print("=" * 60)
    print(
        f"Agent pipeline finished in "
        f"{time.perf_counter() - start:.2f}s"
    )
    print("=" * 60)

    return answer


if __name__ == "__main__":
    run_pipeline()