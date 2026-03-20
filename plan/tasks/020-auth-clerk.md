# Task 020 — Clerk authentication + protected routes

## Goal
Users can sign up/sign in and access protected pages.

## Scope
- Integrate Clerk SDK
- Protect `/library`
- Server-side session verification

## Acceptance Criteria
- Unauthenticated users are redirected to sign-in from `/library`
- Authenticated users see `/library` page
- Clerk user id is available on the server