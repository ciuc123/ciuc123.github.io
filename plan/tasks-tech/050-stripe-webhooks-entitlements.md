# Task 050 — Stripe webhook → purchases + entitlements

## Goal
Grant access based on Stripe webhook confirmation.

## Scope
- Webhook route with signature verification
- Idempotent DB writes (unique checkout session id)
- Create purchase record
- Grant entitlements

## Acceptance Criteria
- Completing checkout triggers webhook
- Entitlement row appears in Supabase for the user/product
- Replaying webhook does not create duplicates