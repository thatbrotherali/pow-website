// Turns the one-page librarian sheets (build/sheets/*.html, written by librarians.py) into PDFs in docs/assets/librarians/.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const src = path.join(__dirname, '..', 'build', 'sheets'), out = path.join(__dirname, '..', 'docs', 'assets', 'librarians');
  const b = await chromium.launch(); const p = await b.newPage();
  for (const f of fs.readdirSync(src).filter(f => f.endsWith('.html'))) {
    await p.goto('file://' + path.join(src, f)); await p.waitForTimeout(300);
    await p.pdf({ path: path.join(out, f.replace('.html', '.pdf')), format: 'A4', printBackground: true, preferCSSPageSize: true });
    console.log('wrote', f.replace('.html', '.pdf'));
  }
  await b.close();
})();
