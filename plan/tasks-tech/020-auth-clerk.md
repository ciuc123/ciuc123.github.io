# Task 020 — Clerk authentication + protected routes

## Goal
Users can sign up/sign in and access protected pages.

## Scope
- Integrate Clerk SDK into `app-next`
- Protect `/library`
- Server-side session verification
- Add sign-in and sign-up App Router pages
- Document local Clerk env setup via `.env.example` / `.env.local`

## Acceptance Criteria
- Unauthenticated users are redirected to sign-in from `/library`
- Authenticated users see `/library` page
- Clerk user id is available on the server
- Required environment variables are documented for local development
- `npm run build` succeeds with valid Clerk keys

## Status Notes
- Production build is verified with Clerk keys loaded from `app-next/.env.local`.
- Next.js 16 auth edge handling now lives in `app-next/proxy.js`.
- The shell may still default to system Node 18 (`/usr/bin/node`) unless `~/.nvm/nvm.sh` is sourced first.
- `app-next/bootstrap.sh` now provides a safer local entrypoint for `dev`, `build`, `start`, and `install` modes by loading `nvm`, switching to Node `20.9.0`, and cleaning stale dev state when needed.
- A stale local dev process was still referencing the removed `middleware.js`; use `./bootstrap.sh dev` for a fully fresh restart on Node 20.9.0.
