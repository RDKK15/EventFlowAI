# Database State Inspection — run this BEFORE any `alembic upgrade`

Do not run `alembic upgrade head` or `alembic stamp` anything until you've
run these and matched your results to one of the cases below. Nothing here
modifies your database.

## 1. Exact commands to run

From `backend/`, with your real `DATABASE_URL` active:

```powershell
# 1. Current Alembic revision (as far as Alembic's bookkeeping knows)
alembic current

# 2. Full migration history Alembic knows about
alembic history --verbose
```

Then connect directly to Postgres (psql, or any SQL client) and run:

```sql
-- 3. Does alembic_version exist, and if so what does it say?
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'alembic_version'
) AS alembic_version_table_exists;

SELECT * FROM alembic_version;  -- only if the above is true

-- 4. Which tables currently exist
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- 5. Does users exist specifically
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'users'
) AS users_exists;

-- 6. If users exists, which columns does it have right now
SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'users'
ORDER BY column_name;
-- Look specifically for: business_id, name, created_at, updated_at

-- 7. Does businesses exist
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'businesses'
) AS businesses_exists;

-- 8. Does business_sequences exist
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'business_sequences'
) AS business_sequences_exists;
```

(psql shortcuts, if you prefer: `\dt` for #4, `\d users` for #6.)

Bring the results of all of these back before doing anything else.

## 2. Case-based plans

Only follow the plan for the case that **actually matches** what you found
above. Don't stamp anything speculatively.

### Case A — Legacy tables exist (`users`, `customers`, etc.), Phase 1
tables/columns do not

i.e. `users_exists = true`, `users` has none of `business_id` / `name` /
`created_at` / `updated_at`, and `businesses_exists = false`.

- **A1: `alembic_version` doesn't exist at all** (this database has never
  been touched by Alembic). Since `7b37bd901e3f` is a genuine no-op
  (empty `upgrade()`/`downgrade()`), declaring "we are at `7b37bd901e3f`"
  is accurate for any database whatsoever — it doesn't assert any schema
  shape. Safe action:
  ```powershell
  alembic stamp 7b37bd901e3f
  alembic upgrade head
  ```
  `alembic upgrade head` will then run only `e014e8ffab24`, which is
  additive (`CREATE TABLE` x2, nullable `ADD COLUMN` x4, one `ADD
  CONSTRAINT`) against your existing `users` table.

- **A2: `alembic_version` exists and already says `7b37bd901e3f`.**
  Nothing to stamp. Just run `alembic upgrade head`.

- **A3: `alembic_version` exists and says something else** (a revision id
  not in this project's history, e.g. from a different branch or a
  reset environment). **Stop.** Don't stamp or upgrade. Share the value
  with me — it means this database's migration history doesn't match
  this codebase's history, and needs to be reconciled deliberately, not
  guessed at.

### Case B — Empty PostgreSQL database (no tables at all)

`users_exists = false` and none of the other tables exist either.

There's a real gap here that predates Phase 1: `7b37bd901e3f` never
created the legacy tables (`customers`, `enquiries`, `quotations`,
`bookings`, `payments`, `users`), so an empty database has no path
through the existing migration chain to get the legacy schema.

The correct fix is a new migration inserted **between** `7b37bd901e3f`
and `e014e8ffab24` (not after — putting it after Phase 1 is the mistake
that was caught here, since it would leave `e014e8ffab24`'s `ALTER TABLE
users` still trying to run before `users` exists). Concretely, that means
a new revision with `down_revision = '7b37bd901e3f'`, and `e014e8ffab24`'s
`down_revision` repointed from `'7b37bd901e3f'` to the new revision's id.

**I have not generated this migration**, because it's only correct if
you're actually in Case B — the same statements would be wrong (duplicate
`CREATE TABLE`) if run against Case A or C. If your results above confirm
you're in Case B, tell me and I'll write that spliced-in "base schema"
migration against the actual current model definitions, rather than
guessing at it now.

### Case C — Phase 1 schema was partially applied

Some but not all of `businesses` / `business_sequences` /
`users.business_id` / `users.name` / `users.created_at` /
`users.updated_at` exist — e.g. a previous attempt was interrupted.

**Do not stamp or upgrade anything in this case without sharing the exact
inspection results first.** This is the one case where guessing can
genuinely corrupt state (e.g. re-running `CREATE TABLE businesses` when it
already exists, or double-adding a column). Once you share exactly which
pieces exist and which don't, I'll write a small targeted migration for
only the missing pieces — not a re-run of `e014e8ffab24`.

### Case D — Schema exists but Alembic history is missing or doesn't match

`alembic_version` is missing, or present but pointing to a revision id
that isn't part of this project's chain, while real tables/columns exist
in some shape.

**Do not auto-stamp.** Instead, compare what the table/column listing
(items 4–8) actually shows against what each known revision would
produce:

- Matches the pre-Phase-1 legacy shape (case A's shape) exactly →
  treat as **A1**: `alembic stamp 7b37bd901e3f`, then `alembic upgrade head`.
- Matches the full Phase 1 end-state exactly (`businesses` and
  `business_sequences` both exist, `users` has all four new columns) →
  `alembic stamp e014e8ffab24` is safe, since the schema genuinely already
  matches head — nothing further to upgrade.
- Matches neither cleanly → **stop**, don't stamp anything, share the
  results and I'll help reconcile it by hand rather than guessing.

## 3. General rule

`alembic stamp <revision>` only records "Alembic should believe the
database is at this revision" — it does not change the schema at all. It
is safe **only** when the real schema genuinely matches what that
revision represents. Never stamp `head` as a way to "skip" a migration
you haven't verified against reality.
