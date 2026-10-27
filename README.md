# tools-hub

The landing page and shared server setup for **https://tools.shaikhismail.com**, the free browser tools by [Mohammed Ismail Shaikh](https://shaikhismail.com).

Every tool is its own repo and deploys into its own folder of this subdomain:

| Repo | Address |
|---|---|
| tools-hub (this repo) | https://tools.shaikhismail.com/ |
| [tool-image-compressor](https://github.com/mdism/tool-image-compressor) | https://tools.shaikhismail.com/image-compressor/ |
| [tool-pdf-merge-split](https://github.com/mdism/tool-pdf-merge-split) | https://tools.shaikhismail.com/pdf-merge-split/ |
| [tool-exam-photo-resizer](https://github.com/mdism/tool-exam-photo-resizer) | https://tools.shaikhismail.com/exam-photo-resizer/ |
| [tool-gst-emi-calculator](https://github.com/mdism/tool-gst-emi-calculator) | https://tools.shaikhismail.com/gst-emi-calculator/ |

## What is in here

```
public/                      Published to the root of tools.shaikhismail.com
├── index.html               Landing page (the list comes from assets/js/tools.js)
├── privacy.html             Privacy policy for all the tools
├── .htaccess                HTTPS, security headers, bot and scanner blocking for the whole subdomain
├── api/verify.php           Confirms Cloudflare Turnstile tokens for every tool
├── robots.txt, sitemap.xml, .well-known/security.txt
└── assets/                  Styles, font, theme toggle, tools list
config/turnstile.example.php Format of the private secret file (the real one is git-ignored)
scripts/bump_version.py      Release helper
.cpanel.yml                  Copies public/ to the subdomain root
```

## One-time setup on MilesWeb (cPanel)

1. **Subdomain:** cPanel → **Domains** → Create a new domain → `tools.shaikhismail.com`. Untick "Share document root", and set the document root to `tools.shaikhismail.com` (that is `/home/qyotupjl/tools.shaikhismail.com`).
2. **SSL:** cPanel → **SSL/TLS Status** → Run AutoSSL.
3. **Turnstile secret:** copy `config/turnstile.example.php` to `turnstile.php`, put the secret in it, and upload it with File Manager to `/home/qyotupjl/.config/shaikhismail-tools/turnstile.php` (create the folders; outside public_html). Set permissions to 600. Never commit it.
4. **Cloudflare:** in the Turnstile widget settings, add `tools.shaikhismail.com` as a hostname.
5. **Deploy this repo:** cPanel → **Git Version Control** → Create → Clone a Repository, URL `https://github.com/mdism/tools-hub.git`, path `repositories/tools-hub`, then Manage → Pull or Deploy → *Deploy HEAD Commit*.
6. **Deploy each tool repo** the same way. Each one's `.cpanel.yml` already points at its own folder.
7. On shaikhismail.com, point the tools page at the new addresses (see the TOOLS list in the mdism/mdism repo).

Needs PHP 8 with curl for `api/verify.php`; cPanel has both. Optional and free: put the domain behind Cloudflare (proxied DNS, Bot Fight Mode, Always Use HTTPS).

## Adding a new tool

1. Create a repo `tool-<what-it-does>` like the others, with `.cpanel.yml` deploying `public/` to `/home/qyotupjl/tools.shaikhismail.com/<what-it-does>/`.
2. Add one line to `public/assets/js/tools.js` here, and its address to `public/sitemap.xml`.
3. Deploy both.

## License

MIT, see [LICENSE](LICENSE).
