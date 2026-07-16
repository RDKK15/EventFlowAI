Principle 1 — Every Business Is an Independent Tenant

Each business is its own isolated workspace. Data, configuration, users, and operations belong to exactly one business unless explicitly designed otherwise.

Principle 2 — Tenant Isolation Is Mandatory

No feature may expose, modify, or infer another tenant's data. Tenant isolation is a security requirement, not an optional optimization.

Principle 3 — BusinessContext Is the Source of Truth

All business operations derive tenant identity from BusinessContext.

Never trust:

business_id from request bodies
business_id from query parameters
business_id from client-side state
Principle 4 — Membership Grants Access

Access is determined by membership (BusinessUser), not ownership of a user record.

This is what allows:

Multiple owners
Managers
Staff
Future invitations
Future consultants/accountants

without changing the architecture.

Principle 5 — Security by Default

If tenant ownership cannot be proven, access is denied.

Default behavior should always be deny, never allow.

Principle 6 — Information Leakage Is a Security Bug

If a resource belongs to another tenant:

Return:

404 Not Found

rather than revealing that another business exists.

Principle 7 — Shared Infrastructure, Isolated Data

BizPart is one SaaS platform.

Businesses share:

Backend
Database server
AI infrastructure
APIs

But never share business data.

Principle 8 — Future Scalability

The architecture must support:

One user belonging to multiple businesses.
Businesses with hundreds of employees.
Multiple roles.
Enterprise plans.

without redesigning tenant isolation.

Principle 9 — Tenant Isolation Is Tested, Not Assumed

It's not enough to believe the architecture is secure.

Every security boundary must have automated tests proving:

Correct tenant → allowed
Wrong tenant → denied

🚫 Constitutional Violations
Trusting business_id supplied by the client.
Executing queries that are not tenant-scoped.
Allowing one tenant to access or infer another tenant's data.
Returning errors that reveal the existence of another business (use 404 Not Found instead of exposing unauthorized resources).
Bypassing BusinessContext for business operations.
Assuming tenant isolation without automated tests.
Sharing business configuration or operational data across tenants without an explicit architectural decision.

🔒 Constitutional Principle

Tenant isolation is a fundamental architectural guarantee of BizPart AI. Every business shall operate within a completely isolated and secure environment where identity is established through trusted backend context, data ownership is absolute, and cross-tenant access is impossible by design rather than by convention.