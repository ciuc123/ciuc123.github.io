# Architecture Goal: Sell gated curated materials (not video)

## What you are building
A Next.js site that has:
- Public landing pages (SEO)
- A private “Library” app area for paying users
- Payments (Stripe Checkout)
- Access control (entitlements stored in Supabase)

The paid value is curated materials (roadmaps, notes, checklists, templates, links, commentary). Video is optional.

## Components

### Next.js + Vercel
Purpose
- SEO + dynamic routes
- Authenticated app area
- Server-side API routes (Stripe webhooks, entitlement checks, signed URLs later)

Guidelines
- Keep paid content server-gated. Do not ship full content to the client for filtering.
- Public routes can show titles + previews only.

### Clerk (Auth)
Purpose
- User accounts + sessions

Integration guideline
- Treat Clerk as identity provider.
- Store a stable mapping in Supabase: users.clerk_user_id (unique).

### Supabase (DB)
Purpose
- purchases audit log
- entitlements (canonical “does user have access?”)
- content metadata (optional)

Security guideline
- Use RLS where appropriate, but still do server-side checks for gating.

### Stripe (Payments)
Purpose
- One-time purchases via Checkout
- Webhook-driven entitlement granting

Critical rule
- Do not grant access from the success page. Only grant from verified webhook events.

### Optional: YouTube
- OK for bonus videos/marketing.
- Unlisted links can leak; do not treat as secure.

### Optional: Resend
- Send purchase confirmation + access instructions after entitlement grant.

### Optional: GA4 + UTMs
- Track funnel: landing → checkout start → purchase (webhook-confirmed).

### Optional Phase 2: S3 + CloudFront signed URLs/cookies
When
- Only if you ship private downloadable assets or your own private video.

How (high level)
- Store assets in private S3.
- Serve via CloudFront.
- Next.js API route checks Clerk session + Supabase entitlements then returns short-lived signed URL/cookie.

## Core domain: entitlements
Everything should reduce to this question:
- Does this user own product X?

Stripe answers “did they pay?”. Supabase records “what do they own?”.

Suggested minimal tables
- users(id, clerk_user_id unique, email)
- products(id, key unique, name, stripe_price_id or mapping)
- purchases(id, user_id, stripe_checkout_session_id unique, status, amount, currency, created_at)
- entitlements(user_id, product_id, granted_at, source_purchase_id, unique(user_id, product_id))
- (optional) content_items + product_content for bundling.