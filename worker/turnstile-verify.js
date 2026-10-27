/*
 * Cloudflare Worker: confirms Turnstile tokens for the free tools on tools.shaikhismail.com.
 * GitHub Pages can't run server code, so this does the job verify.php used to do.
 *
 * Setup (Cloudflare dashboard → Workers & Pages → Create → Worker → paste this file → Deploy):
 *   Settings → Variables and Secrets → add a Secret named TURNSTILE_SECRET with your Turnstile secret key.
 * Free plan: 100,000 requests a day. Nothing is stored or logged by this code.
 */
const ALLOWED_ORIGINS = ['https://tools.shaikhismail.com'];
const ALLOWED_HOSTNAME = 'tools.shaikhismail.com';
const SITEVERIFY = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const cors = {
      'Access-Control-Allow-Origin': ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
      'Access-Control-Allow-Methods': 'POST',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
      'Vary': 'Origin',
    };
    const reply = (status, body) => new Response(JSON.stringify(body), {
      status, headers: { ...cors, 'Content-Type': 'application/json', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' },
    });

    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (request.method !== 'POST') return reply(405, { ok: false, error: 'method' });
    if (!ALLOWED_ORIGINS.includes(origin)) return reply(403, { ok: false, error: 'origin' });
    if (!env.TURNSTILE_SECRET) return reply(500, { ok: false, error: 'not configured' });

    const raw = await request.text();
    if (raw.length > 4096) return reply(400, { ok: false, error: 'token' });
    let token = '';
    try { token = String(JSON.parse(raw).token || ''); } catch (e) { /* falls through to the check below */ }
    if (!token || token.length > 2048) return reply(400, { ok: false, error: 'token' });

    // No visitor IP is sent, and nothing about the request is kept.
    const res = await fetch(SITEVERIFY, {
      method: 'POST',
      body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: token }),
    }).then(r => r.json()).catch(() => null);
    if (!res) return reply(502, { ok: false, error: 'upstream' });

    return reply(200, { ok: res.success === true && res.hostname === ALLOWED_HOSTNAME });
  },
};
