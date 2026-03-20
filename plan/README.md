# Plan

This folder contains architecture notes and an execution plan for turning this repository into a paid, gated “curated materials” product.

Stack (target):
- Next.js + Vercel (frontend + hosting)
- Clerk (authentication)
- Supabase (database for entitlements/purchases/content metadata)
- Stripe (payments + webhooks for access granting)
- Optional: YouTube (bonus video, not a security boundary)
- Optional: Resend (transactional email)
- Optional: GA4 + UTMs (marketing attribution)
- Optional Phase 2: S3 + CloudFront signed URLs/cookies (secure assets)

How to use this folder
1) Read architecture.md + decisions.md.
2) Follow roadmap.md for phases.
3) Execute tasks in plan/tasks/ in order, one at a time.
4) A task is done only when every checkbox is completed and you can verify locally.

Principles
- Stripe webhook is the source of truth for entitlements (never the success page).
- Entitlements-first model: “who owns what” is the core.
- Avoid leaking paid content via static generation or client-side JSON.
- Paid value is curated materials; videos are optional.