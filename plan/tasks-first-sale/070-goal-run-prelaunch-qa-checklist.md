# Goal: Prelaunch QA so first buyers don’t hit bugs

- [ ] Test logged-out purchase flow (sign-in required before purchase? decide and test).
- [ ] Test logged-in purchase flow.
- [ ] Test webhook reliability (Stripe CLI replay event; ensure idempotent).
- [ ] Test “already owns product” behavior (hide buy button or show “Owned”).
- [ ] Test mobile layout for landing + checkout CTA.
- [ ] Local test: run through the full flow twice; second run should not duplicate purchases/entitlements.