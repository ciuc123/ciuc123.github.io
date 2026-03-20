# Goal: Add Clerk auth and protect /library

- [ ] Add Clerk SDK + required config files.
- [ ] Create sign-in and sign-up routes/pages.
- [ ] Protect `/library` so unauthenticated users are redirected to sign-in.
- [ ] Show the current Clerk user id on `/library` (server-derived) for debugging.
- [ ] Local test: run dev server, visit `/library` logged out (redirect), then log in and access `/library`.