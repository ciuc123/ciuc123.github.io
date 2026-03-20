# Decisions

## Decision: paid value is curated materials (video optional)
- We gate original pages/resources.
- We may embed/link to external courses.
- We avoid building secure video delivery until it’s necessary.

## Decision: entitlements-first access model
- Entitlements table is the canonical access check.
- Purchases table is for audit/debug.

## Decision: webhooks grant access
- Stripe webhook is the only writer of purchases/entitlements.
- Success pages are for UX only.

## Decision: prevent content leakage
- No “download full content to client then hide it”.
- Avoid SSG for paid pages unless content is fetched after server-side entitlement check.

## Decision: phase 2 secure assets
- Use S3 + CloudFront signed URLs/cookies only when needed.