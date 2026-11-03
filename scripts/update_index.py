"""Refresh the landing page's built-in tool list from the tool folders next to this repo.

    python scripts/update_index.py

Reads ../<tool>/public/tool.json for every tool folder beside mdism.github.io and rewrites:
  - the tool cards inside public/index.html (so search engines see them without JavaScript),
  - the tool list in the page's structured data (JSON-LD),
  - the fallback list in public/assets/js/tools.js,
  - public/sitemap.xml.
The live page still finds tools on GitHub by the shaikhismail-tool topic; this only keeps the
built-in copy and the sitemap current. Run it after adding a tool, then commit and push this repo.
"""
import html, json, pathlib, re

HUB = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://tools.shaikhismail.com'
esc = lambda s: html.escape(s, quote=True)

tools = []
for meta in sorted(HUB.parent.glob('*/public/tool.json')):
    slug = meta.parent.parent.name
    if slug == HUB.name or not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', slug):
        continue
    t = json.loads(meta.read_text(encoding='utf-8'))
    if t.get('status', 'live') == 'live':
        tools.append(dict(slug=slug, **t))
tools.sort(key=lambda t: (t.get('order', 100), t['name']))
if not tools:
    raise SystemExit(f'No tool folders with public/tool.json found next to {HUB}')

page = HUB / 'public/index.html'
s = page.read_text(encoding='utf-8')
cards = '\n'.join(
    f'      <a class="tool" href="/{t["slug"]}/"><span class="ico" aria-hidden="true">{esc(t["icon"])}</span>'
    f'<h2>{esc(t["name"])}</h2><p>{esc(t["desc"])}</p><div class="meta"><span>/{t["slug"]}/</span><span class="go">Open →</span></div></a>'
    for t in tools)
s = re.sub(r'<!-- cards -->.*?<!-- /cards -->', lambda m: f'<!-- cards -->\n{cards}\n<!-- /cards -->', s, flags=re.S)


def fix_ld(m):
    data = json.loads(m.group(1).replace('<\\/', '</'))
    for node in data.get('@graph', []):
        if node.get('@type') == 'CollectionPage':
            node['mainEntity'] = {'@type': 'ItemList', 'itemListElement': [
                {'@type': 'ListItem', 'position': i + 1, 'name': t['name'], 'url': f'{BASE}/{t["slug"]}/'} for i, t in enumerate(tools)]}
    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return f'<script type="application/ld+json">{out}</script>'


s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_ld, s, count=1, flags=re.S)
page.write_text(s, encoding='utf-8')

js = HUB / 'public/assets/js/tools.js'
rows = '\n'.join(f'  {{ name: {json.dumps(t["name"], ensure_ascii=False)}, icon: {json.dumps(t["icon"], ensure_ascii=False)}, '
                 f'desc: {json.dumps(t["desc"], ensure_ascii=False)}, url: "/{t["slug"]}/", status: "live" }},' for t in tools)
js.write_text(re.sub(r'window\.TOOLS = \[\n.*?\n\];', lambda m: f'window.TOOLS = [\n{rows}\n];', js.read_text(encoding='utf-8'), flags=re.S), encoding='utf-8')

urls = [f'{BASE}/'] + [f'{BASE}/{t["slug"]}/' for t in tools] + [f'{BASE}/privacy.html']
(HUB / 'public/sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n', encoding='utf-8')

print(f'Landing page list and sitemap now have {len(tools)} tools: ' + ', '.join(t['slug'] for t in tools))
