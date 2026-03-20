# Roadmap

## Phase 0 — Branching + deployment workflow
- Work on dev branch.
- Decide whether to keep GitHub Pages or switch to Vercel (recommended for Next.js).

## Phase 1 — Next.js app foundation
- Basic pages + layout
- Public landing pages
- Private /library skeleton (auth later)

## Phase 2 — Auth
- Clerk integration
- Protected routes
- User mapping to Supabase

## Phase 3 — DB + entitlements
- Supabase schema + RLS
- Product catalog + content metadata (optional)

## Phase 4 — Payments
- Stripe checkout session creation
- Product/price mapping

## Phase 5 — Webhooks
- Webhook verification
- Idempotent writes
- Entitlements grant

## Phase 6 — Gated library
- Show full content only when entitled
- Upsell previews when not

## Phase 7 — Optional add-ons
- Resend email
- GA4/UTMs

## Phase 8 — Optional Phase 2 secure assets
- CloudFront/S3 signed URLs for private downloads/video

Last updated: 2026-03-20