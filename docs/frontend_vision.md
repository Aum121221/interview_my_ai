# Interview My AI — Frontend Vision

## 1. Purpose

The frontend is the part of Interview My AI that visitors directly experience.

It should make the candidate easy to understand, explore, and interact with.

This document defines the **frontend direction**, not a fixed visual design.

Contributors are encouraged to bring their own ideas for:

* Layout
* Visual style
* Interactions
* Animations
* Components
* Navigation
* Portfolio presentation
* Interview experience

The goal is to provide a common product direction while leaving room for creativity.

---

# 2. The Frontend Goal

The frontend should answer one simple question:

> **Can a visitor quickly understand who this person is, what they have built, and interact with their AI version?**

The experience should guide the visitor naturally:

```text id="4r9f6k"
Discover the person
       ↓
Understand their work
       ↓
Explore projects
       ↓
Learn about skills / experience
       ↓
Ask questions
       ↓
Interact with Interview My AI
```

The frontend should make this journey feel natural rather than forcing the visitor through a rigid sequence.

---

# 3. The Portfolio Is the Main Product Surface

The AI interview is an important part of the project, but it should not completely replace the portfolio.

The portfolio should remain useful even if a visitor never interacts with the AI.

A visitor should be able to understand:

* Who the person is
* What they do
* What they have built
* Their skills
* Their experience
* Their education
* Relevant links and work

The AI adds a deeper conversational layer.

---

# 4. Contributors Can Use Their Own Information

Frontend contributors may use their own information while developing and demonstrating their implementation.

For example:

```text id="3w1w9j"
Name
Profile photo
Bio
Projects
Skills
Experience
Education
GitHub
LinkedIn
Other links
```

This is encouraged when it helps contributors build and test a realistic portfolio.

However, contributor-specific content should not be confused with the reusable frontend implementation.

The reusable contribution is primarily:

```text id="ax5h5f"
Layout
+
Components
+
Interaction
+
Animation
+
Responsive behavior
+
Accessibility
+
Frontend logic
```

Content should remain replaceable.

---

# 5. Separate Content From Presentation

A contributor should be able to replace:

```text id="6w3q9e"
Name A
   ↓
Name B
```

without rebuilding:

```text id="b2q7cn"
Portfolio layout
Navigation
Project cards
Animations
Responsive behavior
```

Prefer structures where content can change independently from presentation.

The exact implementation may vary depending on the frontend architecture, but the principle should remain:

> **Reusable layout, replaceable content.**

---

# 6. Frontend Freedom

There is no single mandatory visual style.

Contributors may explore different directions such as:

```text id="5m9l4k"
Minimal
Editorial
Modern
Technical
Terminal-inspired
Interactive
Experimental
Visual
```

These are examples, not requirements.

A contributor should be able to propose a different direction if they can explain why it improves the product.

---

# 7. The Experience Matters More Than the Trend

Do not add a design pattern simply because it is popular.

A visual or interaction choice should serve a purpose.

Ask:

```text id="0a1v7j"
Does it improve understanding?
Does it improve navigation?
Does it improve interaction?
Does it make the product memorable?
Does it remain usable?
```

If the answer is no, the feature may not be necessary.

---

# 8. Suggested Portfolio Structure

The portfolio may contain sections such as:

```text id="7m2q0c"
Hero
About
Projects
Skills
Experience
Education
GitHub / Work
Interview My AI
Contact / Links
```

This is a suggested information architecture, not a requirement that every contributor implement the exact same layout.

A contributor may propose a different structure if it creates a better experience.

---

# 9. Hero

The first screen should quickly communicate:

```text id="kj6t8z"
Who is this person?
What do they do?
What have they built?
What can I do next?
```

Possible elements include:

* Name
* Short introduction
* Role
* Profile image
* Primary call-to-action
* Secondary navigation
* AI interview entry point

Avoid making the hero visually impressive at the expense of clarity.

---

# 10. Projects

Projects are one of the most important parts of the portfolio.

The presentation should make it easy to understand:

```text id="2x8r6w"
What was built?
Why was it built?
What technologies were involved?
What did the person contribute?
What makes the project interesting?
```

Possible interfaces include:

* Cards
* Grid
* Timeline
* Expandable projects
* Interactive project views
* Case-study style sections

Contributors are free to propose alternatives.

---

# 11. Skills

Skills should be understandable rather than simply displayed as a large collection of logos.

Possible approaches include:

* Categories
* Skill groups
* Interactive exploration
* Project-linked skills
* Simple lists
* Visual representations

Avoid visualizations that imply unsupported skill levels unless the data actually exists.

---

# 12. Experience

Experience may be presented as:

* Timeline
* Cards
* Sections
* Chronological list
* Interactive history

The chosen design should make the information easy to scan.

---

# 13. Education

Education should be presented clearly and consistently with the rest of the portfolio.

The design should prioritize readability over decorative elements.

---

# 14. GitHub and External Work

Relevant external work may be surfaced through links or integrations.

The frontend should make it clear when the visitor is leaving the application.

Do not fabricate repository activity, project information, or achievements.

---

# 15. Interview My AI

The portfolio should provide a clear path into the AI interview experience.

For example:

```text id="i4h7w8"
Portfolio
    ↓
"Ask my AI"
    ↓
Interview interface
```

The exact presentation is open to contributors.

Possible approaches include:

* CTA
* Floating entry point
* Dedicated navigation item
* Hero action
* Project-specific question prompts

The important part is that the visitor understands what will happen when they enter the interview.

---

# 16. Interview Experience

The interview interface should feel like a natural extension of the portfolio.

The visitor should be able to:

```text id="r2x8sl"
Ask a question
      ↓
See that the AI is thinking / responding
      ↓
Read the answer
      ↓
Continue the conversation
```

Useful interface states include:

* Initial state
* Suggested questions
* User message
* AI response
* Loading state
* Error state
* Empty state
* Conversation history

---

# 17. AI Identity

The AI represents the candidate.

The interface should make this understandable.

Possible elements include:

* Candidate avatar
* AI avatar
* Candidate name
* "AI version of me"
* Interview-specific visual identity

The exact design is open to contributors.

Avoid creating visual elements that imply capabilities the system does not actually have.

---

# 18. Animations

Animations are welcome when they improve the experience.

Good uses include:

* Page transitions
* Section reveals
* Hover interactions
* Card expansion
* Loading feedback
* Interview message transitions
* Navigation feedback

Avoid animation for animation's sake.

Animations should not:

* Make content difficult to read
* Slow down the interface
* Prevent interaction
* Create accessibility problems
* Distract from important information

---

# 19. Responsive Design

The portfolio should work across different screen sizes.

At minimum, contributors should consider:

```text id="o5b9c1"
Desktop
Tablet
Mobile
```

Do not treat mobile as an afterthought.

The layout, navigation, typography, interactions, and interview experience should adapt appropriately.

---

# 20. Accessibility

Accessibility is part of the frontend architecture.

Consider:

* Keyboard navigation
* Semantic structure
* Focus states
* Readable contrast
* Screen-reader compatibility
* Reduced-motion preferences
* Touch targets
* Form labels
* Error messaging

An interaction that only works with a mouse should generally not be considered complete.

---

# 21. Performance

Frontend features should consider their cost.

Before adding a heavy animation, library, image, or dependency, ask:

```text id="c1n8y5"
What does this add?
        ↓
What does it cost?
        ↓
Is the tradeoff worth it?
```

Prefer:

* Optimized assets
* Reasonable bundle size
* Lazy loading where appropriate
* Minimal unnecessary JavaScript
* Efficient rendering
* Sensible animation

Performance should be evaluated rather than assumed.

---

# 22. Frontend Dependencies

Do not add a frontend framework or library merely because it is popular.

Before introducing a dependency, consider:

```text id="n2o8cl"
Can the existing project solve this?

If yes:
→ Prefer the existing solution.

If no:
→ Explain why the dependency is justified.
```

A new dependency should provide meaningful value.

---

# 23. Frontend Logic Boundaries

The frontend should be responsible for presentation and user interaction.

It should not duplicate backend responsibilities.

Prefer:

```text id="6x2wz9"
Frontend
   ↓
Application / Agent
   ↓
Tools
   ↓
Knowledge
```

rather than:

```text id="u5j1q3"
Frontend
   ↓
Direct database logic
   ↓
Custom retrieval
   ↓
Agent
```

Do not bypass established application boundaries simply to make a frontend feature easier to implement.

---

# 24. Do Not Couple the UI to One Person's Content

A contributor may develop using their own:

```text id="8n5v4j"
Name
Projects
Photo
Skills
Experience
```

But the resulting frontend should ideally be adaptable to different candidates.

The design should not assume:

```text id="v7c4d2"
"This specific person's data will always exist."
```

Instead, think:

```text id="z8m3q1"
Candidate data
      ↓
Reusable presentation
```

This is especially important if the project becomes a reusable portfolio system.

---

# 25. Empty and Missing Data

Not every candidate will have every type of information.

The frontend should handle missing sections gracefully.

For example:

```text id="p6k8x2"
No GitHub data
      ↓
Do not show a broken GitHub section.

No experience data
      ↓
Do not display an empty timeline.

No project image
      ↓
Use an appropriate fallback.
```

Do not invent content merely to fill visual space.

---

# 26. Contributor Experiments

Contributors may create prototypes before proposing a final implementation.

For example:

```text id="v3q9l1"
Idea
 ↓
Prototype
 ↓
Screenshot / Demo
 ↓
Proposal
 ↓
Decision
 ↓
Production implementation
```

A prototype does not automatically become production code.

It is a way to explore an idea.

---

# 27. Competing Designs

If multiple contributors propose different designs for the same area, that is acceptable.

For example:

```text id="e7m2p4"
Project Cards

Design A
→ Minimal cards

Design B
→ Interactive cards

Design C
→ Full-screen project exploration
```

The project can compare them based on:

* Clarity
* User experience
* Accessibility
* Performance
* Complexity
* Maintainability
* Overall product fit

The strongest solution should win — not necessarily the earliest submission.

---

# 28. Frontend Contributions Should Be Reusable

When possible, separate:

```text id="y8s3p1"
Content
```

from:

```text id="w4m7c9"
Structure
Styling
Interaction
Behavior
```

A contributor should aim to contribute a frontend system that another candidate can adapt rather than a one-off page that only works for the contributor's personal data.

---

# 29. What Not to Do

Avoid:

### Rewriting everything

Do not replace the existing frontend simply because you prefer another approach.

### Unnecessary framework changes

Do not introduce React, Next.js, Vue, or another framework without a justified architectural proposal.

### Hard-coded personal content

Do not build a reusable feature around one contributor's information when the content can reasonably be separated.

### Decorative complexity

Do not add animations or 3D effects without a clear purpose.

### Backend duplication

Do not implement retrieval or agent logic inside the frontend.

### Accessibility afterthoughts

Do not treat accessibility as something to fix only after the feature is finished.

---

# 30. What a Good Frontend Contribution Looks Like

A strong contribution usually looks like:

```text id="k1q8v5"
Clear problem
      ↓
Good idea
      ↓
Simple implementation
      ↓
Reusable structure
      ↓
Responsive behavior
      ↓
Accessible interaction
      ↓
Tested experience
```

It does not need to be visually spectacular.

It needs to make the product better.

---

# 31. Frontend Design Principle

The frontend should feel:

```text id="s9c2x7"
Clear
Human
Interactive
Fast
Accessible
Responsive
Personal
```

But these qualities should emerge from good design decisions rather than from adding unnecessary effects.

---

# 32. The North Star

A visitor should leave the portfolio understanding:

```text id="j4p7m2"
Who is this person?
        ↓
What have they built?
        ↓
What do they know?
        ↓
How do they think?
        ↓
What can I ask them?
```

The portfolio communicates the first four.

The AI interview helps with the deeper questions.

---

# 33. Repository

Always check the latest project implementation and contribution guidelines:

https://github.com/Aum121221/interview_my_ai

Before starting frontend work, read:

```text id="a3m6v9"
README.md
CONTRIBUTING.md
docs/PROJECT_VISION.md
docs/ARCHITECTURE.md
docs/DECISION_PROCESS.md
frontend/FRONTEND_VISION.md
```

The current repository takes precedence over examples in this document.

---

# 34. Final Principle

> **Build a frontend that makes the person understandable, the work discoverable, and the AI interview worth having.**

Bring your own design ideas.

Make them useful.

Keep them simple.

Make them reusable.

And leave the frontend better for the next contributor.
