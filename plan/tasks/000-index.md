# Task Index + Working Agreement

## How we work (one task at a time)
- Only one task is “In Progress” at any time.
- Each task ends with a demoable result and clear acceptance criteria.
- If a task is too large, split it before coding.

## Definition of Done (DoD)
- Code compiles/builds.
- Feature works in local dev.
- Environment variables documented.
- Security-sensitive flows are server-side (webhooks, entitlements).
- Minimal tests or manual test steps documented.

## Task execution order
1. 010-repo-migrate-to-next-vercel
2. 020-auth-clerk
3. 030-db-supabase-schema-rls
4. 040-stripe-checkout
5. 050-stripe-webhooks-entitlements
6. 060-gated-content-library
7. 070-emails-resend (optional)
8. 080-analytics-ga4-utms (optional)
9. 090-secure-assets-cloudfront-s3 (phase 2, optional)