# Goal: Add Clerk auth and protect /library

- [ ] Add Clerk SDK to `app-next` and document required environment variables.
- [x] Wrap the App Router layout with Clerk provider setup.
- [x] Create sign-in and sign-up routes/pages under `app-next/app/`.
- [x] Add middleware or server-side auth protection so `/library` redirects to sign-in when logged out.
- [x] Show the current Clerk user id on `/library` (server-derived) for debugging.
- [x] Update `README.md` with local auth setup notes.
- [ ] Local test: run dev server, visit `/library` logged out (redirect), then log in and access `/library`.

Notes:
- Current app foundation lives in `app-next/` on Next.js 16.2.0.
- Auth route code is scaffolded.
- The Clerk install failure was caused by a React patch mismatch (`react@~19.2.3` with `react-dom@19.2.0`). `package.json` has been corrected so both `react` and `react-dom` use `~19.2.3`.
- Full runtime verification still requires a successful `npm install` plus valid Clerk environment variables (`NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, `CLERK_SECRET_KEY`).
