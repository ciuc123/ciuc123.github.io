# Task 090 — Secure assets via CloudFront/S3 signed URLs (Phase 2)

## Goal
Securely deliver private files/videos only to entitled users.

## Scope
- Private S3 bucket + CloudFront distribution
- Next.js API route: verify Clerk session + Supabase entitlement
- Return signed URL or set signed cookie with short TTL

## Acceptance Criteria
- Non-entitled users cannot fetch assets
- Entitled users can fetch assets via short-lived signed URL
- No public object ACLs