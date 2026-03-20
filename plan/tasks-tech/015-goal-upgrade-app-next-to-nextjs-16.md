# Goal: Upgrade `app-next` to Next.js 16

- [x] Review Next.js 16 upgrade notes for App Router compatibility and any config changes needed by the current `app-next` skeleton.
- [x] Upgrade `next` in `app-next/package.json` to a stable `16.x` version and align related dependencies if required.
- [x] Reinstall dependencies and confirm the lockfile updates cleanly.
- [x] Verify `npm run dev` starts locally and `/` plus `/library` render successfully.
- [x] Verify `npm run build` succeeds locally.
- [x] Confirm `npm audit` no longer reports the current Next.js 14.x advisory chain.

Why this exists:
- `010-goal-prepare-nextjs-vercel-foundation.md` established the Next.js foundation and upgraded to the latest verified 14.x patch.
- Remaining audit findings required a major upgrade path, so this task moved `app-next` onto the supported Next.js 16 line before auth and data work expand the migration surface.

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
- Updated `app-next/.nvmrc` to `20.9.0` and added `app-next/.npmrc` with `engine-strict=true`.
- Verified `npm install`, `npm run build`, and `npm audit` under Node.js `20.9.0`.
- Verified local route responses for `/library` and started the dev server successfully; the root route is the current static home page in the upgraded Next.js app.
