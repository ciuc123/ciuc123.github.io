---
slug: contact-form-spam-turnstile
status: drafting
inbox: none (three bot inquiries on ciuculescu.com, November 24 to 26, 2026)
---

# Brief: bot inquiries that never loaded the contact form, and how I stopped them

**Reader:** a developer or small business owner with a static site and a hand-rolled contact form (a serverless function or Worker that emails them), getting short odd inquiries and wondering whether they are real.

**Main question:** how do you tell a bot contact form submission from a real one, and stop it without a CAPTCHA wall?

**Related questions:**
- Why doesn't a honeypot field stop contact form spam?
- Does CORS stop bots posting to my form endpoint?
- What should a contact form endpoint log without storing personal data?
- How do you add Cloudflare Turnstile to a Cloudflare Worker without breaking the live form?

**Intent:** learn (diagnose, then fix)

**Service it supports:** none. The default CTA (contact) applies.

**Unique angle / proof:** three real messages (English, Albanian, Welsh), the one empty field that gave them away, the actual Worker code, a real log line, the rollout order, and two mistakes made on the way (a TOML table that swallowed the routes key, a secret saved under the wrong name).

**Answer in one paragraph:** look for what your own page always sends. My form's script fills a source_page field, at least "(direct)", and all three messages arrived with it empty, so they were posted straight to the endpoint. A honeypot and CORS don't stop that. Dropping posts with that field empty stopped this bot, a log line per request shows the next one, and Cloudflare Turnstile, verified in the Worker, stops bots that copy the field.

**Sources to cite:** Turnstile server-side validation and plans, Turnstile FAQ (single-use tokens, 300 s), Workers pricing, Workers Logs, Cloudflare observability pricing, wrangler configuration, MDN CORS.

## Distribution
- [ ] LinkedIn: hook (three messages, three languages, one empty field) + 3 takeaways, link in the first comment (Andrei)
- [ ] Add to `_data/llms.yml`? No.
