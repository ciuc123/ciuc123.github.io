# Andrei Ciuculescu - Professional Portfolio

A clean, professional Jekyll portfolio website showcasing Laravel backend development and DevOps expertise.

## Features

- Responsive design optimized for all devices
- Professional minimalist theme
- Integrated contact form
- SEO optimized
- Fast loading and accessible

## Deployment

This site is configured for GitHub Pages deployment at ciuculescu.com.

## Local Development

```bash
bundle install
bundle exec jekyll serve --livereload
```

Visit http://localhost:4000 to view the site locally.

## Contact

For inquiries, please use the contact form on the website or connect via LinkedIn.


## Tags
welcome-email - Include in the welcome email pdf generation

## Generate email from blog posts
All blog posts with the tag welcome-email will be included in the welcome email pdf.
To generate the email, run: ./generate-welcome-pdf.sh

## Next.js Foundation (Migration Track)

A minimal Next.js App Router app lives in `app-next/` so it can coexist with the current Jekyll site during migration.

Use Node.js `20.9.0` or newer for `app-next/`.

If `nvm` is not installed in WSL, install Node.js 20+ using your preferred manager (for example NodeSource packages, `fnm`, or `volta`) before running the commands below.

### `app-next/bootstrap.sh`

`app-next/bootstrap.sh` is the preferred way to work with the Next.js app locally.
It helps avoid accidentally using the system Node 18 runtime.

What it does:
- loads `nvm` from `~/.nvm/nvm.sh`
- switches to the Node version in `app-next/.nvmrc`
- runs commands from inside `app-next/`
- in `dev` mode, clears stale `.next` output and restarts the dev server cleanly

Supported modes:
- `./bootstrap.sh dev` — install dependencies, clear stale dev state, and start the dev server
- `./bootstrap.sh build` — install dependencies and run a production build
- `./bootstrap.sh start` — start the production server
- `./bootstrap.sh install` — install dependencies only

### Run Next.js locally

Preferred helper:

```bash
cd app-next
./bootstrap.sh dev
```

Manual equivalent:

```bash
export NVM_DIR="$HOME/.nvm"
. "$NVM_DIR/nvm.sh"
cd app-next
nvm use 20.9.0
npm install
npm run dev
```

Visit http://localhost:3000 to view the Next.js app locally.

### Build Next.js

Preferred helper:

```bash
cd app-next
./bootstrap.sh build
```

Manual equivalent:

```bash
export NVM_DIR="$HOME/.nvm"
. "$NVM_DIR/nvm.sh"
cd app-next
nvm use 20.9.0
npm run build
npm run start
```

### Install dependencies only

```bash
cd app-next
./bootstrap.sh install
```

### Start the production server

```bash
cd app-next
./bootstrap.sh start
```

### `bootstrap.sh` troubleshooting

If `./bootstrap.sh` says `nvm was not found`, make sure `nvm` is installed in `~/.nvm`.

If `./bootstrap.sh` says `Node.js 20.9.0 is not installed in nvm`, run:

```bash
export NVM_DIR="$HOME/.nvm"
. "$NVM_DIR/nvm.sh"
nvm install 20.9.0
```

If your shell still reports Node 18, avoid running `npm` directly and use the helper instead:

```bash
cd app-next
./bootstrap.sh dev
```

### Clerk auth setup

Before running authenticated routes in `app-next/`, configure these environment variables in your shell or a local env file.
A ready-to-copy example lives at `app-next/.env.example`.

- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
- `CLERK_SECRET_KEY`

Optional Clerk URL overrides if you want explicit route configuration:
- `NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in`
- `NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up`
- `NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/library`
- `NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/library`

Without valid Clerk keys, the app now falls back to non-crashing setup messages on `/sign-in`, `/sign-up`, and `/library` so local builds and prerendering still succeed.
With valid Clerk keys, the full auth flow is enabled automatically.

### Supabase schema setup

The initial SQL-first schema for products, purchases, entitlements, and gated content lives in:
- `app-next/supabase/migrations/0001_entitlements_schema.sql`
- `app-next/supabase/README.md`

Additional environment variables are documented in `app-next/.env.example`:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`

Recommended next step for task `030`:
1. Copy `app-next/.env.example` to `app-next/.env.local`
2. Fill in your Supabase values
3. Open the Supabase SQL editor
4. Run `app-next/supabase/migrations/0001_entitlements_schema.sql`
5. Seed one `products` row using the commented example in the migration

