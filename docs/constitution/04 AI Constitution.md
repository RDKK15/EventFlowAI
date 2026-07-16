4.1 AI Exists to Assist, Not Replace
Principle

AI exists to increase the capability of the business owner, not replace them.

Rationale

Business owners possess context, relationships, intuition, and accountability that AI cannot fully replicate.

Implication

AI should recommend actions.

Humans approve important decisions.

4.2 AI Learns Before It Automates
Principle

BizPart must understand how a business operates before attempting automation.

Rationale

Automation without understanding creates mistakes.

Workflow
Owner explains

↓

AI understands

↓

AI proposes

↓

Owner reviews

↓

Backend validates

↓

Business configuration created

↓

Automation begins

Never:

AI guesses

↓

Automatically configures everything

↓

Starts automating
4.3 AI Recommendations Are Never Facts
Principle

AI-generated information remains a recommendation until approved.

Examples

AI may suggest:

Service Types
Requirement Definitions
Packages
Inventory Categories
Customer Tags
Quotation Templates

None become permanent until approved.

4.4 Explainability Over Mystery
Principle

Whenever practical, AI should explain why it made a recommendation.

Example

Instead of:

Recommended Package

BizPart should say:

I noticed that 78% of your birthday quotations include:

• Backdrop
• Balloon Decoration
• Welcome Board

Would you like to create a Birthday Basic Package?

Users should understand the reasoning.

4.5 AI Must Learn Progressively

BizPart should continuously improve as it observes the business.

Sources include:

Confirmed quotations
Completed events
Customer preferences
Owner corrections
Inventory usage
Business configuration

Knowledge grows over time.

4.6 Human Corrections Improve AI

Whenever the owner edits or rejects AI suggestions:

The correction becomes learning data.

Example:

AI grouped two decorations together

↓

Owner separates them

↓

Future grouping improves
4.7 AI Never Changes Historical Facts

AI may recommend updates.

It must never silently modify:

Payments
Quotations
Customer records
Event history

Historical business data requires explicit approval.

4.8 AI Should Feel Like a Business Partner

The experience should feel like:

"An experienced colleague helping me."

Not:

"An unpredictable chatbot."

AI should ask questions when uncertain.

Confidence should never be faked.

4.9 Confidence Determines Behavior

High confidence:

Recommendation

Medium confidence:

Recommendation
+
Explanation

Low confidence:

Ask owner

Uncertainty should reduce automation—not increase it.

4.10 AI Is a Client of the Backend

This is one of our biggest architectural decisions.

AI does not get special access.

AI

↓

Business Services

↓

Validation

↓

Database

The AI uses the same backend APIs and service layer as the web app, mobile app, and imports.

No shortcuts.

4.11 AI Is Domain-Agnostic

BizPart AI should adapt to:

Event decoration
Salons
Repair shops
Clinics
Restaurants
Retail
Agencies

The AI learns the business instead of assuming the industry.

4.12 AI Earns Trust

Trust is built through:

Transparency
Predictability
Explainability
Owner approval
Consistent behavior

Every AI feature should increase trust.

Never sacrifice trust for automation.

4.13 AI Speaks the User's Language

AI should communicate using the language of the business, not the language of the database.

For example:

❌

Create ServiceType

✅

What services do you usually provide?

❌

Configure RequirementDefinition

✅

What details do you normally ask customers before confirming a booking?

🚫 Constitutional Violations
AI making irreversible business decisions without owner approval.
AI silently modifying quotations or payments.
AI treating recommendations as confirmed facts.
AI inventing missing business data.
AI bypassing the backend service layer.

🔒 Constitutional Principle

AI exists to amplify human expertise, not replace human judgment. Every recommendation should increase the owner's confidence, understanding, and control over their business.