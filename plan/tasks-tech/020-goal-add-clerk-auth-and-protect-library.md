# Goal: Add Clerk auth and protect /library

- [x] Add Clerk SDK to `app-next` and document required environment variables.
- [x] Wrap the App Router layout with Clerk provider setup.
- [x] Create sign-in and sign-up routes/pages under `app-next/app/`.
- [x] Add middleware or server-side auth protection so `/library` redirects to sign-in when logged out.
- [x] Show the current Clerk user id on `/library` (server-derived) for debugging.
- [x] Update `README.md` with local auth setup notes.
- [ ] Local test: run dev server, visit `/library` logged out (redirect), then log in and access `/library`.

Notes:
- Current app foundation lives in `app-next/` on Next.js 16.2.0.
- Auth route code is scaffolded and now degrades gracefully when Clerk env vars are missing, so local builds and prerendering do not crash.
- Clerk install issues were caused by a React patch mismatch (`react@~19.2.3` with `react-dom@19.2.0`). `package.json` has been corrected so both `react` and `react-dom` use `~19.2.3`.
- Local Clerk setup now uses `app-next/.env.example` copied to `app-next/.env.local`, and `app-next/.env.local` is gitignored.
- Verified with real keys in `.env.local`: `npm run build` succeeds and the Clerk-enabled routes are included in the production build.
- Next.js 16 deprecates `middleware.js`; the auth edge hook has been moved to `app-next/proxy.js`.
- Remaining local dev issue: the running dev server still references a removed `middleware.js` path from a stale edge cache, so the browser smoke test needs one fully fresh dev restart after stopping old dev processes.
