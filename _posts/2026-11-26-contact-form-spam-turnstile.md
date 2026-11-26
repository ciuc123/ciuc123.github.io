---
layout: post
title: "Contact Form Spam That Never Loaded the Form"
description: "Three one-line inquiries in three languages, one empty hidden field. How I spotted bots posting straight to my Worker, logged them and added Turnstile."
date: 2026-11-26
tags: [cloudflare-workers, turnstile, spam, contact-form, security]
tldr:
  - "Three inquiries in three days asked for my price in English, Albanian and Welsh, from the same name. All three had an empty source_page, which my form's script never sends."
  - "An empty field your page always fills means the request skipped the page: the bot posted straight to /api/contact. A honeypot and CORS don't stop that."
  - "Dropping posts without source_page, with a silent success, stopped this bot. It cost one if statement."
  - "One JSON log line per request (country, network, user agent, outcome, no IP or message) shows what gets through next."
  - "Cloudflare Turnstile, verified in the Worker and enforced only once the secret exists, stops bots that copy the field. Order the rollout or real messages fail."
faq:
  - q: "How do I tell a bot contact form submission from a real one?"
    a: "Check a field your own page always fills. My form's script sets a hidden source_page to the page the visitor came from, or to (direct). All three suspect messages arrived with it empty, so they were posted straight to the endpoint without loading the page. That is a stronger signal than the odd wording or the language."
  - q: "Why didn't my honeypot field stop the spam?"
    a: "A honeypot catches bots that fill in every field of the HTML form. A bot that posts directly to the endpoint just leaves the honeypot fields out, so the check sees nothing. CORS doesn't help either: it only stops browsers from reading the response, not scripts from sending the request."
  - q: "Can I add Cloudflare Turnstile without breaking the live form?"
    a: "Yes, if the Worker enforces the check only once its secret is set. Deploy the Worker first, then publish the page with the widget, then set the secret. Set the secret before the page sends a token and every real message fails."
---

My contact form received three messages from a bot, and one empty hidden field proved it. Each one asked for my price in a different language, and all three arrived with an empty `source_page`, a field my own page always fills. They never loaded the form: something posted straight to the endpoint. Here is how I spotted it, what the Worker logs now, and how I added Cloudflare Turnstile without losing a real message.

The form itself is new. In [My Contact Form Never Sent a Single Email](/posts/2026-11-20-seo-client-zero-1-contact-form/) I replaced a fake one with a Cloudflare Worker on `/api/contact` that emails me through Resend. Six days later, the first bot found it.

## What did the messages look like?

Three emails, same sender name, same throwaway-looking Gmail address:

| Received | Message |
|---|---|
| November 24, 22:46 | Hi, I wanted to know your price. |
| November 25, 06:07 | Hi, kam dashur të di çmimin tuaj |
| November 26, 12:41 | Hi, roeddwn i eisiau gwybod eich pris. |

The second is Albanian and the third Welsh, both saying the same thing. The name was `RobertCep`. Nothing on my site is in either language, and a real buyer asks about a project, not "your price". Replying would only confirm that someone reads the inbox.

Odd wording is a hint, not proof. The proof was a line in every email: `Source page: -`.

## How do you tell a bot submission from a real one?

Look for a field your own page always fills. My form has a hidden `source_page` input, and the site's script sets it before sending: the page the visitor came from, or `(direct)` when there is none. The Worker prints `-` only when the field arrives empty. A visitor using the form can't send it empty, so all three messages came from something that posted to `/api/contact` without running the page.

```javascript
// assets/js/main.js: what a real visitor always sends
function leadSourcePage() {
  // ...the stored page, or the referrer...
  return '(direct)';
}
```

## Why didn't the honeypot or CORS stop it?

The form already had a honeypot: two hidden fields, `_gotcha` and `botcheck`, that people never see and form-filling bots tend to fill. The Worker drops anything that fills them. But a bot that posts directly sends only the fields it wants, so the honeypot is simply absent and the check passes.

CORS didn't help either. The Worker only sends `Access-Control-Allow-Origin` for `https://ciuculescu.com`, but that only stops a browser on another site from reading the answer. A script sending a POST with `curl` or anything else never asks.

## How did I stop it?

With one `if`. A post without a source page gets the same answer as a honeypot hit, a `200` with `{"success":true}`, and no email. The bot can't tell it was dropped.

```javascript
export function missingSourcePage(fields) {
  return !String(fields.source_page || '').trim();
}

// in the request handler, after the honeypot check
if (missingSourcePage(fields)) {
  log('no_source_page', fields);
  return json({ success: true }, 200, cors);
}
```

Who could this block by mistake? Only a visitor with JavaScript turned off, and they already got a raw JSON reply instead of a thank-you message, so that path was broken anyway. It stops this bot, not a smarter one: a bot that copies the field, or loads the page in a real browser, gets through. That needs Turnstile.

## What should a contact form endpoint log?

Enough to tell a bot from a person, and no personal data. Until now the Worker logged nothing, so I couldn't look back at who sent the three messages. Now every request writes one JSON line: the outcome, Cloudflare's country and network for the connection, the user agent, `Origin` and `Referer`, the source page, the email's domain and the message length. No IP, no name, no full address, no message text.

```javascript
export function requestSummary(request, outcome, fields = {}, extra = {}) {
  const cf = request.cf || {};
  const h = (name) => (request.headers.get(name) || '').slice(0, 200);
  const email = String(fields.email || '');
  return {
    event: 'contact',
    outcome, // sent, honeypot, no_source_page, invalid, turnstile_failed, ...
    country: cf.country || null,
    asn: cf.asn || null,
    as_org: cf.asOrganization || null,
    user_agent: h('User-Agent'),
    origin: h('Origin'),
    referer: h('Referer'),
    source_page: String(fields.source_page || '').slice(0, 100) || null,
    email_domain: email.includes('@') ? email.split('@').pop().slice(0, 100).toLowerCase() : null,
    message_length: String(fields.message || '').length,
    ...extra,
  };
}
```

This is the line my own test post produced, sent with `curl` and no source page, after the deploy (I swapped my provider for a documentation ASN and a made-up name):

```json
{"event":"contact","outcome":"no_source_page","country":"RO","asn":64500,
 "as_org":"Example Residential ISP","user_agent":"curl/8.5.0","origin":"",
 "referer":"","source_page":null,"email_domain":"example.com","message_length":2}
```

`npx wrangler tail` shows these live. `[observability] enabled = true` in `wrangler.toml` turns on Workers Logs, so I can also search them in the dashboard. The free plan keeps them for seven days. A contact form writes a handful of lines a day, far below the free allowance.

## How do you add Cloudflare Turnstile to a Worker?

Turnstile is Cloudflare's CAPTCHA replacement, free on the standard plan and usually invisible. The page renders a widget that adds a token to the form, and the Worker checks the token with Cloudflare's `siteverify` endpoint using the secret key. Three pieces:

1. **The page.** The site key is public, so it goes in `_config.yml`, and the contact page renders the widget only when it is set:
   {% raw %}
   ```html
   <div class="cf-turnstile" data-sitekey="{{ cf.turnstile_site_key }}" data-action="contact"></div>
   <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
   ```
   {% endraw %}
   The widget adds a hidden `cf-turnstile-response` input, so the existing `new FormData(form)` sends the token without changes. A token works once and expires after 300 seconds, so the script calls `turnstile.reset()` after every attempt.
2. **The Worker.** It checks the token after validating the fields, so a typo in the email doesn't use up the token:
   ```javascript
   export async function verifyTurnstile(token, request, env) {
     if (!env.TURNSTILE_SECRET) return { ok: true, codes: ['not_configured'] };
     if (!token) return { ok: false, codes: ['missing-input-response'] };
     const body = new FormData();
     body.append('secret', env.TURNSTILE_SECRET);
     body.append('response', String(token).slice(0, 2048));
     const ip = request.headers.get('CF-Connecting-IP');
     if (ip) body.append('remoteip', ip);
     const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body });
     const data = await res.json();
     return { ok: data.success === true, codes: data['error-codes'] || [] };
   }
   ```
   A failed check answers `403` with a visible message ("The spam check failed. Please reload the page and try again."), not a silent success: a real person whose check failed needs to know.
3. **The secret**, set with `npx wrangler secret put TURNSTILE_SECRET`, never committed.

## In what order do you roll it out?

The first line of `verifyTurnstile` is what makes the order safe: without the secret, the Worker accepts posts without a token. So:

1. Deploy the Worker. Nothing changes for visitors yet.
2. Publish the page with the widget. Real visitors now send a token, and the Worker still doesn't require one.
3. Set the secret. Saving a secret redeploys the Worker, and from that moment a post without a valid token gets a `403`.

Swap steps 2 and 3 and, until the page is live, every real visitor's message fails. After step 3, the same `curl` post, this time with a source page, got `{"success":false,"message":"The spam check failed. Please reload the page and try again."}` and sent nothing. A real message from the live form arrived as usual.

## What went wrong on the way?

Two things, both worth knowing before you copy this.

**A TOML table swallowed my route.** I added the logs setting in the middle of `wrangler.toml`:

```toml
compatibility_date = "2026-11-01"

[observability]
enabled = true

routes = [{ pattern = "ciuculescu.com/api/contact", zone_name = "ciuculescu.com" }]
```

In TOML, every key after a `[table]` header belongs to that table until the next header. So `routes` became `observability.routes`, and wrangler said so: `Unexpected fields found in observability field: "routes"`. I missed the warning in the deploy output. The existing route kept working, but the deploy no longer listed it, and with no routes in the config, wrangler turned on the `workers.dev` address by default. The fix is to put tables after all the top-level keys. After that, the deploy listed `ciuculescu.com/api/contact` again and `workers.dev` was off.

**The secret was saved under the wrong name.** `wrangler secret put` takes the name as an argument and asks for the value at a prompt. The key ended up as the name, so the Worker never found `TURNSTILE_SECRET`, the check stayed off, and the key itself was in plain sight in the secret listing. `npx wrangler secret list` showed it right away. I deleted that secret, rotated the key in the Turnstile dashboard (one click, since the old one had been on screen), and set the new one under the right name. The takeaway: after setting a secret, list the secrets and send one request that should now fail.

## What does it cost?

Nothing at this scale. The Workers free plan covers 100,000 requests a day, Turnstile's free plan covers sites like this one, and a few log lines a day are far below the Workers Logs allowance. The one-`if` source page check cost nothing to run and stopped the bot that started this. Turnstile is there for the next bot, the one that loads the page first.

## Sources

- [Cloudflare Turnstile: server-side validation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/)
- [Cloudflare Turnstile: plans](https://developers.cloudflare.com/turnstile/plans/)
- [Cloudflare Turnstile: FAQ (single-use tokens, 300-second validity)](https://developers.cloudflare.com/turnstile/frequently-asked-questions/)
- [Cloudflare Workers: pricing and free plan limits](https://developers.cloudflare.com/workers/platform/pricing/)
- [Cloudflare Workers Logs](https://developers.cloudflare.com/workers/observability/logs/workers-logs/)
- [Cloudflare observability pricing](https://developers.cloudflare.com/observability/pricing/)
- [Wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)
- [Wrangler commands: secret](https://developers.cloudflare.com/workers/wrangler/commands/#secret)
- [TOML specification: tables](https://toml.io/en/v1.0.0#table)
- [MDN: Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

*The bot that started this only had to find a URL; everything it needed to know was in my own email: `Source page: -`.*
