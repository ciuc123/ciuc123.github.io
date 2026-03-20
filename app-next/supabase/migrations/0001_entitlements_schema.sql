-- Initial Supabase schema for products, purchases, entitlements, and gated content.
-- Apply in the Supabase SQL editor or via a future migration workflow.

create extension if not exists pgcrypto;

create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  clerk_user_id text not null unique,
  email text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.products (
  id uuid primary key default gen_random_uuid(),
  key text not null unique,
  name text not null,
  stripe_price_id text unique,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.purchases (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  stripe_checkout_session_id text not null unique,
  status text not null,
  amount integer,
  currency text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.entitlements (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  product_id uuid not null references public.products(id) on delete cascade,
  source_purchase_id uuid references public.purchases(id) on delete set null,
  granted_at timestamptz not null default now(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (user_id, product_id)
);

create table if not exists public.content_items (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  title text not null,
  excerpt text,
  body_ref text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.product_content (
  product_id uuid not null references public.products(id) on delete cascade,
  content_item_id uuid not null references public.content_items(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (product_id, content_item_id)
);

create index if not exists purchases_user_id_idx on public.purchases (user_id);
create index if not exists entitlements_user_id_idx on public.entitlements (user_id);
create index if not exists entitlements_product_id_idx on public.entitlements (product_id);
create index if not exists product_content_product_id_idx on public.product_content (product_id);
create index if not exists product_content_content_item_id_idx on public.product_content (content_item_id);

alter table public.users enable row level security;
alter table public.products enable row level security;
alter table public.purchases enable row level security;
alter table public.entitlements enable row level security;
alter table public.content_items enable row level security;
alter table public.product_content enable row level security;

-- Read-only product/catalog access can be public for now.
drop policy if exists "products are readable by everyone" on public.products;
create policy "products are readable by everyone"
  on public.products
  for select
  using (true);

drop policy if exists "content items are readable by everyone" on public.content_items;
create policy "content items are readable by everyone"
  on public.content_items
  for select
  using (true);

-- Entitlement and purchase reads should be server-side or user-owned only.
-- These policies assume the request context carries a Clerk user id in the JWT claim `request.jwt.claims.clerk_user_id`.
drop policy if exists "users can read their own user row" on public.users;
create policy "users can read their own user row"
  on public.users
  for select
  using (clerk_user_id = current_setting('request.jwt.claims.clerk_user_id', true));

drop policy if exists "users can read their own purchases" on public.purchases;
create policy "users can read their own purchases"
  on public.purchases
  for select
  using (
    exists (
      select 1
      from public.users
      where public.users.id = public.purchases.user_id
        and public.users.clerk_user_id = current_setting('request.jwt.claims.clerk_user_id', true)
    )
  );

drop policy if exists "users can read their own entitlements" on public.entitlements;
create policy "users can read their own entitlements"
  on public.entitlements
  for select
  using (
    exists (
      select 1
      from public.users
      where public.users.id = public.entitlements.user_id
        and public.users.clerk_user_id = current_setting('request.jwt.claims.clerk_user_id', true)
    )
  );

-- Writes remain service-role only for now; no insert/update/delete policies are granted.

-- Manual seed example (adjust values before running in production):
-- insert into public.products (key, name, stripe_price_id)
-- values ('library-access', 'Library Access', 'price_replace_me')
-- on conflict (key) do update set
--   name = excluded.name,
--   stripe_price_id = excluded.stripe_price_id,
--   updated_at = now();

