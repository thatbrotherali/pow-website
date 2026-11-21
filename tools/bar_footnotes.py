"""Move \\fn{...} footnotes out of margin-bar boxes (mdframed letters them a, b, ...):
inside the box \\footnotemark, after it the matching \\footnotetext, so numbering runs on."""
import re, sys
BOX = re.compile(r'(\\begin\{(argbar|hypbar|openbar)\})(.*?)(\\end\{\2\})', re.S)
def fix(s):
    def one(m):
        keys = re.findall(r'\\fn\{([^}]*)\}', m.group(3))
        if not keys: return m.group(0)
        body = re.sub(r'\\fn\{[^}]*\}', r'\\footnotemark{}', m.group(3))
        n = len(keys)
        texts = f"\\addtocounter{{footnote}}{{-{n-1}}}" if n > 1 else ""
        for i, k in enumerate(keys):
            texts += ("\\stepcounter{footnote}" if i else "") + f"\\footnotetext{{\\citealp{{{k}}}.}}"
        return m.group(1) + body + m.group(4) + "\n" + texts
    return BOX.sub(one, s)
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read(); t = fix(s)
    if t != s: open(p, 'w', encoding='utf-8').write(t); print('moved footnotes out of boxes in', p)
