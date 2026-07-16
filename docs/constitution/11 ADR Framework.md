11.1 Purpose
Principle

Not every architectural decision belongs in the Constitution.

The Constitution defines permanent principles.

Architectural Decision Records (ADRs) document why important decisions were made.

ADRs preserve engineering knowledge so future contributors understand both the decision and its reasoning.

11.2 What Is an ADR?

An ADR is a permanent record of a significant architectural decision.

It answers:

What was the problem?
What options were considered?
What decision was made?
Why was it chosen?
What are the consequences?

Every ADR becomes part of BizPart AI's engineering history.

11.3 When an ADR Is Required

An ADR must be created when making decisions that affect:

System architecture
Security
Multi-tenancy
Data ownership
AI behavior
Product philosophy
Development workflow
Long-term maintainability

Minor implementation details do not require an ADR.

11.4 Standard ADR Structure

Every ADR should follow this format:

ADR-XXX

Title

Status
(Proposed / Accepted / Superseded / Deprecated)

Date

Context

Decision

Alternatives Considered

Consequences

Related Constitution Chapters

Related BPA Decisions
11.5 ADR Lifecycle

Every ADR moves through the following stages:

Idea

↓

Discussion

↓

Proposal

↓

Review

↓

Accepted

↓

Implemented

↓

Referenced

↓

Archived (if superseded)

Historical ADRs should never be deleted.

11.6 Constitution vs ADR

The Constitution defines what BizPart AI believes.

ADRs explain why specific architectural choices were made.

Example:

Constitution

AI proposes.
Owner approves.

ADR:

Why did BizPart adopt progressive AI onboarding instead of a setup wizard?
11.7 ADRs Are Historical Records

Accepted ADRs should remain immutable.

If a later decision replaces an earlier one:

Do not edit the original ADR.

Instead:

Create a new ADR referencing the previous one.

Engineering history should remain traceable.

11.8 Referencing ADRs

Architecture discussions, pull requests, and code reviews should reference relevant ADRs.

Example:

This implementation follows:

ADR-003

and

BPA-005.

This creates a shared engineering vocabulary.

11.9 Superseding Decisions

When an architectural decision changes:

Old ADR

↓

Superseded

↓

New ADR

↓

Constitution Updated (if required)

History is preserved.

11.10 Learning From Decisions

The goal of an ADR is not only to document success.

It should also record:

Rejected alternatives
Trade-offs
Lessons learned

Future contributors benefit from understanding what was not chosen.

🚫 Constitutional Violations
Making significant architectural changes without an ADR.
Editing accepted ADRs instead of superseding them.
Recording implementation details that don't warrant an ADR.
Changing the Constitution without documenting the underlying decision.
Ignoring existing ADRs when making related architectural changes.
🔒 Constitutional Principle

Every significant architectural decision in BizPart AI shall be documented, justified, and preserved so that future contributors understand not only what was built, but why it was built that way.