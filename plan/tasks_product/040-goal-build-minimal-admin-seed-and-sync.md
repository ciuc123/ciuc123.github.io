# Goal: Make product/content management repeatable without a full admin UI

- [ ] Decide MVP admin method:
  - [ ] “Seed script” in repo that upserts products/content via Supabase admin key
  - [ ] Manual SQL inserts documented in a runbook
- [ ] Create `seed` approach (script or docs).
- [ ] Ensure the seed process is idempotent (safe to run multiple times).
- [ ] Local test: run seed twice and verify no duplicates.