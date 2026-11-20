---
layout: post
title: "My Contact Form Never Sent a Single Email"
description: "First fix in my SEO and AI-search program on my own site: the contact form faked success and dropped every inquiry. How I found it, fixed it and proved it."
date: 2026-11-20
tags: [seo, conversion, cloudflare-workers, resend, client-zero]
series: seo-client-zero
series_part: 1
---

I'm starting an SEO, answer-engine (AEO) and AI-search (GEO) program on this site before I offer it to anyone else. ciuculescu.com is client zero: every task gets done here first, checked, and measured against a baseline, and this series documents each one.

The first audit turned up something worse than a missing meta tag. **The contact form on this site never sent anything.** You typed your name, email and project, clicked *Send Inquiry*, waited two seconds, got a friendly "Thank you for your inquiry!" pop-up, and your message went nowhere. That's been true since the form went live. I have no way of knowing how many people wrote to me.

So before chasing rankings, the first task was making sure the site can turn a visitor into a conversation.

## Why lead capture comes first

The whole plan has ten areas: measurement, technical foundation, identity and trust, positioning and keywords, on-page, answer engines, AI assistants, conversion, authority, and content operations. They're roughly in dependency order, with one exception I pulled to the front: **conversion**.

Traffic that can't convert is wasted. If the only way to reach me is broken, every improvement in rankings or AI citations just sends more people into a dead end. It's also the cheapest win: one afternoon of work against an unknown number of lost leads.

## The bug

This was the entire form handler in `assets/js/main.js`:

```javascript
// Simulate form submission (replace with actual form handler)
setTimeout(() => {
  alert('Thank you for your inquiry! I will get back to you within 24 hours.');
  this.reset();
  button.classList.remove('loading');
  button.disabled = false;
}, 2000);
```

The comment says it all. A placeholder from the first version of the site made it to production and stayed there, because from the outside it *looked* like it worked. Nobody gets an error, so nobody reports one.

## Choosing a backend for a static site

The site is Jekyll on GitHub Pages, behind Cloudflare. There's no server to receive a POST. The options I considered:

- **Formspree or Web3Forms:** a hosted form endpoint, free tier, no code. The quickest fix and a fine default for most small sites.
- **MailerLite:** already loaded on the site, but its forms are built for newsletter signups, not inquiries.
- **Resend:** a transactional email API I wanted to use anyway. It needs a secret API key, and anything in a static page is public, so it can't be called from the browser.

I went with Resend behind a **Cloudflare Worker**. The site already runs through Cloudflare, so the Worker can own one path on the same domain, `ciuculescu.com/api/contact`. The key stays on Cloudflare as a secret, the page never sees it, and because it's the same origin there's no cross-domain setup in the browser.

## The Worker

It does four things: drop bots, validate, send, answer in JSON.

```javascript
// Honeypot hit: answer like a success so bots learn nothing, send nothing.
if (isSpam(fields)) return json({ success: true }, 200, cors);

const checked = validate(fields);
if (checked.error) return json({ success: false, message: checked.error }, 422, cors);

const res = await fetch('https://api.resend.com/emails', {
  method: 'POST',
  headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
  body: JSON.stringify(buildEmail(checked.value, env)),
});
if (!res.ok) return json({ success: false, message: 'Email service error.' }, 502, cors);
return json({ success: true }, 200, cors);
```

A few details that matter more than they look:

- **Honeypot instead of a CAPTCHA.** A hidden field real visitors never see. Bots fill it, get a fake success, and nothing is sent. No friction for humans.
- **`reply_to` is the visitor.** The email comes from my sending domain, but hitting *Reply* in my inbox goes straight to the person who wrote.
- **The email body includes the page the visitor came from.** More on that below.
- **The subject line has newlines stripped** and the HTML body is escaped, so a crafted name can't inject headers or markup.

## The form, done properly

On the page side, the fake `setTimeout` became a real `fetch` with real outcomes:

- **Success** shows an inline message ("Thanks, your message was sent. I reply within 24 business hours.") and clears the form.
- **Failure** keeps what the visitor typed and says so plainly: "Sorry, the message could not be sent. Please email me directly at …" with the address.
- **No `alert()` anywhere.**
- **A visible email address under the form**, for people who'd rather just write an email.

## Measuring leads, not just sending them

A lead is only useful for SEO if you know where it came from. The site already had PostHog, so I added three events:

- `cta_clicked` with which CTA (post footer, nav, home hero) and the page it was on.
- `lead_submitted` with `source_page`: the post or page the visitor was reading before they went to the contact page.
- `lead_submit_failed`, so a broken backend shows up as a number instead of silence.

The source page is remembered for the browser tab when someone clicks a link to the contact page, and falls back to the referrer. It's also included in the email itself, so I can see "this inquiry came from the Laravel queues post" without opening analytics.

I also added a call to action at the end of every post, including this one. Before, a post ended with "← Back to Posts", and a reader who liked it had no obvious next step.

## How I checked it

"Looks fine" is how the original bug survived, so every claim got a test:

1. **Unit tests for the Worker** (8, Node's built-in test runner, Resend mocked): valid input sends exactly one email with the right `reply_to`; honeypot sends nothing; bad input gets a 422; a Resend failure gets a 502; other origins get no CORS header.
2. **Browser test against the built site** (12 checks, headless Chromium): click the CTA on a post, land on the contact page, submit, and confirm the email payload contains that post as the source, `lead_submitted` fires, the form resets, the honeypot sends nothing, and a backend failure shows the email fallback with no pop-up.
3. **Live checks after deploy:** GET returns 405, a bad email returns 422, the honeypot returns success without sending, and a real test inquiry landed in my inbox.
4. **A real submission on the live site** from a browser: success message shown, `lead_submitted` recorded.

One surprise from the live check: Cloudflare's *Email Obfuscation* feature rewrites email addresses in the HTML into `[email protected]` and decodes them with its own script. My error message reads the address from that link, so I checked in a real browser that the decoded address is what visitors see. It is, but this is exactly the kind of thing that passes locally and breaks in production.

## Result

| Metric | Before | After |
|---|---|---|
| Inquiries that reach my inbox | 0% (form faked success) | 100% of test submissions |
| Lead source tracked | No | Yes, page + CTA |
| Call to action on posts | 0 of 23 | 23 of 23 |
| Failure visible to the visitor | Never (always "Thank you") | Yes, with an email fallback |

The number that matters, leads per month, starts at zero by construction. I'll report it in later parts once there's enough data to be honest about.

## Check this on your own site

This takes five minutes and I'd do it on any site, today:

1. **Submit your own contact form** with a real address. Did the email arrive? Check spam too.
2. **Find out where it goes.** Which service, which inbox, who reads it? Forms often point at an old address or a developer's test account.
3. **Break it on purpose** if you can (wrong endpoint, offline). Does the visitor see an error, or a fake "thank you"?
4. **Show an email address** next to the form as a fallback.
5. **Track the submit as a conversion** in your analytics, with the page the visitor came from.
6. **Put the next step at the end of every article.** People who just read 1,500 words of yours are the warmest visitors you'll get.

Then put a reminder in your calendar to repeat step 1 every month.

## Next

Part 2 is the audit tool: a small dependency-free Python script that checks every page on every build (titles, descriptions, structured data, broken links, and, yes, that the contact form has a real endpoint and every post has a call to action) so this kind of bug can't quietly come back.

*The most expensive SEO bug on my site wasn't about search at all. It was a two-second timer that said "thank you" and threw the message away.*
