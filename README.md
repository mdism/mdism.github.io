# mdism.github.io

The landing page for **https://tools.shaikhismail.com**, the free browser tools by [Mohammed Ismail Shaikh](https://shaikhismail.com), hosted on GitHub Pages.

This is your GitHub *user site*. Because it has the custom domain tools.shaikhismail.com, every other repo of yours with Pages
turned on is published under it automatically, at `/<repo-name>/`:

| Repo | Address |
|---|---|
| mdism.github.io (this repo) | https://tools.shaikhismail.com/ |
| [image-compressor](https://github.com/mdism/image-compressor) | https://tools.shaikhismail.com/image-compressor/ |
| [pdf-merge-split](https://github.com/mdism/pdf-merge-split) | https://tools.shaikhismail.com/pdf-merge-split/ |
| [exam-photo-resizer](https://github.com/mdism/exam-photo-resizer) | https://tools.shaikhismail.com/exam-photo-resizer/ |
| [gst-emi-calculator](https://github.com/mdism/gst-emi-calculator) | https://tools.shaikhismail.com/gst-emi-calculator/ |

## What is in here

```
public/                        Published to https://tools.shaikhismail.com/
├── index.html                 Landing page (finds tools by GitHub topic)
├── privacy.html               Privacy policy for all the tools
├── 404.html                   Not-found page for the whole subdomain
├── CNAME                      tools.shaikhismail.com
├── api/config.json            Address of the bot-check Worker (used by every tool)
├── robots.txt, sitemap.xml, .well-known/security.txt
└── assets/                    Styles, font, theme toggle, tools list
worker/turnstile-verify.js     Cloudflare Worker that confirms Turnstile tokens (not published)
scripts/new_tool.py            Starts a new tool repo with everything wired in
template/                      What new_tool.py copies
.github/workflows/pages.yml    Publishes public/ on every push
```

## One-time setup

**1. Create the repo.** On GitHub, create a public repo named exactly `mdism.github.io` and push this folder to it.

**2. Turn on Pages.** Repo → Settings → Pages → Source: **GitHub Actions**. The workflow publishes on the next push (or run it from the Actions tab).

**3. Add the domain on MilesWeb.** cPanel → **Zone Editor** → shaikhismail.com → Add Record:
- Type `CNAME`, Name `tools`, Record `mdism.github.io`

Then on GitHub: Settings → Pages → Custom domain → `tools.shaikhismail.com` → Save. Wait for the DNS check to pass (minutes to a few hours), then tick **Enforce HTTPS**.
Recommended: GitHub → your profile Settings → Pages → **Add a domain** to verify `shaikhismail.com`, so nobody else can claim your subdomains.

**4. Bot-check Worker (free).** Cloudflare dashboard → Workers & Pages → Create → Worker → name it `tools-verify` → Deploy → Edit code → paste `worker/turnstile-verify.js` → Deploy.
Then Settings → Variables and Secrets → Add → type **Secret**, name `TURNSTILE_SECRET`, value = your Turnstile secret key.
Copy the Worker's address (like `https://tools-verify.<your-name>.workers.dev`) into `public/api/config.json`, commit and push.

**5. Turnstile hostname.** Cloudflare → Turnstile → your widget → Hostnames: make sure `tools.shaikhismail.com` is listed.

**6. Each tool repo:** push it, set Settings → Pages → Source: **GitHub Actions**, and add the topic `shaikhismail-tool`. It appears at `/<repo-name>/` and on the landing page.

## Adding a new tool

```
python scripts/new_tool.py word-counter "Word Counter" "Count words, characters and reading time." --what "text"
```

This creates `../word-counter/`, ready to build. Push it as a repo named `word-counter`, turn on Pages (GitHub Actions), add the topic `shaikhismail-tool`. Done: it shows up on the landing page by itself.

## License

MIT, see [LICENSE](LICENSE).
