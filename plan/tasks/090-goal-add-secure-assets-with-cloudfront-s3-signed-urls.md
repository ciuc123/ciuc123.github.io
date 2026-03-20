# Goal: Add secure assets delivery via CloudFront/S3 signed URLs (Phase 2, optional)

- [ ] Create private S3 bucket for assets (no public ACLs).
- [ ] Create CloudFront distribution in front of the bucket.
- [ ] Add Next.js API route: verify Clerk session, check Supabase entitlement, then issue short-lived signed URL/cookie.
- [ ] Add a protected download link in the Library that calls the API and then fetches the signed URL.
- [ ] Local test: without entitlement, asset fetch fails; with entitlement, asset fetch succeeds.