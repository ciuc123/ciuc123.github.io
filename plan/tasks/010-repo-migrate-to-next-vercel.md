# Task 010 — Migrate repo to Next.js + Vercel-ready structure

## Goal
Introduce/confirm Next.js app structure suitable for Vercel deployment, while preserving existing content as needed.

## Scope
- Add Next.js scaffolding (App Router preferred)
- Add basic layout + a home page
- Add a protected “/library” placeholder route (actual auth later)

## Acceptance Criteria
- `npm run dev` works locally
- `npm run build` succeeds
- Deployed preview on Vercel works (once wired)

## Notes
If the repo currently contains a static site/blog, decide whether to:
- migrate gradually (keep old content under `/legacy`), or
- replace with Next.js fully.