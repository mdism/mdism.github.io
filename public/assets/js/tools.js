/* =========================================================
   TOOLS LIST
   You never edit this to add a tool. The page asks GitHub for mdism's public repos tagged
   "shaikhismail-tool", then reads each one's /<repo>/tool.json (name, icon, description, order).
   The list below is only the fallback if GitHub can't be reached.
   ========================================================= */
window.TOOLS = [
  { name: "Image Compressor", icon: "Im", desc: "Shrink JPG, PNG and WebP files right in your browser. Nothing is uploaded.", url: "/image-compressor/", status: "live" },
  { name: "PDF Merge & Split", icon: "Pd", desc: "Combine PDFs into one, or pull out the pages you need.", url: "/pdf-merge-split/", status: "live" },
  { name: "Exam Photo Resizer", icon: "Ph", desc: "Resize photos and signatures to exact KB and pixel sizes for exam forms.", url: "/exam-photo-resizer/", status: "live" },
  { name: "GST, EMI & SIP Calculator", icon: "₹", desc: "Quick GST, EMI and SIP calculations with clear breakdowns.", url: "/gst-emi-calculator/", status: "live" },
];

(function () {
  const grid = document.getElementById('toolsGrid');
  if (!grid) return;

  const getJson = url => fetch(url, { credentials: 'omit' }).then(r => r.ok ? r.json() : Promise.reject(r.status));

  getJson('https://api.github.com/users/mdism/repos?per_page=100&type=owner')
    .then(repos => Promise.all(repos
      .filter(r => (r.topics || []).includes('shaikhismail-tool') && !r.archived && /^[a-z0-9-]+$/.test(r.name))
      .map(r => getJson(`/${r.name}/tool.json`)
        .then(t => ({ name: t.name, icon: t.icon, desc: t.desc, status: t.status === 'soon' ? 'soon' : 'live', order: Number(t.order) || 100, url: `/${r.name}/` }))
        .catch(() => null))))   // tagged but not published yet: skip it
    .then(list => list.filter(Boolean).sort((a, b) => a.order - b.order || a.name.localeCompare(b.name)))
    .then(list => render(list.length ? list : window.TOOLS))
    .catch(() => render(window.TOOLS));

  // Built with textContent only, so nothing in a tool.json can inject HTML.
  function render(list) {
    grid.textContent = '';
    list.forEach(t => {
      const live = t.status === 'live';
      const card = document.createElement(live ? 'a' : 'div');
      card.className = 'tool' + (live ? '' : ' soon');
      if (live) card.href = t.url;
      const ico = document.createElement('span'); ico.className = 'ico'; ico.setAttribute('aria-hidden', 'true'); ico.textContent = t.icon;
      const h = document.createElement('h2'); h.textContent = t.name;
      const p = document.createElement('p'); p.textContent = t.desc;
      const meta = document.createElement('div'); meta.className = 'meta';
      const where = document.createElement('span'); where.textContent = live ? t.url : 'Coming soon';
      const go = document.createElement('span'); go.className = 'go'; go.textContent = live ? 'Open →' : '';
      meta.append(where, go);
      card.append(ico, h, p, meta);
      grid.appendChild(card);
    });
  }
})();
