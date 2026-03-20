# Goal: Upgrade `app-next` to Next.js 16

- [ ] Review Next.js 16 upgrade notes for App Router compatibility and any config changes needed by the current `app-next` skeleton.
- [ ] Upgrade `next` in `app-next/package.json` to a stable `16.x` version and align related dependencies if required.
- [ ] Reinstall dependencies and confirm the lockfile updates cleanly.
- [ ] Verify `npm run dev` starts locally and `/` plus `/library` render successfully.
- [ ] Verify `npm run build` succeeds locally.
- [ ] Confirm `npm audit` no longer reports the current Next.js 14.x advisory chain.

Why this exists:
- `010-goal-prepare-nextjs-vercel-foundation.md` established the Next.js foundation and upgraded to the latest verified 14.x patch.
- Remaining audit findings require a major upgrade path, so this is tracked as a separate task before auth and data work expand the migration surface.

Risks:
- Next.js 16 may require React or tooling updates.
- `next.config.js` behavior or defaults may change.
- Vercel/runtime behavior should be rechecked after the upgrade.

Verification:
- `cd app-next && npm install`
- `cd app-next && npm run dev`
- Open `http://localhost:3000/` and `http://localhost:3000/library`
- `cd app-next && npm run build`
- `cd app-next && npm audit`

