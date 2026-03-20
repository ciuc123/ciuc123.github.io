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

### Run Next.js locally

```bash
cd app-next
npm install
npm run dev
```

Visit http://localhost:3000 to view the Next.js app locally.

### Build Next.js

```bash
cd app-next
npm run build
npm run start
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
