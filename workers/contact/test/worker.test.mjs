import test from 'node:test';
import assert from 'node:assert/strict';
import worker, { validate, isSpam, buildEmail } from '../src/index.js';

const env = {
  RESEND_API_KEY: 'test-key',
  MAIL_FROM: 'site <contact@example.com>',
  MAIL_TO: 'me@example.com',
  SUBJECT_PREFIX: 'New inquiry',
  ALLOWED_ORIGINS: 'https://ciuculescu.com',
};

function post(fields, origin = 'https://ciuculescu.com') {
  const fd = new FormData();
  for (const [k, v] of Object.entries(fields)) fd.append(k, v);
  return new Request('https://ciuculescu.com/api/contact', { method: 'POST', body: fd, headers: { Origin: origin } });
}

const good = { name: 'Ana', email: 'ana@example.com', message: 'Need a Laravel upgrade', source_page: '/posts/x/' };

function mockResend(status = 200) {
  const calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, body: JSON.parse(init.body), auth: init.headers.Authorization });
    return new Response('{}', { status });
  };
  return calls;
}

test('validate rejects missing and bad fields', () => {
  assert.ok(validate({ name: 'a', email: '', message: 'm' }).error);
  assert.ok(validate({ name: 'a', email: 'nope', message: 'm' }).error);
  assert.ok(validate({ name: 'a', email: 'a@b.co', message: 'x'.repeat(5001) }).error);
  assert.deepEqual(validate(good).value, good);
});

test('honeypot detection', () => {
  assert.equal(isSpam({ _gotcha: 'http://spam' }), true);
  assert.equal(isSpam({ botcheck: 'on' }), true);
  assert.equal(isSpam({ _gotcha: '' }), false);
});

test('email escapes HTML, strips newlines from subject, sets reply_to', () => {
  const m = buildEmail({ ...good, name: 'Eve\r\nBcc: x', message: '<script>' }, env);
  assert.ok(!/[\r\n]/.test(m.subject));
  assert.ok(m.html.includes('&lt;script&gt;'));
  assert.equal(m.reply_to, good.email);
  assert.deepEqual(m.to, ['me@example.com']);
});

test('valid submission is sent to Resend', async () => {
  const calls = mockResend(200);
  const res = await worker.fetch(post(good), env);
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), { success: true });
  assert.equal(calls.length, 1);
  assert.equal(calls[0].url, 'https://api.resend.com/emails');
  assert.equal(calls[0].auth, 'Bearer test-key');
  assert.ok(calls[0].body.text.includes('/posts/x/'));
  assert.equal(res.headers.get('Access-Control-Allow-Origin'), 'https://ciuculescu.com');
});

test('honeypot submission returns success but sends nothing', async () => {
  const calls = mockResend(200);
  const res = await worker.fetch(post({ ...good, _gotcha: 'x' }), env);
  assert.equal(res.status, 200);
  assert.equal(calls.length, 0);
});

test('invalid submission returns 422 and sends nothing', async () => {
  const calls = mockResend(200);
  const res = await worker.fetch(post({ ...good, email: 'bad' }), env);
  assert.equal(res.status, 422);
  assert.equal((await res.json()).success, false);
  assert.equal(calls.length, 0);
});

test('Resend failure returns 502 with success false', async () => {
  mockResend(500);
  const res = await worker.fetch(post(good), env);
  assert.equal(res.status, 502);
  assert.equal((await res.json()).success, false);
});

test('foreign origin gets no CORS header; GET is rejected', async () => {
  mockResend(200);
  const res = await worker.fetch(post(good, 'https://evil.example'), env);
  assert.equal(res.headers.get('Access-Control-Allow-Origin'), null);
  const get = await worker.fetch(new Request('https://ciuculescu.com/api/contact'), env);
  assert.equal(get.status, 405);
});
