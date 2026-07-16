6.1 Layered Architecture
Principle

Every backend feature shall follow the same architectural flow.

Client
↓

API Router

↓

Service Layer

↓

Repository / ORM

↓

Database
Rationale

Each layer has one responsibility.

Business logic must never be duplicated across layers.

6.2 Thin API Controllers
Principle

API routes coordinate requests.

They do not contain business logic.

Responsibilities

API routes may:

Authenticate
Validate request
Call service
Return response

API routes must not:

Implement business rules
Write SQL
Decide tenant ownership
Duplicate validation
6.3 Service Layer Owns Business Logic

Every business rule belongs inside the service layer.

Examples:

Create customer
Create quotation
Create requirement
Generate next sequence
Validate duplicates

Everything goes through services.

6.4 BusinessContext Is Mandatory

Every business operation receives:

BusinessContext

Not:

business_id

BusinessContext is the trusted source of:

Current business
Current user
Membership
Role
6.5 Database Is Never Trusted Directly

Clients never modify the database directly.

Everything flows through:

API

↓

Service

↓

Validation

↓

Database
6.6 Models Represent Data

SQLAlchemy models describe persistence.

They do not contain business workflows.

Business behavior belongs in services.

6.7 Schemas Represent Contracts

Pydantic schemas define communication.

They are not business logic.

They are not database models.

They define:

Input
Output
Validation
6.8 Migrations Preserve History

Alembic migrations are permanent records.

Never edit old migrations after deployment.

New changes require new migrations.

History should remain reproducible.

6.9 Dependency Injection

Shared dependencies should be injected.

Examples:

Database Session

BusinessContext

Current User

Avoid hidden global state.

6.10 Reuse Before Creating

Before writing new code, ask:

Does an existing helper already solve this?

Example:

Instead of:

Query ServiceType again...

Use:

get_service_type_for_business()
6.11 Services Are Clients Too

The AI layer.

Excel Import.

Future Mobile App.

Automation Engine.

All use the same service layer.

Nobody bypasses validation.

6.12 Predictability Beats Cleverness

Readable architecture is preferred over clever architecture.

Future maintainability is more valuable than short-term optimization.

Anti-Patterns

❌ Business logic inside API routes.

❌ SQL inside controllers.

❌ Duplicate validation.

❌ Trusting client-provided tenant IDs.

❌ Editing old migrations.

❌ Skipping the service layer.

❌ Direct database writes from AI.

6.13 Architecture Is More Valuable Than Code

Code can always be rewritten.

Architecture becomes increasingly expensive to change as the product grows.

Therefore:

Optimize architecture before implementation.
Review architecture before reviewing code.
Never sacrifice architecture for faster coding.

🚫 Constitutional Violations
Business logic inside API routes.
SQL queries inside controllers.
Trusting business_id from the client.
Duplicating business logic across layers.
Editing old Alembic migrations.

🔒 Constitutional Principle

Every business operation in BizPart AI must pass through a consistent architectural pipeline where responsibilities are clearly separated, business rules are centralized, and tenant safety is enforced by design rather than by convention.