# Goal: Display product catalog + content catalog cleanly

- [ ] Create `/library` list view with sections:
  - [ ] “Your unlocked items”
  - [ ] “Locked previews”
- [ ] Add content detail route (e.g., `/library/items/[slug]`).
- [ ] Ensure the detail route checks entitlement server-side before loading full body.
- [ ] Local test: toggle entitlement in DB and verify page behavior changes.