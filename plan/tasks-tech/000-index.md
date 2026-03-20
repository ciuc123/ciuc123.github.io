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
2. 015-upgrade-app-next-to-nextjs-16
3. 020-auth-clerk
4. 030-db-supabase-schema-rls
5. 040-stripe-checkout
6. 050-stripe-webhooks-entitlements
7. 060-gated-content-library
8. 070-emails-resend (optional)
9. 080-analytics-ga4-utms (optional)
10. 090-secure-assets-cloudfront-s3 (phase 2, optional)
