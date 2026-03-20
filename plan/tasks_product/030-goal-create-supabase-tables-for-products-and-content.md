# Goal: Add DB tables to support product catalog + content mapping

- [ ] Add `products` table (id, key, name, active, stripe_price_id).
- [ ] Add `content_items` table (id, slug, title, excerpt, body_ref/body, status).
- [ ] Add `product_content` join table (product_id, content_item_id, sort_order).
- [ ] Add minimal RLS:
  - [ ] content_items public fields (title/excerpt) readable by all (optional)
  - [ ] full body gated via server (recommended) or via RLS tied to entitlements (advanced)
- [ ] Local test: insert sample rows in Supabase and confirm your app can read them.