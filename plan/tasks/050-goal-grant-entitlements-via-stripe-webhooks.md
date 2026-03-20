# Goal: Grant entitlements via Stripe webhook (source of truth)

- [ ] Create webhook endpoint that verifies Stripe signature.
- [ ] On `checkout.session.completed`, upsert purchase record (idempotent).
- [ ] Grant entitlement for the product associated with the price/session.
- [ ] Ensure webhook retries don’t create duplicates (unique constraints + upsert).
- [ ] Local test: use Stripe CLI to forward webhooks; complete a test checkout and verify entitlement is created in Supabase.