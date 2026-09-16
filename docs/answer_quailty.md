# `answer_quality.md`

````markdown
# Answer Quality Specification

## Purpose

Define the V1 quality contract for evaluating the final answer produced by Interview My AI.

This specification belongs to the Answer stage of the pipeline.

It defines how an answer is evaluated after the real agent execution has completed.

It does not control agent behavior and must not be added to candidate instructions.

---

## Position in the Answer Pipeline

```text
01 INPUT
    ↓
02 AGENT
    ↓
03 TOOL
    ↓
04 RETRIEVAL
    ↓
05 EVIDENCE
    ↓
06 LLM
    ↓
07 ANSWER
    ↓
Answer Quality Evaluation
````

The evaluation observes the output of the real execution.

It does not perform another agent execution or LLM call.

---

# V1 Answer Contract

A final answer should satisfy the following requirements.

## 1. Existence

The answer must:

* exist
* not be `None`
* not be empty or whitespace-only

### PASS

A substantive final answer is produced.

### FAIL

No usable final answer is produced.

---

## 2. Relevance

The answer should directly address the recruiter's question.

It should:

* stay on the requested topic
* avoid unrelated information
* respond to the actual intent of the question

### PASS

The answer directly addresses the question.

### WARNING

The answer is related but contains unnecessary or weakly relevant material.

### FAIL

The answer does not meaningfully answer the question.

---

## 3. Grounding

Candidate-specific factual claims must be supported by retrieved candidate evidence.

Relevant claims include:

* projects
* skills
* technologies
* education
* experience
* responsibilities
* technical decisions
* implementations
* achievements
* challenges
* outcomes
* learning

General technical knowledge may be used to explain concepts, but must not be presented as candidate experience unless supported by candidate evidence.

### PASS

Candidate-specific claims are supported by available evidence.

### WARNING

Some claims require review or have weak/partial evidence.

### FAIL

The answer contains significant unsupported candidate-specific claims.

---

## 4. Unsupported Candidate Claims

The answer must not invent candidate-specific information.

Examples of claims requiring evidence include:

* "I built..."
* "I designed..."
* "I implemented..."
* "I worked on..."
* "I faced..."
* "I learned..."
* "I achieved..."
* "I improved..."
* "I used..."

The evaluator should distinguish between:

```text
Evidence-supported candidate fact
```

and:

```text
General technical explanation
```

### PASS

No unsupported candidate-specific claims are detected.

### WARNING

A claim requires additional evidence review.

### FAIL

The answer clearly fabricates candidate-specific information.

---

## 5. Question Coverage

The answer should address the information requested by the recruiter.

For a simple question:

```text
Tell me about my Sudoku solver project.
```

the answer should provide a useful description of the project.

For a multi-part question:

```text
What approach did I use?
What challenges did I face?
What did I learn?
```

the answer should address each requested part.

### PASS

The requested information is adequately covered.

### WARNING

One or more requested details are missing or weakly addressed.

### FAIL

The answer misses the primary purpose of the question.

---

## 6. Candidate Voice

The answer should represent the candidate appropriately.

Where the question concerns the candidate's own work, the answer should naturally use candidate perspective where appropriate.

Example:

```text
I implemented...
```

However, first-person claims must still be grounded in evidence.

Candidate voice does not override grounding requirements.

### PASS

The response is naturally expressed as the candidate.

### WARNING

The response is technically correct but sounds overly generic, detached, or unnatural.

### FAIL

The response misrepresents the candidate's perspective.

---

## 7. Clarity

The answer should be:

* understandable
* coherent
* grammatically readable
* logically organized
* free from obvious formatting or wording problems

### PASS

The answer is clear and readable.

### WARNING

Minor grammar, wording, formatting, or readability problems exist.

### FAIL

The answer is substantially unclear or difficult to understand.

---

## 8. Conciseness

The answer should provide enough information to answer the question without unnecessary repetition or unrelated detail.

The target is:

```text
Complete enough to be useful
+
Short enough for an interview response
```

### PASS

The answer is appropriately focused.

### WARNING

The answer contains noticeable repetition or unnecessary detail.

### FAIL

The answer is excessively verbose or substantially distracted from the question.

---

# 9. Format Compliance

The answer should follow an explicitly requested response format.

V1 supports basic format observation only.

Initial format types:

```text
GENERAL_TEXT
PROSE
CODE
BULLET_LIST
JSON
TABLE
UNKNOWN
```

Examples:

```text
"Tell me about the project."
→ GENERAL_TEXT / PROSE

"Show me the solving function."
→ CODE

"Give me the key points."
→ BULLET_LIST
```

Format compliance is evaluated by comparing:

```text
Requested format
        ↓
Observed answer format
```

### PASS

The answer generally follows the requested format.

### WARNING

The answer is useful but does not fully follow the requested format.

### FAIL

The requested format is explicitly required and the answer substantially violates it.

V1 should use deterministic structural observation where practical.

Do not introduce an additional LLM call solely for format detection or evaluation.

---

# Status Semantics

## PASS

The requirement is satisfied.

## WARNING

The answer was produced and is usable, but a quality weakness was observed.

## FAIL

The requirement has a fundamental violation.

A warning in one dimension does not automatically mean the entire answer execution failed.

---

# V1 Evaluation Principles

## One Real Execution

Answer evaluation must not execute the agent again.

```text
agent.run(...)
     ↓
actual final answer
     ↓
evaluate
```

There must be no second generation merely for evaluation.

---

## Deterministic First

Deterministic checks should remain deterministic.

Use Python-based observation for things such as:

* empty answer
* obvious formatting structure
* code fences
* JSON structure
* bullet structure
* basic answer properties

Do not introduce an LLM judge unless a demonstrated evaluation requirement cannot be handled adequately with deterministic methods.

---

## Evidence Is the Boundary

The evaluator should use:

```text
Recruiter Question
+
Final Answer
+
Retrieved Candidate Evidence
```

to evaluate candidate-specific grounding.

The evaluator must not assume that general model knowledge represents candidate experience.

---

## No Arbitrary Quality Score in V1

V1 does not define a numerical score such as:

```text
72/100
```

Instead, report individual dimensions:

```text
Existence: PASS
Relevance: PASS
Grounding: PASS
Coverage: WARNING
Unsupported Claims: WARNING
Candidate Voice: PASS
Clarity: PASS
Conciseness: PASS
Format: PASS
```

This provides actionable diagnostics without implying unsupported precision.

---

# Example

Question:

```text
Tell me about my Sudoku solver project.
```

Answer:

```text
I designed and implemented a Sudoku solver project using
backtracking and constraint propagation. The project involves
finding valid candidates for a cell, checking row, column,
and 3x3 grid constraints, and using backtracking to solve
the puzzle.
```

Possible evaluation:

```text
Existence: PASS
Relevance: PASS
Grounding: PASS
Question Coverage: PASS
Unsupported Claims: WARNING
Candidate Voice: PASS
Clarity: PASS
Conciseness: PASS
Format Compliance: PASS
```

The ownership statement:

```text
"I designed and implemented..."
```

should only be considered fully grounded if the candidate evidence supports that claim.

---

# Future Extensions

The V1 contract is intentionally small.

Future versions may add:

* richer format detection
* code-quality evaluation
* structured response requirements
* deeper completeness analysis
* answer consistency checks
* evaluation datasets
* persisted evaluation results
* typed evaluation schemas
* automated quality scoring
* model-based evaluation where justified

These should be introduced only when demonstrated requirements justify the additional complexity.

---

# Design Principle

The Answer stage should remain:

```text
Observe
→ Evaluate
→ Diagnose
→ Improve
```

rather than becoming another answer-generation system.

Complexity must earn its place through demonstrated requirements.

```

This is the **specification only**. After saving it as `answer_quality.md`, **Task 1 is complete**. Then we can implement Task 2 against this contract without prematurely introducing Pydantic, registries, or another LLM.
```
