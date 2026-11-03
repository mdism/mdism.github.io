"""Start a new free tool in one command.

    python scripts/new_tool.py word-counter "Word Counter" "Count words, characters and reading time." --icon Wc --what "texts" --what-one "text" \
        --input "Any text" --process "Counts words, characters and sentences" --output "Totals and reading time"

Creates ../word-counter/ next to this repo: a ready-to-deploy page with the privacy notice,
privacy policy, bot check, footer version, breadcrumb, input → process → output strip, FAQ, SEO tags,
shared styles and a GitHub Pages workflow. Pushed as the repo "word-counter", it is served at
https://tools.shaikhismail.com/word-counter/. The folder is a git repo on branch main with nothing committed yet.

It also refreshes this repo's built-in tool list and sitemap (scripts/update_index.py), so commit and push this repo too.
Add the topic shaikhismail-tool on GitHub and the live landing page lists the tool by itself.
"""
import argparse, datetime, html, pathlib, re, shutil, subprocess, sys

HUB = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = HUB / 'template'

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('slug', help='folder name and URL path, e.g. word-counter (lowercase letters, numbers, dashes)')
ap.add_argument('name', help='display name, e.g. "Word Counter"')
ap.add_argument('desc', help='one sentence shown on the landing page and in search results')
ap.add_argument('--icon', default=None, help='1-3 characters for the card icon (default: first two letters)')
ap.add_argument('--what', default='files', help='what the user gives the tool, plural, for the privacy text (default: files)')
ap.add_argument('--what-one', default=None, help='the same word, singular, for the FAQ (default: --what without the final s)')
ap.add_argument('--input', default='Your file', help='the Input box of the input → process → output strip')
ap.add_argument('--process', default='Processed in your browser', help='the Process box')
ap.add_argument('--output', default='The result, ready to download', help='the Output box')
a = ap.parse_args()

if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', a.slug):
    sys.exit('slug must be lowercase letters, numbers and dashes, like word-counter')
dest = HUB.parent / a.slug
if dest.exists():
    sys.exit(f'{dest} already exists')

values = {
    '{{SLUG}}': a.slug, '{{NAME}}': a.name, '{{DESC}}': a.desc, '{{WHAT}}': a.what,
    '{{WHAT_ONE}}': a.what_one or re.sub(r's$', '', a.what),
    '{{INPUT}}': a.input, '{{PROCESS}}': a.process, '{{OUTPUT}}': a.output,
    '{{ICON}}': a.icon or a.name[:2].title(), '{{DATE}}': str(datetime.date.today()),
    '{{DETAIL}}': f'Your {a.what} are read and processed by JavaScript in your browser, and the result is offered to you directly. Nothing is sent to a server.',
}
shutil.copytree(TEMPLATE, dest)
for f in dest.rglob('*'):
    if f.is_file():
        text = f.read_text(encoding='utf-8')
        for k, v in values.items():
            # HTML-escape for pages; values in the JSON-LD block stay readable because & < > are rare in names
            text = text.replace(k, html.escape(v, quote=True) if f.suffix == '.html' else v)
        f.write_text(text, encoding='utf-8')

# Shared look and behaviour come from this repo, so every tool stays consistent.
assets = dest / 'public/assets'
(assets / 'css').mkdir(parents=True, exist_ok=True)
shutil.copy(HUB / 'public/assets/css/tool.css', assets / 'css/tool.css')
shutil.copy(HUB / 'public/assets/js/common.js', assets / 'js/common.js')
shutil.copytree(HUB / 'public/assets/fonts', assets / 'fonts')

git = ['git', '-C', str(dest)]
subprocess.run(git + ['init', '-q', '-b', 'main'], check=True)
subprocess.run([sys.executable, str(HUB / 'scripts/update_index.py')], check=True)

print(f'''Created {dest}

Next:
  1. Build the tool in public/index.html and public/assets/js/app.js (open index.html in a browser to try it).
     Edit the FAQ answers and the title in public/index.html if you like.
  2. Create an empty public GitHub repo named {a.slug}, then:
       git -C "{dest}" add -A
       git -C "{dest}" commit -m "Start {a.name}"
       git -C "{dest}" remote add origin https://github.com/mdism/{a.slug}.git
       git -C "{dest}" push -u origin main
  3. On GitHub: Settings → Pages → Source: GitHub Actions, and add the topic shaikhismail-tool.
  4. Commit and push mdism.github.io too, so the sitemap and built-in list include the new tool.
It appears at https://tools.shaikhismail.com/{a.slug}/ and on the landing page by itself.''')
