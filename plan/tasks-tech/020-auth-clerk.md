# Task 020 — Clerk authentication + protected routes

## Goal
Users can sign up/sign in and access protected pages.

## Scope
- Integrate Clerk SDK into `app-next`
- Protect `/library`
- Server-side session verification
- Add sign-in and sign-up App Router pages

## Acceptance Criteria
- Unauthenticated users are redirected to sign-in from `/library`
- Authenticated users see `/library` page
- Clerk user id is available on the server
- Required environment variables are documented for local development
