/* =========================================================
   TOOLS LIST
   Normally you never edit this: the page asks /api/tools.php, which finds every deployed
   tool folder that has a tool.json. This list is only the fallback if that request fails.
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

  fetch('/api/tools.php', { credentials: 'omit' })
    .then(r => r.ok ? r.json() : Promise.reject())
    .then(list => render(Array.isArray(list) && list.length ? list : window.TOOLS))
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
