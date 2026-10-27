# Changelog

## 2.0.0 — 2026-10-27
- Moved to GitHub Pages as the user site mdism.github.io with the custom domain tools.shaikhismail.com
- Landing page lists repos tagged shaikhismail-tool; bot check moved to a Cloudflare Worker (worker/); 404 page added
- Removed cPanel-only parts (.htaccess, PHP endpoints, .cpanel.yml)

## 1.0.0 — 2026-10-27
- Landing page listing every free tool, shared privacy page
- Server-wide security rules (.htaccess) and the Cloudflare Turnstile check (api/verify.php) for all tools
