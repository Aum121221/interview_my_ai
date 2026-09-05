# Interview My AI — Decision Process

## 1. Purpose

Interview My AI is an open-source project where different contributors may bring different ideas.

This is intentional.

One contributor may propose a minimal interface.

Another may propose an interactive experience.

Another may propose a completely different approach to the interview experience.

The project should be open to these ideas while maintaining a coherent product and architecture.

This document explains how ideas move from:

```text
Idea
 ↓
Proposal
 ↓
Discussion
 ↓
Decision
 ↓
Implementation
 ↓
Review
 ↓
Merge
```

The goal is not to control creativity.

The goal is to make creativity manageable.

---

# 2. Core Principle

> **Freedom at the edges, discipline at the core.**

Contributors are encouraged to challenge existing approaches and propose new ones.

However, accepted contributions should continue to respect:

* Project vision
* Architecture
* Simplicity
* Maintainability
* Security
* Source boundaries
* User value

A contributor does not need permission to have an idea.

A significant change does need a shared decision before substantial implementation begins.

---

# 3. Types of Decisions

Not every change requires the same level of discussion.

We broadly divide contributions into three categories.

## Small Changes

Examples:

* Bug fixes
* Documentation corrections
* Small UI improvements
* Minor styling changes
* Small test improvements
* Simple refactors with no behavior change

These can usually move directly to implementation.

```text
Small change
   ↓
Issue / PR
   ↓
Review
   ↓
Merge
```

---

## Medium Changes

Examples:

* New portfolio section
* New interview UI interaction
* New retrieval behavior
* Significant UI redesign
* New user-facing feature
* Meaningful dependency addition

These should generally have an issue or proposal before implementation.

```text
Idea
 ↓
Issue / Proposal
 ↓
Discussion
 ↓
Implementation
 ↓
PR
```

---

## Large / Architectural Changes

Examples:

* Changing the agent framework
* Introducing multiple agents
* Replacing the retrieval architecture
* Replacing the frontend architecture
* Introducing a new backend service
* Adding persistent memory
* Major database changes
* Introducing a new framework

These require explicit discussion before implementation.

```text
Proposal
 ↓
Architecture discussion
 ↓
Decision
 ↓
Implementation
 ↓
PR
 ↓
Review
```

Do not implement a major architectural change first and ask for approval afterward.

---

# 4. Start With the Problem

A proposal should begin with the problem, not the technology.

Prefer:

> "The current interview experience makes it difficult for users to understand what they can ask."

over:

> "We should add framework X."

First understand the problem.

Then evaluate possible solutions.

---

# 5. Proposal Questions

For a significant proposal, answer:

```text
What problem are we solving?

Who experiences this problem?

What is the proposed solution?

Why is this useful?

What alternatives were considered?

Why is this approach better?

What part of the architecture changes?

Does it introduce a dependency?

What complexity does it introduce?

How can we evaluate whether it worked?
```

The proposal does not need to be perfect.

Its purpose is to make the reasoning visible.

---

# 6. Multiple Ideas Are Welcome

Different contributors may propose different solutions to the same problem.

For example:

```text
Problem:
Portfolio navigation feels difficult.

Proposal A:
Sidebar navigation.

Proposal B:
Command palette.

Proposal C:
Scroll-based navigation.

Proposal D:
Interactive visual navigation.
```

Do not automatically choose the first proposal.

Compare the ideas.

Consider:

* User experience
* Simplicity
* Accessibility
* Performance
* Maintainability
* Architecture fit
* Implementation cost
* Long-term usefulness

---

# 7. Combining Ideas

Sometimes the best solution is not one proposal.

Two or more proposals may contain useful ideas.

For example:

```text
Proposal A
→ Excellent navigation structure

Proposal B
→ Excellent visual interaction

Final solution
→ Navigation structure from A
   +
   useful interaction from B
```

Contributors should be open to combining ideas rather than treating proposals as competitions.

---

# 8. Project Lead Responsibility

The project lead is responsible for maintaining the overall direction of the project.

The project lead may:

* Accept a proposal
* Request changes
* Combine proposals
* Defer a proposal
* Reject a proposal
* Ask for an experiment
* Request additional evidence

The purpose is not to control contributors.

The purpose is to protect the project's coherence.

---

# 9. Decision Criteria

When evaluating a proposal, consider the following.

## 9.1 User Value

Does this make Interview My AI meaningfully better?

A technically interesting feature without meaningful user value may not justify implementation.

---

## 9.2 Simplicity

Can the same result be achieved more simply?

Prefer the simplest useful solution.

---

## 9.3 Architecture Fit

Does the idea fit the existing architecture?

If not, is the architectural change genuinely justified?

---

## 9.4 Maintainability

Can another contributor understand and modify the implementation later?

---

## 9.5 Complexity Cost

What new complexity does the proposal introduce?

Consider:

* New files
* New abstractions
* New dependencies
* New services
* New configuration
* New failure modes
* New maintenance requirements

---

## 9.6 Performance

Does the feature introduce unnecessary:

* Runtime cost
* Network requests
* Bundle size
* Memory usage
* Database load

---

## 9.7 Accessibility

Can users with different devices and abilities use the feature effectively?

Accessibility is part of product quality, not an optional decoration.

---

## 9.8 Security

Does the change introduce new access paths, data exposure, dependencies, or configuration risks?

Security-sensitive changes require additional care.

---

## 9.9 Evidence

For uncertain technical decisions, prefer experimentation over speculation.

For example:

```text
Question:
Does BM25 improve retrieval?

       ↓

Experiment

       ↓

Measure

       ↓

Decision
```

The same principle can apply to UI ideas:

```text
Question:
Does this interaction improve usability?

       ↓

Prototype

       ↓

Test

       ↓

Decision
```

---

# 10. Decision Outcomes

A proposal normally receives one of four outcomes.

## Accepted

The idea fits the project and should proceed.

```text
ACCEPTED
```

The contributor can implement it according to the agreed scope.

---

## Accepted With Changes

The core idea is useful, but the proposed implementation needs adjustment.

```text
ACCEPTED — CHANGES REQUESTED
```

The contributor and project lead refine the scope before implementation.

---

## Deferred

The idea is potentially valuable but is not currently a priority.

```text
DEFERRED
```

A deferred idea is not necessarily a bad idea.

It may become appropriate later.

Possible reasons:

* V1 is not ready
* Another dependency must be completed first
* The current architecture is not ready
* More evidence is needed
* The feature is better suited to a later milestone

---

## Rejected

The proposal should not become part of the project in its current form.

```text
REJECTED
```

Possible reasons:

* Doesn't solve an important problem
* Adds too much complexity
* Conflicts with project direction
* Duplicates existing functionality
* Introduces unacceptable maintenance cost
* Creates security concerns

A rejection should ideally include a short reason.

---

# 11. Do Not Take Rejection Personally

A rejected proposal is not a judgment of the contributor.

The project evaluates ideas against the needs and direction of the project.

A good idea can still be wrong for the current project.

A proposal may also be rejected in its current form and later become useful after the project changes.

---

# 12. Experiments Before Decisions

When the team is uncertain, use a small experiment.

For example:

```text
Proposal:
Use a new retrieval strategy.

       ↓

Small experiment

       ↓

Compare against current retrieval

       ↓

Evaluate results

       ↓

Decide
```

The experiment should be smaller than the final implementation.

Do not build an entire production system just to discover whether an idea works.

---

# 13. Architectural Decisions

If an accepted proposal changes an important architectural boundary, document the decision.

The record should explain:

```text
Decision
Context
Problem
Options considered
Chosen approach
Why
Tradeoffs
Consequences
```

This creates project memory.

Future contributors should be able to understand not only **what** the architecture is, but **why** it became that way.

---

# 14. Avoid Reopening Settled Decisions Without a Reason

Existing decisions should not be changed simply because a contributor prefers another style.

Revisit a decision when there is new evidence.

Good reasons include:

* New requirements
* Demonstrated limitations
* Significant performance problems
* Security concerns
* Better measured results
* Important changes in project direction

Prefer:

```text
Old decision
     ↓
New evidence
     ↓
Re-evaluation
```

rather than:

```text
I prefer another approach
     ↓
Rewrite everything
```

---

# 15. Decision Scope

Decisions should be made at the smallest appropriate level.

A contributor should not need project-wide approval for a small styling change.

Likewise, a project-wide architectural change should not be hidden inside an ordinary pull request.

Use the smallest process that provides enough confidence.

---

# 16. Implementation After Approval

Once a significant proposal is accepted:

```text
Proposal
   ↓
Decision
   ↓
Issue
   ↓
Implementation
   ↓
Pull Request
```

The implementation should remain reasonably close to the accepted scope.

If implementation reveals a substantially different problem or solution, pause and discuss the change rather than silently expanding the scope.

---

# 17. Pull Request Review

Approval of an idea does not automatically mean approval of the implementation.

The pull request still needs to be reviewed for:

* Correctness
* Code quality
* Architecture
* Testing
* Security
* Performance
* Maintainability
* Scope

Think of these as two different questions:

```text
Proposal:
Should we build this?

Pull Request:
Did we build it well?
```

---

# 18. Avoid Scope Creep

A contributor may discover additional improvements while implementing a feature.

That is useful.

But unrelated improvements should generally become separate issues.

For example:

```text
Original:
Improve project cards

Discovered:
Navigation needs redesign
Database query can be optimized
Agent instructions could be improved
```

Do not automatically combine all four changes into one pull request.

Create follow-up issues where appropriate.

---

# 19. Contributor Ownership

Contributors should receive credit for their ideas and implementations.

When an idea evolves through discussion or combines multiple contributions, acknowledge the relevant contributors.

Open-source collaboration should reward both:

```text
Ideas
+
Implementation
```

---

# 20. Project Evolution

The decision process itself may evolve.

As the contributor community grows, the project may introduce:

* Maintainers
* Area owners
* Reviewers
* Design discussions
* Architecture reviews
* RFCs
* Milestones

Do not introduce these systems before they are needed.

Start simple.

Add process when the project's size creates a real need.

---

# 21. Decision Summary

The process can be summarized as:

```text
                 CONTRIBUTOR
                      │
                      ↓
                    IDEA
                      │
                      ↓
                  PROPOSAL
                      │
                      ↓
                 DISCUSSION
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       ACCEPT       DEFER       REJECT
          │           │
          ↓           │
      IMPLEMENT       │
          │           │
          ↓           │
           PR         │
          │           │
          ↓           │
        REVIEW        │
          │           │
          ↓           │
         MERGE        │
                      │
                 Revisit later
```

---

# 22. The Principle Behind the Process

The project should not become:

> "The project lead tells everyone what to build."

Nor should it become:

> "Everyone changes whatever they want."

Instead:

> **Contributors bring ideas. The project evaluates them. The best ideas become focused work.**

That balance allows the project to remain open to creativity without losing its identity.

---

## Repository

Always check the latest project guidelines and implementation here:

https://github.com/Aum121221/interview_my_ai

The repository is the canonical source for current project decisions.

---

## Final Rule

> **Bring the idea. Explain the problem. Discuss the tradeoffs. Keep the solution simple. Then build it well.**
