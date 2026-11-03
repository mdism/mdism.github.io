# Changelog

## 2.1.0 — 2026-11-03
- Three new tools (PDF to Image, Image to PDF, Age Calculator), breadcrumb on every page, tool cards built into the page for search engines, fuller sitemap and share previews. New: scripts/update_index.py; new_tool.py now adds the breadcrumb, input → process → output strip, FAQ and SEO tags, and leaves the first commit to you.

## 2.0.0 — 2026-10-27
- Moved to GitHub Pages as the user site mdism.github.io with the custom domain tools.shaikhismail.com
- Landing page lists repos tagged shaikhismail-tool; bot check moved to a Cloudflare Worker (worker/); 404 page added
- Removed cPanel-only parts (.htaccess, PHP endpoints, .cpanel.yml)

## 1.0.0 — 2026-10-27
- Landing page listing every free tool, shared privacy page
- Server-wide security rules (.htaccess) and the Cloudflare Turnstile check (api/verify.php) for all tools
