# One-off repair tool, 22 November 2026: carries the 18 November web cleanup (commit 6918215) back into LaTeX sources.
"""Replace each LaTeX paragraph changed on 18 Nov (commit 6918215) with the cleaned web paragraph,
converted back to LaTeX (marks, maths, footnotes, cross-references).
usage: port2.py <slug> <texfile> [--dry]"""
import sys, re, subprocess, difflib, html as H
slug, texf = sys.argv[1], sys.argv[2]; dry = '--dry' in sys.argv
def show(rev, path): return subprocess.run(['git','show',f'{rev}:{path}'],capture_output=True,text=True).stdout
oldh = show('6918215~1', f'src/library/{slug}.html'); newh = show('6918215', f'src/library/{slug}.html')
def fnmap(h):
    m = {}
    for li in re.finditer(r'<li id="fn(\d+)">(.*?)</li>', h, re.S):
        keys = re.findall(r'data-cites="([^"]+)"', li.group(2))
        m[li.group(1)] = ','.join(k for ks in keys for k in ks.split())
    return m
FN = fnmap(newh)
def blocks(h):
    body = h.split('<section id="footnotes"')[0]
    return [b for b in re.findall(r'<(?:p|li)>(.*?)</(?:p|li)>', body, re.S) if b.strip()]
def plain(s):
    s = re.sub(r'</?p>', ' ', s)
    s = re.sub(r'<span class="sr">[^<]*</span>', '', s); s = re.sub(r'<a href="#fn\d+"[^>]*>.*?</a>', '', s)
    s = re.sub(r'<[^>]+>', '', s); s = H.unescape(s)
    s = s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('—','-').replace('–','-')
    return re.sub(r'\s+', ' ', s).strip()
def plain_tex(s):
    s = re.sub(r'\\fn\{[^}]*\}|\\footnote(mark)?(\{[^}]*\})?|\\(label|ref|citep|citealp|cite)\{[^}]*\}', '', s)
    s = s.replace("``",'"').replace("''",'"').replace('---','-').replace('--','-').replace('~',' ')
    s = re.sub(r'\\(argm|hypm|openm|emph|textbf|textit|paragraph|item)\*?', '', s)
    s = re.sub(r'\\[a-zA-Z]+\s?', '', s); s = s.replace('{','').replace('}','').replace('$','')
    return re.sub(r'\s+', ' ', s).strip()
def to_tex(s):
    s = re.sub(r'</?p>', ' ', s)
    s = re.sub(r'<a href="#fn(\d+)"[^>]*>.*?</a>', lambda m: '\\fn{' + FN.get(m.group(1), '??') + '}', s)
    s = re.sub(r'<span class="citation" data-cites="([^"]+)">.*?</span>', lambda m: '\\citep{' + ','.join(m.group(1).split()) + '}', s)
    s = re.sub(r'<a href="#[^"]*" data-reference-type="ref" data-reference="([^"]+)">.*?</a>', r'\\ref{\1}', s)
    s = re.sub(r'<span class="math inline">\\\((.*?)\\\)</span>', lambda m: '$' + H.unescape(m.group(1)) + '$', s, flags=re.S)
    for cls, mac in (('arg','argm'),('hyp','hypm'),('opn','openm')):
        s = re.sub(r'<span class="m ' + cls + r'"[^>]*>(.*?)<span class="sr">[^<]*</span></span>', lambda m: '\\' + mac + '{' + m.group(1) + '}', s, flags=re.S)
    s = re.sub(r'<em>(.*?)</em>', r'\\emph{\1}', s); s = re.sub(r'<strong>(.*?)</strong>', r'\\textbf{\1}', s)
    s = re.sub(r'<span>(.*?)</span>', r'\1', s)
    if '<' in re.sub(r'\$[^$]*\$', '', s): return None
    s = H.unescape(s)
    s = s.replace('“','``').replace('”',"''").replace('’',"'").replace('‘','`').replace('—','---').replace('–','--').replace('%','\\%').replace(' ',' ')
    s = re.sub(r'Section “?\\ref', r'Section~\\ref', s)
    return re.sub(r'\s+', ' ', s).strip()
OB, NB = blocks(oldh), blocks(newh)
tex = open(texf, encoding='utf-8').read()
sm = difflib.SequenceMatcher(a=[plain(x) for x in OB], b=[plain(x) for x in NB], autojunk=False)
rep, fails = 0, []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'replace': 
        if tag != 'equal': fails.append((tag, plain(' '.join(OB[i1:i2]+NB[j1:j2]))[:150]))
        continue
    for k in range(max(i2-i1, j2-j1)):
        if i1+k >= i2 or j1+k >= j2: fails.append(('UNPAIRED', plain((OB+NB)[0])[:10])); continue
        o, n = OB[i1+k], NB[j1+k]
        po = plain(o); nt = to_tex(n)
        if nt is None: fails.append(('CONVERT', plain(n)[:150])); continue
        # find the tex span: a paragraph or \item whose plain text contains po
        cands = list(re.finditer(r'(?:^(?!\\item )|(?<=\\item ))(?P<b>(?!\\(?:begin|end|item)\b)(?:\\paragraph\{[^}]*\}\s*)?[A-Za-z`(\\$][^\n]*(?:\n(?!\s*\n|\\item |\\end\{|\\begin\{)[^\n]*)*)', tex, re.M))
        best, bm = 0, None
        for m in cands:
            body = re.sub(r'^\\paragraph\{[^}]*\}\s*', '', m.group('b'))
            r = difflib.SequenceMatcher(None, po, plain_tex(body), autojunk=False).ratio()
            if r > best: best, bm = r, m
        if best < 0.75: fails.append(('NOTEX %.2f' % best, po[:150])); continue
        body = bm.group('b'); head = re.match(r'^\\paragraph\{[^}]*\}\s*', body)
        newbody = (head.group(0) if head else '') + nt
        tex = tex[:bm.start('b')] + newbody + tex[bm.end('b'):]; rep += 1
if not dry: open(texf, 'w', encoding='utf-8').write(tex)
print('replaced', rep)
for f in fails: print(*f, sep='  ::  ')
