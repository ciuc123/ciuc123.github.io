// Contact form -> Resend email. Deployed as a Cloudflare Worker on ciuculescu.com/api/contact.
// Secrets: RESEND_API_KEY (wrangler secret put RESEND_API_KEY). Vars: see wrangler.toml.

const MAX = { name: 200, email: 320, message: 5000, source_page: 300 };

function json(body, status, cors) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...cors },
  });
}

function corsHeaders(request, env) {
  const origin = request.headers.get('Origin') || '';
  const allowed = (env.ALLOWED_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean);
  if (!allowed.includes(origin)) return {};
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Accept',
    Vary: 'Origin',
  };
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

export function validate(fields) {
  const name = String(fields.name || '').trim();
  const email = String(fields.email || '').trim();
  const message = String(fields.message || '').trim();
  const source_page = String(fields.source_page || '').trim().slice(0, MAX.source_page);
  if (!name || !email || !message) return { error: 'Please fill in name, email and project details.' };
  if (name.length > MAX.name || email.length > MAX.email || message.length > MAX.message) {
    return { error: 'One of the fields is too long.' };
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return { error: 'Please enter a valid email address.' };
  return { value: { name, email, message, source_page } };
}

export function isSpam(fields) {
  return Boolean(fields._gotcha) || Boolean(fields.botcheck);
}

// The site's script always fills source_page (at least "(direct)"), so an empty one means the
// request did not come from the form page: a bot posting straight to /api/contact.
export function missingSourcePage(fields) {
  return !String(fields.source_page || '').trim();
}

// One JSON line per request, for Workers Logs / wrangler tail. No IP, name, address or message:
// only what tells a bot from a person (network, country, browser, where it came from).
export function requestSummary(request, outcome, fields = {}) {
  const cf = request.cf || {};
  const h = (name) => (request.headers.get(name) || '').slice(0, 200);
  const email = String(fields.email || '');
  return {
    event: 'contact',
    outcome,
    country: cf.country || null,
    asn: cf.asn || null,
    as_org: cf.asOrganization || null,
    colo: cf.colo || null,
    bot_score: (cf.botManagement && cf.botManagement.score) || null,
    user_agent: h('User-Agent'),
    origin: h('Origin'),
    referer: h('Referer'),
    content_type: h('Content-Type'),
    source_page: String(fields.source_page || '').slice(0, 100) || null,
    email_domain: email.includes('@') ? email.split('@').pop().slice(0, 100).toLowerCase() : null,
    message_length: String(fields.message || '').length,
  };
}

export function buildEmail(lead, env) {
  const subject = `${env.SUBJECT_PREFIX || 'New inquiry'}: ${lead.name}`.replace(/[\r\n]+/g, ' ').slice(0, 200);
  const text = `Name: ${lead.name}\nEmail: ${lead.email}\nSource page: ${lead.source_page || '-'}\n\n${lead.message}\n`;
  const html =
    `<p><strong>Name:</strong> ${escapeHtml(lead.name)}<br>` +
    `<strong>Email:</strong> ${escapeHtml(lead.email)}<br>` +
    `<strong>Source page:</strong> ${escapeHtml(lead.source_page || '-')}</p>` +
    `<p style="white-space:pre-wrap">${escapeHtml(lead.message)}</p>`;
  return { from: env.MAIL_FROM, to: [env.MAIL_TO], reply_to: lead.email, subject, text, html };
}

async function readFields(request) {
  const type = request.headers.get('Content-Type') || '';
  if (type.includes('application/json')) return await request.json();
  const form = await request.formData();
  return Object.fromEntries(form.entries());
}

export default {
  async fetch(request, env) {
    const log = (outcome, fields) => console.log(JSON.stringify(requestSummary(request, outcome, fields)));
    const cors = corsHeaders(request, env);
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (request.method !== 'POST') return json({ success: false, message: 'Method not allowed' }, 405, cors);

    let fields;
    try {
      fields = await readFields(request);
    } catch (err) {
      log('bad_body');
      return json({ success: false, message: 'Invalid request body.' }, 400, cors);
    }

    // Honeypot hit: answer like a success so bots learn nothing, send nothing.
    if (isSpam(fields)) {
      log('honeypot', fields);
      return json({ success: true }, 200, cors);
    }
    // Same silent success for posts that skipped the form page.
    if (missingSourcePage(fields)) {
      log('no_source_page', fields);
      return json({ success: true }, 200, cors);
    }

    const checked = validate(fields);
    if (checked.error) {
      log('invalid', fields);
      return json({ success: false, message: checked.error }, 422, cors);
    }

    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(buildEmail(checked.value, env)),
    });
    if (!res.ok) {
      log('resend_error', fields);
      console.log('resend error', res.status, await res.text());
      return json({ success: false, message: 'Email service error.' }, 502, cors);
    }
    log('sent', fields);
    return json({ success: true }, 200, cors);
  },
};
