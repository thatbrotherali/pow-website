"""Protect every bib title's capitalisation from BibTeX (plainnat lowercases all but the first word):
title = {X}  ->  title = {{X}}. Idempotent."""
import re, sys
def brace(s):
    out, i = [], 0
    for m in re.finditer(r'\btitle\s*=\s*\{', s):
        j = m.end(); depth = 1; k = j
        while depth:
            depth += {'{': 1, '}': -1}.get(s[k], 0); k += 1
        inner = s[j:k-1]
        # already protected if the whole inner text is one braced group
        d, whole = 0, inner.startswith('{')
        for n, ch in enumerate(inner):
            d += {'{': 1, '}': -1}.get(ch, 0)
            if d == 0 and n < len(inner) - 1: whole = False; break
        out.append(s[i:j]); out.append(inner if whole else '{' + inner + '}'); i = k - 1
    out.append(s[i:]); return ''.join(out)
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read(); t = brace(s)
    if t != s: open(p, 'w', encoding='utf-8').write(t); print('braced', p)
