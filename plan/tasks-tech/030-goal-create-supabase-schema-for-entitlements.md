# Goal: Create Supabase schema for products, purchases, entitlements

- [ ] Create tables: users, products, purchases, entitlements (minimal columns).
- [ ] Add uniqueness constraints for idempotency (checkout_session_id; user_id+product_id).
- [ ] Add a seed product row (manual) and note its product key + Stripe price id mapping strategy.
- [ ] Add RLS policies for entitlements so a user can only read their own entitlements.
- [ ] Local test: using Supabase SQL editor, insert a test user + entitlement; verify select returns expected rows.