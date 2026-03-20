# Task 030 — Supabase schema for entitlements/purchases/content

## Goal
Create database tables to support entitlements-first access checks.

## Suggested tables
- users (id, clerk_user_id unique, email)
- products (id, key unique, name, stripe_price_id or mapping)
- purchases (id, user_id, stripe_checkout_session_id unique, status, amount, currency, timestamps)
- entitlements (user_id, product_id, granted_at, source_purchase_id, unique(user_id, product_id))
- content_items (id, slug, title, excerpt, body_ref)
- product_content (product_id, content_item_id)

## Acceptance Criteria
- Schema exists in Supabase
- Uniqueness constraints in place for idempotency
- Basic RLS policies defined where appropriate