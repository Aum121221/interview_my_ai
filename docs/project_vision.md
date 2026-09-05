# Interview My AI — Project Vision

## 1. What Are We Building?

**Interview My AI** is an AI-powered personal portfolio that allows a recruiter, interviewer, or visitor to interact with an AI version of a candidate.

The AI represents the candidate and answers questions using the candidate's own knowledge base.

The goal is not to build another generic chatbot.

The goal is to create a portfolio where:

```text
Portfolio
   +
Candidate knowledge
   +
AI interview experience
   =
A more interactive way to understand a person
```

The portfolio communicates what the candidate has built.

The AI interview experience allows a visitor to ask deeper questions about that candidate.

---

## 2. The Core Experience

The primary experience is:

```text
Visitor
   ↓
Explores portfolio
   ↓
Finds projects / skills / experience
   ↓
Wants to know more
   ↓
Talks to the AI version of the candidate
   ↓
AI answers using candidate knowledge
```

The portfolio and the AI interview experience should feel like parts of the same product.

They should not feel like two unrelated applications.

---

## 3. The AI Is the Candidate

The AI speaks in the candidate's first-person voice.

For example:

> "I built this project to..."

rather than:

> "The candidate built this project..."

The AI represents the candidate's perspective.

However, representation does not mean invention.

The AI must remain grounded in the candidate's actual knowledge base.

---

## 4. Knowledge Is the Source of Truth

Candidate-specific claims should come from the candidate's knowledge base.

This includes information such as:

* Projects
* Skills
* Education
* Experience
* Achievements
* Certifications
* Technical decisions
* Challenges
* Project details
* Personal development experiences

The AI should not invent information that is not supported by the knowledge base.

If information is unavailable, the AI should acknowledge that it is unavailable rather than creating an answer.

---

## 5. Knowledge Is Not the Same as Expertise

The system may use general technical knowledge when explaining general concepts.

For example, the AI can explain what a technology does.

But it must not turn general knowledge into a claim about the candidate.

There is an important distinction:

```text
General knowledge
        ≠
Candidate experience
```

A contributor should preserve this boundary when modifying the AI system.

---

## 6. Missing Information Is Not Negative Information

If the knowledge base does not contain information about something, that does not prove that the candidate:

* never did it
* does not know it
* lacks the skill
* has no experience with it

The correct interpretation is simply:

```text
Information unavailable in the current knowledge base.
```

This distinction is important for the trustworthiness of the system.

---

## 7. The AI Architecture

The agent follows the project's simple reasoning model:

```text
Think → Act → Observe
```

The LLM reasons.

Tools perform actions.

Observations provide information for the next reasoning step.

The project uses Hugging Face's `smolagents` `ToolCallingAgent` rather than maintaining a custom agent loop.

The V1 system intentionally keeps the agent simple.

The current architecture centers around:

```text
User Question
      ↓
ToolCallingAgent
      ↓
Candidate Knowledge Search
      ↓
Evidence
      ↓
LLM Reasoning
      ↓
Candidate Answer
```

The agent is the reasoning layer around the task.

It is not the entire application.

---

## 8. The Portfolio Is More Than the Agent

The project contains normal software around the AI.

For example:

```text
UI
 ↓
Application
 ↓
Agent
 ↓
Tools
 ↓
Knowledge / Data
```

Not every problem should be solved by the LLM.

Deterministic work should remain deterministic.

This keeps the system understandable and reliable.

---

## 9. The V1 Philosophy

V1 should remain intentionally small.

The goal is not to demonstrate how many technologies can be used.

The goal is to prove that the core experience works.

V1 prioritizes:

* A useful portfolio
* A working AI interview experience
* Evidence-grounded candidate answers
* Reliable knowledge retrieval
* A simple contributor-friendly architecture
* A clean and usable interface

Features should earn their place by providing meaningful value.

---

## 10. What We Want Contributors to Improve

Contributors can improve any part of the product when there is a clear reason.

Potential areas include:

### Portfolio Experience

* Visual design
* Navigation
* Project presentation
* About section
* Skills presentation
* Experience
* Education
* GitHub integration
* Responsive design
* Accessibility
* Performance

### Interview Experience

* Interview UI
* Conversation experience
* Starter questions
* Loading states
* Error states
* AI avatar
* Response presentation
* Conversation usability

### Engineering

* Retrieval
* Evaluation
* Testing
* Developer experience
* Documentation
* Reliability
* Performance
* Security

These are examples, not a fixed feature list.

Contributors are encouraged to propose better ideas.

---

## 11. Freedom to Experiment

Different contributors may have different visions for the interface or user experience.

That is expected.

For example, one contributor may propose:

```text
Minimal portfolio
```

while another proposes:

```text
Interactive portfolio
```

and another proposes:

```text
Terminal-inspired portfolio
```

The project does not require contributors to independently arrive at the same design.

Instead, ideas should be discussed and evaluated against the project's principles.

---

## 12. How Ideas Are Evaluated

A contribution should be evaluated based on:

### User Value

Does it make the portfolio or interview experience meaningfully better?

### Simplicity

Is this the simplest reasonable way to achieve the goal?

### Architecture Fit

Does it respect the existing boundaries?

### Maintainability

Can future contributors understand and modify it?

### Performance

Does it introduce unnecessary runtime or frontend cost?

### Accessibility

Can different users interact with it effectively?

### Security

Does it introduce new risks or weaken existing boundaries?

### Long-Term Value

Will the contribution remain useful as the project grows?

A visually impressive feature is not automatically a good feature.

A technically sophisticated implementation is not automatically a good implementation.

---

## 13. Complexity Must Earn Its Place

We prefer:

```text
Simple solution
      ↓
Measure
      ↓
Identify real limitation
      ↓
Improve
```

rather than:

```text
Predict every future problem
      ↓
Build abstraction
      ↓
Build another abstraction
      ↓
Add framework
      ↓
Add infrastructure
```

The project should evolve from real needs.

---

## 14. What This Project Is Not

Interview My AI is not intended to become:

* A generic autonomous agent platform
* A candidate-ranking system
* An unnecessarily complex multi-agent framework
* A collection of unrelated AI demos
* A frontend framework showcase
* A system that fabricates candidate achievements
* An architecture where every feature requires an LLM

The project should remain focused on its central experience.

---

## 15. Product Direction

The long-term vision is to make a personal portfolio more interactive.

A visitor should be able to:

```text
See what someone has built
        ↓
Understand their background
        ↓
Explore their work
        ↓
Ask questions
        ↓
Receive grounded answers
        ↓
Form a better understanding of the person
```

The AI should enhance the portfolio rather than replace the portfolio.

---

## 16. Contributor Principle

Contributors should think like product builders, not task executors.

Before implementing something, ask:

> What problem am I solving?

Then:

> Is this the simplest useful solution?

Then:

> Does it fit Interview My AI?

Then:

> Can another contributor understand what I changed?

If the answer to these questions is yes, the contribution is likely moving in the right direction.

---

## 17. The North Star

The project can be summarized as:

> **A personal portfolio that can explain itself through an AI version of the person who built it.**

Everything we build should strengthen that experience.

---

## 18. Repository

The repository is the canonical source for the current implementation, architecture, decisions, and contribution guidelines.

**Interview My AI**

https://github.com/Aum121221/interview_my_ai

Before beginning significant work, always check the latest version of the repository and its documentation.

---

## 19. Final Principle

> **Build the simplest system that makes the portfolio more useful, more understandable, and more human to interact with.**

Bring your own ideas.

Experiment at the edges.

Respect the core.

Keep complexity justified.

Build something the next contributor can understand.
