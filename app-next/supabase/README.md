# Supabase schema notes

This folder holds SQL-first database artifacts for the gated library flow.

## Current migration

- `migrations/0001_entitlements_schema.sql`

It creates:
- `public.users`
- `public.products`
- `public.purchases`
- `public.entitlements`
- `public.content_items`
- `public.product_content`

## Clerk identity mapping

Application auth uses Clerk.
Database ownership maps through `public.users.clerk_user_id`.

Expected flow:
1. Clerk authenticates the user.
2. A matching row exists in `public.users` with the same `clerk_user_id`.
3. Entitlements and purchases join through `public.users.id`.

## Apply the schema

For now, use the Supabase SQL editor and run `migrations/0001_entitlements_schema.sql`.

## Manual seed

Seed one product row for the first paid library offering.
Recommended product key:
- `library-access`

Store the Stripe mapping in `public.products.stripe_price_id`.

## RLS note

The initial policies assume a request claim named `request.jwt.claims.clerk_user_id`.
If your final Supabase + Clerk integration uses a different claim shape, update the policies before production rollout.

## Local verification idea

1. Insert a test row into `public.users` with a known Clerk user id.
2. Insert a test row into `public.products`.
3. Insert a linked row into `public.entitlements`.
4. Verify the entitlement row is readable only for the intended user context.

