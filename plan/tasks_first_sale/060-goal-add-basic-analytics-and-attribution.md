# Goal: Measure the funnel for the first sale

- [ ] Add UTMs capture (store in cookie/local storage) on landing page visit.
- [ ] Fire `start_checkout` when CTA is clicked.
- [ ] Fire `purchase` only after webhook-confirmed entitlement (not on success page view).
- [ ] Local test: verify events fire in dev (console log ok) and UTMs persist into checkout creation.