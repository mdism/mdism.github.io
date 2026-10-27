# Security

tools-hub serves https://tools.shaikhismail.com/ and provides the protection every tool folder under it relies on.

## What protects the tools

- **`public/.htaccess`** (applies to the whole subdomain, including every tool folder):
  HTTPS only with HSTS; a strict Content Security Policy (scripts only from this site and Cloudflare Turnstile, and pages may only talk back to this site);
  `X-Frame-Options: DENY`, `nosniff`, `Referrer-Policy: no-referrer`, a locked-down `Permissions-Policy`;
  only GET/HEAD allowed (POST only to `/api/verify.php`); dotfiles, `.git` and directory listings hidden; PHP/WordPress probes and known scanner bots refused.
- **`public/api/verify.php`**: confirms each Turnstile token with Cloudflare, checks the hostname, accepts only same-origin POSTs of a limited size, and stores or logs nothing.
- **Secret handling**: the Turnstile secret is never in this repo. It is read from `~/.config/shaikhismail-tools/turnstile.php` on the server (format in `config/turnstile.example.php`). `config/turnstile.php` is git-ignored.

## Reporting a problem

Email hello@shaikhismail.com. Please do not open a public issue for a security problem.
