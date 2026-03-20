# Task 040 — Stripe Checkout (one-time purchase)

## Goal
User can purchase a product via Stripe Checkout.

## Scope
- Create checkout session server-side
- Redirect to Stripe-hosted checkout
- Return to success/cancel routes

## Acceptance Criteria
- Clicking “Buy” creates a checkout session
- Stripe checkout opens and completes in test mode
- Success page shows “processing access” message (no entitlement granted here)