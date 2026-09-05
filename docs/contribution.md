# Contributing to Interview My AI

Thank you for contributing to **Interview My AI**.

Interview My AI is an open-source project that builds an AI-powered personal portfolio where an AI version of the candidate can answer recruiter-style interview questions using the candidate's own knowledge base.

The project is intentionally built around a simple principle:

> **Build the simplest system that solves the real problem.**

We welcome different ideas, designs, implementations, and improvements. Contributors are encouraged to bring their own ideas rather than simply following a fixed list of tasks.

At the same time, contributions should respect the project's architecture, boundaries, and engineering principles.

---

## 1. Start Here

Before contributing, first understand the project.

**Repository:**

https://github.com/Aum121221/interview_my_ai

Read these documents in order:

1. `README.md`
2. `docs/PROJECT_VISION.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DECISION_PROCESS.md`
5. Relevant contributor guide for the area you want to work on

If you are working on the frontend, also read:

```text
frontend/FRONTEND_VISION.md
```

The repository is the source of truth for the current implementation and contribution guidelines.

---

## 2. Understand the Project Before Changing It

Please do not start by rewriting or restructuring the project.

First understand:

```text
What problem are we solving?
        ↓
What is the current architecture?
        ↓
Where does the change belong?
        ↓
What is the smallest useful change?
        ↓
How can it be evaluated?
```

Prefer extending the existing system over introducing a parallel system.

Before proposing a large architectural change, discuss it first.

---

## 3. Our Engineering Philosophy

The project follows a simple engineering philosophy:

* Start with the simplest working solution.
* Reuse existing abstractions.
* Keep modules focused.
* Keep deterministic work outside the LLM.
* Keep the agent responsible for reasoning.
* Keep tools responsible for actions.
* Avoid unnecessary abstraction.
* Avoid unnecessary dependencies.
* Avoid premature optimization.
* Preserve clear data and source boundaries.
* Make changes small and understandable.
* Measure before adding complexity.

A contribution should make the project easier to understand, maintain, or extend — not merely make it larger.

---

## 4. Bring Your Own Ideas

We want contributors to contribute ideas, not just code.

You may propose:

* A new frontend interaction
* A different portfolio layout
* A better interview experience
* A new visualization
* A usability improvement
* An accessibility improvement
* A performance improvement
* A developer-experience improvement
* A testing improvement
* A documentation improvement
* A new approach to an existing problem

Different contributors may have completely different ideas.

That is okay.

We do not expect every contribution to look identical.

What matters is whether the idea:

1. Solves a real problem
2. Fits the project's direction
3. Respects the architecture
4. Adds justified complexity
5. Can be maintained by future contributors

---

## 5. Propose Before Building Large Features

For a significant feature, please open a proposal before implementing it.

A proposal should explain:

```text
Idea
Problem
Proposed solution
User experience
Why this approach?
Alternatives considered
Expected project impact
New dependencies, if any
```

Small fixes do not require a proposal.

For larger changes, discussion before implementation helps prevent duplicated work and unnecessary rewrites.

---

## 6. Project Boundaries

Some parts of the project are intentionally stable.

In particular, contributors should not casually change:

* The core agent architecture
* The source-of-truth rules for candidate information
* Knowledge retrieval boundaries
* Security-sensitive configuration
* Existing project decisions
* Core ingestion behavior
* Dependencies without justification

If you believe one of these areas genuinely needs to change, explain why in the proposal or issue.

Architectural changes require stronger justification than normal feature changes.

---

## 7. Avoid Unnecessary Complexity

Before adding a new library, framework, abstraction, service, or module, ask:

> **Can the existing project solve this problem without it?**

Prefer:

```text
existing abstraction
        ↓
small extension
```

over:

```text
existing abstraction
        +
new framework
        +
new abstraction layer
        +
new service
```

Every new piece of complexity should have a clear reason.

---

## 8. Working With the Repository

Clone the repository:

```bash
git clone https://github.com/Aum121221/interview_my_ai.git
cd interview_my_ai
```

Create your development environment according to the instructions in `README.md`.

Before making changes:

```bash
git pull
```

Create a focused branch:

```bash
git checkout -b feature/your-feature-name
```

Keep each branch focused on one meaningful change.

---

## 9. Make Small Changes

Prefer small, reviewable changes.

Good:

```text
Add project-card interaction
```

Less desirable:

```text
Rewrite entire frontend
+ change routing
+ introduce new framework
+ redesign backend
+ modify agent
```

If a feature requires several independent changes, split them into separate issues or pull requests where practical.

---

## 10. Test Your Changes

Before opening a pull request:

* Run the relevant tests.
* Verify the affected functionality locally.
* Check that existing functionality still works.
* Check imports and configuration.
* Check error and empty states where relevant.
* Remove debugging code.
* Remove unnecessary files or dependencies.

Do not add tests merely to increase test count.

Tests should provide useful confidence.

---

## 11. Pull Requests

When your work is ready:

```bash
git status
git add .
git commit -m "Describe the change"
git push -u origin your-branch-name
```

Then open a pull request against the repository's main development branch.

Your pull request should explain:

```text
What changed?
Why was it changed?
How does it work?
How was it tested?
Are there any tradeoffs?
```

Keep the pull request focused.

---

## 12. Review Process

A pull request may be:

```text
Submitted
   ↓
Reviewed
   ↓
Changes requested
   ↓
Updated
   ↓
Approved
   ↓
Merged
```

Review feedback is part of the development process.

A requested change does not necessarily mean the idea is wrong.

The goal is to make the contribution fit the project while preserving the contributor's useful idea.

---

## 13. Different Ideas Are Welcome

Two contributors may solve the same problem differently.

For example:

```text
Contributor A
→ Minimal portfolio design

Contributor B
→ Interactive portfolio design

Contributor C
→ Experimental visual design
```

The project does not automatically prefer the first idea simply because it was proposed first.

Evaluate ideas based on:

* User value
* Simplicity
* Maintainability
* Architecture fit
* Performance
* Accessibility
* Security
* Long-term usefulness

The project lead may accept one approach, combine ideas, defer an idea, or reject an idea.

---

## 14. Decisions

Important architectural or product decisions should be documented.

Before introducing a significant change, check:

```text
docs/DECISIONS.md
```

If a new decision changes the project's direction, document the reasoning so future contributors understand why it was made.

We want to avoid repeatedly having the same architectural discussion.

---

## 15. Contributor Freedom

The project provides boundaries, not a script.

You are encouraged to:

* Think independently.
* Suggest improvements.
* Challenge existing approaches.
* Experiment.
* Bring design ideas.
* Improve usability.
* Improve developer experience.

But experiments should eventually become clear, maintainable contributions if they are accepted into the main project.

---

## 16. When in Doubt

If you are unsure whether something belongs in the project:

**Ask before making a large change.**

A short discussion is usually better than a large pull request that has to be completely redesigned.

---

## 17. The Core Rule

Remember:

> **Freedom at the edges, discipline at the core.**

Bring your ideas.

Respect the architecture.

Keep the implementation simple.

Make the project better for the next contributor, not just for yourself.

---

## 18. Stay Up to Date

The repository contains the latest contribution rules and project decisions.

Always check the current repository before starting work:

https://github.com/Aum121221/interview_my_ai

Guidelines and architecture may evolve as the project grows.

Thank you for contributing to Interview My AI.
