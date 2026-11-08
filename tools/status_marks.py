"""Claim-status marks for the web and plain-text editions.

LaTeX source uses \\argm{..}, \\hypm{..}, \\openm{..} for single claims, the environments
argbar / hypbar / openbar for whole passages, and \\statuskey for the printed key.
Before pandoc, these become placeholder tokens; after pandoc, the tokens become
underlined spans (HTML) or the status word in brackets (Markdown, for search and AI)."""
import re

KINDS = {"argm": ("A", "arg", "Argued", "Argued: a conclusion this framework argues in detail, which readers can check."),
         "hypm": ("H", "hyp", "Hypothesis", "Hypothesis: a proposal of GPT, not yet tested."),
         "openm": ("O", "opn", "Open", "Open: a question not yet answered; work still owed.")}
BARS = {"argbar": KINDS["argm"], "hypbar": KINDS["hypm"], "openbar": KINDS["openm"]}


def _balanced(t, i):
    """t[i] == '{'; return index just past the matching '}'."""
    d = 0
    for j in range(i, len(t)):
        if t[j] == "{": d += 1
        elif t[j] == "}":
            d -= 1
            if d == 0: return j + 1
    raise ValueError("unbalanced braces near: " + t[i:i + 80])


def to_tokens(tex):
    tex = tex.replace("\\statuskey", "").replace("\\hyptag", " (Hypothesis)")
    for env, (k, *_r) in BARS.items():
        tex = tex.replace(f"\\begin{{{env}}}", f"\n\n⟦BAR{k}⟧\n\n").replace(f"\\end{{{env}}}", f"\n\n⟦/BAR⟧\n\n")
    pat = re.compile(r"\\(argm|hypm|openm)\{")
    while True:
        m = pat.search(tex)
        if not m: break
        end = _balanced(tex, m.end() - 1)
        k = KINDS[m.group(1)][0]
        tex = tex[:m.start()] + f"⟦{k}⟧" + tex[m.end():end - 1] + f"⟦/{k}⟧" + tex[end:]
    return tex


def to_html(h):
    for k, cls, word, tip in KINDS.values():
        h = h.replace(f"⟦{k}⟧", f'<span class="m {cls}" tabindex="0" data-tip="{tip}">')
        h = h.replace(f"⟦/{k}⟧", f'<span class="sr"> [{word}]</span></span>')
        h = re.sub(rf"<p>\s*⟦BAR{k}⟧\s*</p>", f'<div class="bar {cls}" role="note"><p class="bar-tag">{word}</p>', h)
    h = re.sub(r"<p>\s*⟦/BAR⟧\s*</p>", "</div>", h)
    assert "⟦" not in h, "unconverted status token: " + h[h.index("⟦") - 60:h.index("⟦") + 60]
    return h


def to_md(md):
    for k, cls, word, tip in KINDS.values():
        md = md.replace(f"⟦{k}⟧", "").replace(f"⟦/{k}⟧", f" **\\[{word}\\]**")
        md = re.sub(rf"⟦BAR{k}⟧", f"**\\[{word}: the passage that follows\\]**", md)
    md = md.replace("⟦/BAR⟧", "**\\[End of passage\\]**")
    # a status word that lands before the sentence's full stop reads better after it
    md = re.sub(r" (\*\*\\\[(?:Argued|Hypothesis|Open)\\\]\*\*)([.,;:])", r"\2 \1", md)
    assert "⟦" not in md, "unconverted status token in markdown"
    return md


KEY_HTML = """<aside class="status-key" aria-label="How to read the marks">
<p class="step-label">How to read the marks</p>
<p>Claims about Graviton Pressure Theory are marked by how far they are established. Hover over or tap a marked passage to see its status.</p>
<ul>
<li><span class="k">Established</span> No mark. Accepted, measured physics.</li>
<li><span class="m arg">Argued</span> Solid underline. A conclusion this framework argues in detail, which readers can check.</li>
<li><span class="m hyp">Hypothesis</span> Dashed underline. A proposal of GPT, not yet tested.</li>
<li><span class="m opn">Open</span> Dotted underline and a small circle. A question not yet answered; work still owed.</li>
</ul>
<p class="muted">A whole passage with one status has a bar of the same style beside it. Changes since the first edition are listed at the end.</p>
</aside>
"""

KEY_MD = ("*How to read the marks.* Claims about Graviton Pressure Theory are marked by status. Established claims carry no mark. "
          "**\\[Argued\\]** marks a conclusion this framework argues in detail; **\\[Hypothesis\\]** a proposal of GPT, not yet tested; "
          "**\\[Open\\]** a question not yet answered. On the web page and in the PDF these appear as solid, dashed and dotted underlines.\n\n")


def has_marks(tex_tokens):
    return any(f"⟦{k}⟧" in tex_tokens or f"⟦BAR{k}⟧" in tex_tokens for k in "AHO")
