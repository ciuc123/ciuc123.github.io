# Goal: Create Supabase schema for products, purchases, entitlements

- [x] Create tables: users, products, purchases, entitlements (minimal columns).
- [x] Add uniqueness constraints for idempotency (checkout_session_id; user_id+product_id).
- [x] Add a seed product row (manual) and note its product key + Stripe price id mapping strategy.
- [x] Add RLS policies for entitlements so a user can only read their own entitlements.
- [ ] Local test: using Supabase SQL editor, insert a test user + entitlement; verify select returns expected rows.

Notes:
- Initial SQL schema lives in `app-next/supabase/migrations/0001_entitlements_schema.sql`.
- Setup and Clerk mapping notes live in `app-next/supabase/README.md`.
- Supabase environment variables were added to `app-next/.env.local`.
- Remaining work is the manual Supabase-side application and verification of the migration in a real project.
