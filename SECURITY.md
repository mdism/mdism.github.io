# Security

mdism.github.io is the landing site for https://tools.shaikhismail.com and holds what every tool shares.

## What protects the tools

- **GitHub Pages**: static hosting, HTTPS enforced. No server code runs on the site.
- **Content Security Policy** in every page (`<meta>` tag): scripts only from the site and Cloudflare Turnstile; pages may only talk to the site, the bot-check Worker and (on this landing page) the GitHub API.
- **Bot check**: `worker/turnstile-verify.js` runs as a Cloudflare Worker. It accepts only POSTs from https://tools.shaikhismail.com, limits the token size, confirms the token with Cloudflare, checks the hostname, and stores or logs nothing. The Turnstile secret is a Worker secret in Cloudflare and is never in any repo.
- **No framing**: pages refuse to run inside another site's frame.
- **Optional extra**: put tools.shaikhismail.com behind Cloudflare's free proxy to add security headers and Bot Fight Mode; GitHub Pages itself can't set custom headers.

## Reporting a problem

Email hello@shaikhismail.com. Please do not open a public issue for a security problem.
