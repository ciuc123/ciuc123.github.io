# Contact form Worker (Resend)

`/contact/` posts to `/api/contact`. This Cloudflare Worker owns that path on the
`ciuculescu.com` zone. It checks the honeypot (`_gotcha`, `botcheck`), validates the fields and
sends the inquiry through [Resend](https://resend.com), with `reply_to` set to the visitor so
replying from the inbox goes straight to them. The site stays static. The Resend key lives only
in the Worker.

Responses are JSON: `{ "success": true }`, or `{ "success": false, "message": "..." }` with
status 422 (bad input), 502 (Resend failed) or 405. `assets/js/main.js` shows the message and,
on failure, the email fallback.

## Setup (once)

1. Resend: the sending domain is `email.content.ciuculescu.com` (verified, DNS records in
   Cloudflare). Use an API key with "Sending access".
2. `MAIL_FROM` must be on that domain; `MAIL_TO` is the inbox that receives inquiries. Both are in
   `wrangler.toml`.
3. Deploy:
   ```sh
   cd workers/contact
   npx wrangler login
   npx wrangler secret put RESEND_API_KEY
   npx wrangler deploy
   ```
4. Smoke test: `curl -s -X POST https://ciuculescu.com/api/contact -F name=Test -F email=you@example.com -F message=hi`
   should return `{"success":true}` and the email should arrive.

## Tests

`npm test` (Node 18+, no dependencies) runs the unit tests with Resend mocked.
