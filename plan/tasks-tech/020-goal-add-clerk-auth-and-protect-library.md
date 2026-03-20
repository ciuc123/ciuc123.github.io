# Goal: Add Clerk auth and protect /library

- [ ] Add Clerk SDK to `app-next` and document required environment variables.
- [ ] Wrap the App Router layout with Clerk provider setup.
- [ ] Create sign-in and sign-up routes/pages under `app-next/app/`.
- [ ] Add middleware or server-side auth protection so `/library` redirects to sign-in when logged out.
- [ ] Show the current Clerk user id on `/library` (server-derived) for debugging.
- [ ] Update `README.md` with local auth setup notes.
- [ ] Local test: run dev server, visit `/library` logged out (redirect), then log in and access `/library`.

Notes:
- Current app foundation lives in `app-next/` on Next.js 14.2.35.
- A separate follow-up task (`015-goal-upgrade-app-next-to-nextjs-16.md`) tracks the major framework upgrade required to fully clear current audit findings.
