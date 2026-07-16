😂😂🔥 ALMOST THERE BRO.

📜 Chapter 9 — Naming & Coding Standards Constitution

This chapter ensures that five years from now, the codebase still looks like it was written by one team.

Without this chapter, every contributor (human or AI) will gradually introduce different naming styles, patterns, and conventions.

9.1 Consistency Over Preference
Principle

Consistency is more valuable than individual coding preference.

If an existing convention exists, follow it.

Do not introduce a new style without a justified architectural reason.

9.2 Business Language First
Principle

Names should represent business concepts rather than technical implementation.

Examples:

✅

Business

ServiceType

RequirementDefinition

Booking

Quotation

Payment

Avoid vague or overly generic names.

❌

DataManager

Thing

Helper

Utils2

ObjectHandler
9.3 Self-Describing Code

Code should explain itself.

Names should reduce the need for comments.

Example:

Good

create_requirement_definition()

Better than

create_req()
9.4 One Meaning Per Name

A concept should have exactly one name throughout the project.

Example:

If the project uses:

ServiceType

Never introduce:

Service

BusinessService

Category

to represent the same concept.

9.5 Predictable Project Structure

Every module should follow the same structure.

Example:

models/

schemas/

services/

api/

tests/

Future developers should know where to find code without searching.

9.6 Naming Conventions

Classes

PascalCase

Functions

snake_case

Variables

snake_case

Constants

UPPER_CASE

Files

snake_case.py
9.7 Public APIs Should Be Descriptive

API endpoints should represent business actions.

Example

Good

/service-types

Better than

/service-config
9.8 Comments Explain Why

Comments should explain:

WHY

not

WHAT

Bad

# increment i
i += 1

Good

# Reserve the next business-specific customer number.
9.9 Reuse Existing Vocabulary

Before introducing a new name, check whether the concept already exists.

Avoid creating synonyms.

Consistency improves maintainability.

9.10 AI Must Follow Existing Style

AI-generated code must follow the project's naming conventions.

AI should adapt to BizPart AI.

BizPart AI should not adapt to AI.

9.11 Code Should Read Like Documentation

Someone reading the service layer should almost understand the business process without opening external documentation.

Example:

service_type = get_service_type_for_business(...)

ensure_unique_requirement_key(...)

create_requirement_definition(...)

Even without comments, the workflow is obvious.

That is the standard we should aim for.

🚫 Constitutional Violations
Mixing multiple naming styles.
Introducing synonyms for existing concepts.
Abbreviating names unnecessarily.
Generic class or function names that hide intent.
Creating inconsistent folder structures.
AI-generated code that ignores established naming conventions.
Comments that repeat what the code already says instead of explaining why.

🔒 Constitutional Principle

Every name in BizPart AI should communicate intent clearly, consistently, and in the language of the business, making the codebase understandable to both current and future contributors.