# Goal: Upgrade `app-next` to Next.js 16

- [x] Review Next.js 16 upgrade notes for App Router compatibility and any config changes needed by the current `app-next` skeleton.
- [x] Upgrade `next` in `app-next/package.json` to a stable `16.x` version and align related dependencies if required.
- [x] Reinstall dependencies and confirm the lockfile updates cleanly.
- [ ] Verify `npm run dev` starts locally and `/` plus `/library` render successfully.
- [ ] Verify `npm run build` succeeds locally.
- [x] Confirm `npm audit` no longer reports the current Next.js 14.x advisory chain.

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

Notes:
- Upgraded `app-next` to `next@16.2.0`, `react@19.2.0`, and `react-dom@19.2.0`.
- Clean install completed successfully and `npm audit` is now clean.
- Local build is currently blocked by the terminal runtime using system Node.js `18.19.1` from Ubuntu packages (`/usr/bin/node`); Next.js 16 requires Node.js `>=20.9.0`.
- Updated `app-next/.nvmrc` to `20.9.0` so local and CI/Vercel runtimes can align with the new engine requirement.
- This WSL shell does not have `nvm` installed, so final local dev/build verification should use any available Node.js 20+ installation method before rerunning `npm run dev` and `npm run build`.
