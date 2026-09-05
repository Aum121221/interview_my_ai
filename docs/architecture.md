# Interview My AI — Architecture

## 1. Purpose

This document explains the current architecture of **Interview My AI** and the responsibilities of its major parts.

The goal is not to prescribe how every feature must be implemented.

The goal is to provide clear boundaries so contributors can introduce their own ideas without accidentally mixing unrelated responsibilities.

The repository is the source of truth for the current implementation.

---

## 2. Core Architecture

The project is organized around a simple flow:

```text
Candidate Sources
       ↓
   Ingestion
       ↓
Knowledge Base
       ↓
   Retrieval
       ↓
     Tool
       ↓
     Agent
       ↓
      UI
       ↓
     User
```

The AI reasoning layer sits inside a larger normal software system.

The agent is not the entire application.

---

## 3. Current Repository Structure

The project is organized approximately as:

```text
interview_my_ai/
│
├── app.py
│
├── config/
│   ├── settings.py
│   └── source_map.json
│
├── ingestion/
│   ├── scanner.py
│   ├── loaders.py
│   ├── processor.py
│   ├── build_knowledge.py
│   └── vector_store.py
│
├── agent/
│   ├── instructions.py
│   ├── tools.py
│   └── core.py
│
├── ui/
│   └── interview.py
│
├── experiments/
│   ├── test_model.py
│   ├── test_retrieval.py
│   └── test_agent.py
│
├── tests/
│   └── test_scanner.py
│
├── scripts/
│   └── ingest_vectors.py
│
├── data/
│   └── knowledge.jsonl
│
├── .streamlit/
│   └── secrets.toml
│
├── requirements.txt
│
└── README.md
```

The exact repository structure may evolve.

When making a contribution, check the current repository before assuming a file or directory still exists.

---

# 4. Application Layer

## `app.py`

`app.py` is the application entrypoint and orchestration layer.

Its job is to connect the major pieces of the application.

Conceptually:

```text
Configuration
      ↓
Agent setup
      ↓
UI
```

Keep `app.py` small.

Do not turn it into a place where unrelated business logic accumulates.

If a piece of logic has a clear independent responsibility, it should generally live in the appropriate module instead.

---

# 5. Configuration

## `config/`

Configuration belongs here.

Examples include:

* Environment-based settings
* Model configuration
* Database configuration
* Embedding configuration
* Source mapping

### `settings.py`

Centralizes application configuration.

Avoid scattering environment-variable reads throughout the codebase.

### `source_map.json`

Defines what candidate source material is allowed to enter the ingestion pipeline.

The source boundary is intentional.

Contributors should not casually bypass it.

---

# 6. Ingestion Layer

## `ingestion/`

The ingestion layer converts candidate source material into usable knowledge.

The conceptual pipeline is:

```text
Source files
     ↓
Scanner
     ↓
Loader
     ↓
Processor
     ↓
Knowledge records
     ↓
Vector store
```

Each stage has a focused responsibility.

---

## `scanner.py`

The scanner determines which files are allowed to enter the pipeline.

It should answer:

> Which files should be processed?

It should not be responsible for understanding the contents of those files.

---

## `loaders.py`

Loaders extract raw text from supported file types.

Examples include:

```text
Markdown
PDF
Text
Python
```

The loader answers:

> What text can we extract from this file?

It should not decide what the text means.

---

## `processor.py`

The processor handles transformations such as:

* Cleaning
* Classification
* Chunking
* Metadata
* Stable identifiers
* Provenance

The processor converts extracted material into structured knowledge records.

---

## `build_knowledge.py`

Builds the knowledge dataset from the ingestion pipeline.

The resulting knowledge is stored in:

```text
data/knowledge.jsonl
```

The exact CLI behavior should always be checked against the current implementation rather than assumed from this document.

---

## `vector_store.py`

This module contains the knowledge retrieval/storage logic.

The current retrieval design combines:

```text
Semantic vector search
        +
BM25 lexical search
```

BM25 is intentionally kept within the existing vector-store/retrieval boundary rather than creating a separate module solely for BM25.

The project currently uses:

* Gemini embeddings
* Supabase PostgreSQL
* pgvector
* BM25

The current embedding configuration uses the Gemini embedding model configured by the project, with 768-dimensional embeddings.

---

# 7. Knowledge Boundary

The knowledge base is the source of truth for candidate-specific claims.

This is a critical architectural boundary.

The system should distinguish:

```text
Candidate knowledge
        ≠
General technical knowledge
```

Candidate-specific information must remain grounded in candidate source material.

General technical knowledge may be used for general explanations, but should not silently become candidate experience.

---

# 8. Agent Layer

## `agent/`

The agent layer contains the reasoning system.

The current implementation uses Hugging Face `smolagents` and specifically a `ToolCallingAgent`.

The architecture intentionally does **not** maintain a custom ReAct loop.

The agent framework owns the agent loop.

Conceptually:

```text
Question
   ↓
ToolCallingAgent
   ↓
Tool selection
   ↓
Tool execution
   ↓
Observation
   ↓
Reasoning
   ↓
Answer
```

---

## `instructions.py`

Contains the agent's behavioral instructions.

This is where the system defines important rules such as:

* Candidate first-person voice
* Evidence grounding
* Handling missing information
* Separation of candidate experience from general knowledge

Instructions should remain focused on agent behavior.

---

## `tools.py`

Contains tools available to the agent.

V1 intentionally keeps the tool surface small.

The primary knowledge tool is:

```text
candidate_knowledge_search
```

A tool should have a narrow responsibility.

Avoid creating a tool for something the agent does not actually need.

---

## `core.py`

Responsible for constructing/configuring the agent.

The agent should remain a relatively small reasoning layer around the task.

Do not place UI logic, database ingestion logic, or unrelated application behavior here.

---

# 9. Agent Complexity

The current V1 agent is intentionally constrained.

Current principles include:

```text
ToolCallingAgent
      +
Candidate knowledge search
      +
Limited steps
      +
No unnecessary planning
```

The project does not currently require a multi-agent architecture.

Do not introduce multiple agents simply because the framework makes it possible.

Additional agent complexity should only be introduced when a demonstrated problem requires it.

---

# 10. UI Layer

## `ui/`

The UI is responsible for the user-facing experience.

For the current application:

```text
ui/interview.py
```

contains the interview interface.

The UI should handle things such as:

* Displaying the conversation
* Accepting user questions
* Showing agent responses
* Loading states
* Error states
* Empty states
* User interaction

The UI should not contain retrieval implementation.

The UI should not directly implement agent reasoning.

---

# 11. Session Memory

The interview experience uses session-only conversation memory.

The agent instance should remain available through the Streamlit session state.

Conceptually:

```text
Streamlit session
       ↓
Agent instance
       ↓
Question 1
       ↓
Question 2
       ↓
Question 3
```

The interview interface calls the existing agent while preserving the conversation context.

Contributors should not introduce a persistent memory system unless there is a clearly demonstrated product requirement.

---

# 12. Experiments

## `experiments/`

Experiments are for testing ideas and evaluating behavior before making them part of the main system.

Examples:

```text
test_model.py
test_retrieval.py
test_agent.py
```

Use experiments to answer questions such as:

```text
Does this retrieval strategy work better?

Does this model improve answers?

Does this agent configuration solve the task?

Does this feature actually improve the user experience?
```

Experiments should not automatically become production architecture.

Measure first.

Then decide.

---

# 13. Tests

## `tests/`

Tests provide repeatable confidence in production behavior.

Use them for stable functionality that should continue working as the project evolves.

Do not confuse:

```text
experiment
```

with:

```text
production test
```

Experiments explore.

Tests protect known behavior.

---

# 14. Scripts

## `scripts/`

Scripts are used for operational or development workflows that should remain outside the application runtime.

For example:

```text
scripts/ingest_vectors.py
```

handles vector ingestion from the generated knowledge dataset.

Scripts should not become hidden application modules.

---

# 15. Data

## `data/`

Contains generated/local project data used by the development pipeline.

For example:

```text
data/knowledge.jsonl
```

represents processed knowledge records.

Do not manually edit generated data unless the workflow explicitly requires it.

The source material remains upstream of the generated knowledge.

---

# 16. Where Should My Contribution Go?

When you have an idea, first classify it.

```text
Is it configuration?
        ↓
     config/

Is it source ingestion?
        ↓
    ingestion/

Is it agent behavior?
        ↓
      agent/

Is it user interface?
        ↓
       ui/

Is it experimentation?
        ↓
   experiments/

Is it a production regression check?
        ↓
      tests/

Is it an operational workflow?
        ↓
     scripts/

Is it application orchestration?
        ↓
      app.py
```

If none of these categories fit, **do not immediately create a new directory**.

First discuss whether a new boundary is actually justified.

---

# 17. Do Not Duplicate Responsibilities

Avoid patterns such as:

```text
ui/
    retrieval.py

agent/
    database.py

ingestion/
    agent.py

another_retrieval_system/
```

when the existing architecture already has clear boundaries for those responsibilities.

Prefer using the existing module.

For example:

```text
UI
 ↓
Agent tool
 ↓
Vector store
```

rather than:

```text
UI
 ↓
Direct database query
 ↓
Custom retrieval
 ↓
Agent
 ↓
Another retrieval system
```

The second architecture creates competing paths and makes the system harder to understand.

---

# 18. When Is a New Module Justified?

A new module is justified when there is a real, stable responsibility that:

1. Does not naturally belong to an existing module.
2. Has a clear input and output.
3. Improves maintainability.
4. Is used by more than a trivial piece of code.
5. Reduces rather than increases conceptual complexity.

A new file is not automatically an improvement.

---

# 19. Frontend Contributions

Frontend contributors have more freedom in presentation.

They may introduce new:

* Layouts
* Components
* Animations
* Interactions
* Visual systems
* Portfolio sections
* Interview experiences

But frontend changes should preserve the application's existing backend and agent boundaries unless the proposal explicitly changes architecture.

The frontend should consume application capabilities rather than reimplement them.

Detailed frontend guidance belongs in:

```text
frontend/FRONTEND_VISION.md
```

---

# 20. Dependency Rule

Before adding a dependency:

```text
Can the existing project do this?
        ↓
      Yes
        ↓
Use the existing solution.

      No
        ↓
Is the new dependency worth its cost?
        ↓
Explain it in the proposal/PR.
```

Consider:

* Complexity
* Maintenance
* Bundle/runtime cost
* Security
* Compatibility
* Long-term value

A dependency should solve a real problem.

---

# 21. External Services

External services should remain behind clear boundaries.

For example:

```text
Agent
  ↓
Tool
  ↓
Retrieval layer
  ↓
Supabase
```

rather than allowing arbitrary parts of the application to directly depend on the database.

This keeps external infrastructure replaceable and the application easier to reason about.

---

# 22. Security and Source Boundaries

The candidate's source material is an intentional boundary.

Contributors must not create shortcuts that:

* Read excluded source folders
* Bypass `source_map.json`
* Expose private candidate material
* Hard-code secrets
* Commit API keys
* Circumvent configured access boundaries

Security-sensitive changes require additional review.

---

# 23. Architecture Change Rule

If a contribution changes the architecture itself, explain:

```text
Current problem
      ↓
Why current architecture is insufficient
      ↓
Proposed architecture
      ↓
Alternatives considered
      ↓
Complexity introduced
      ↓
Expected benefit
```

Do not introduce architectural changes simply because another architecture is fashionable.

---

# 24. Evolution of the Architecture

This architecture is not frozen forever.

It should evolve when real evidence shows that a change is necessary.

The preferred progression is:

```text
Simple implementation
        ↓
Real usage
        ↓
Observe limitation
        ↓
Measure / experiment
        ↓
Propose improvement
        ↓
Update architecture
```

Not:

```text
Imagine future problems
        ↓
Build infrastructure
        ↓
Hope it becomes useful
```

---

# 25. Architectural North Star

The architecture should remain:

```text
Simple
Readable
Composable
Testable
Evidence-grounded
Contributor-friendly
```

The most important question is not:

> "How sophisticated can we make the architecture?"

It is:

> **"What is the simplest architecture that reliably solves the problem we have today?"**

---

## Repository

Always check the latest repository before contributing:

https://github.com/Aum121221/interview_my_ai

The implementation may evolve beyond the examples in this document.

The repository and its latest decisions take precedence over assumptions.

---

## Final Rule

> **Put each responsibility in one clear place, reuse existing boundaries, and create new complexity only when the problem earns it.**
