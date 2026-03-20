# Goal: Prepare a Next.js + Vercel-ready foundation

- [x] Inspect current repo structure and note what is static site vs app code.
- [x] Add/confirm Node version + package manager choice (document in README or .nvmrc).
- [x] Add Next.js (App Router) skeleton that runs with `npm run dev`.
- [x] Add `npm run build` and ensure it succeeds locally.
- [x] Add a placeholder route `/library` that renders a simple page.
- [ ] Local test: run `npm install`, `npm run dev`, open `/` and `/library`.

Notes:
- Upgraded `app-next` from `next@14.2.5` to `next@14.2.35` (latest verified 14.x patch) and re-ran `npm install` + `npm run build` successfully.
- `npm audit` still reports a remaining Next.js advisory whose automatic fix path is `next@16.2.0` (major upgrade). That follow-up should be handled as a separate upgrade task after the foundation is in place.
