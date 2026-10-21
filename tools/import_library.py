"""One-off importer: turns Shareef's original documents (LaTeX, OpenDocument, PDF) into clean
HTML fragments and Markdown files in src/library/, ready for build.py to publish.

Run it again only when an original document changes:
    python tools/import_library.py <folder holding the originals>
It needs pandoc and pdftotext (poppler). build.py itself needs neither.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "library"
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/mnt/user-data/uploads")
GPT = SRC / "Graviton Pressure Theory"
TEX = GPT / "Tex files"
WEB = GPT / "Web site for AI gravity"
POW = SRC / "People of the world - Ministry and Services" / "Mega-Success"
PORTAL = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("/home/claude/thatbrotherali/ai-portal")


def pandoc(text_or_path, src_fmt, dst_fmt, extra=(), is_path=False):
    args = ["pandoc", "-f", src_fmt, "-t", dst_fmt, "--wrap=none", *extra]
    if is_path:
        return subprocess.run(args + [str(text_or_path)], capture_output=True, text=True, check=True).stdout
    r = subprocess.run(args, input=text_or_path, capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr[:600])
    return r.stdout


def braced(s, i):
    """Return (content, end) for the {...} group starting at s[i] == '{'."""
    depth, j = 0, i
    while j < len(s):
        if s[j] == "{": depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0: return s[i + 1:j], j + 1
        j += 1
    raise ValueError("unbalanced braces")


def strip_tex(s):
    s = re.sub(r"\\footnote\{.*", "", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", "", s)
    return re.sub(r"\s+", " ", s.replace("{", "").replace("}", "")).strip()


def tidy_html(h):
    h = re.sub(r"<h([1-6])([^>]*)>", lambda m: f"<h{min(6, int(m.group(1)) + 1)}{m.group(2)}>", h)  # page owns the h1
    h = re.sub(r"</h([1-6])>", lambda m: f"</h{min(6, int(m.group(1)) + 1)}>", h)
    h = re.sub(r"<p>\s*</p>", "", h)
    return h.strip()


def first_para(h):
    for m in re.finditer(r"<p>(.*?)</p>", h, re.S):
        inner = re.sub(r'<a[^>]*class="footnote-ref"[^>]*>.*?</a>|<sup>.*?</sup>', "", m.group(1), flags=re.S)
        t = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()
        if len(t.split()) >= 20:
            return re.sub(r"\s+", " ", t)
    return ""


def save(slug, title, subtitle, frag_html, md, source):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{slug}.html").write_text(frag_html, encoding="utf-8")
    md_head = f"# {title}\n\n" + (f"*{subtitle}*\n\n" if subtitle else "") + "By Shareef Ali Rashada\n\n"
    (OUT / f"{slug}.md").write_text(md_head + md.strip() + "\n", encoding="utf-8")
    words = len(re.sub(r"<[^>]+>", " ", frag_html).split())
    return {"slug": slug, "title": title, "subtitle": subtitle, "words": words, "lead": first_para(frag_html), "source": source}


# ---------- LaTeX: the 30 parts of the Unified Framework ----------
def tex_doc(path, slug):
    t = path.read_text(encoding="utf-8", errors="replace")
    title = subtitle = ""
    k = t.find("\\partwithsubtitle")
    if k >= 0:
        a, e1 = braced(t, t.index("{", k))
        b, e2 = braced(t, e1)
        title, subtitle = strip_tex(a), strip_tex(b)
        t = t[:k] + t[e2:]
    else:
        m = re.search(r"\\section\*?\{([^}]*)\}", t)
        title = strip_tex(m.group(1)); t = t[:m.start()] + t[m.end():]
    for cmd in ("\\setcounter", "\\renewcommand"):
        while (k := t.find(cmd)) >= 0:
            _, e1 = braced(t, t.index("{", k)); _, e2 = braced(t, e1); t = t[:k] + t[e2:]
    t = t.replace("\\newpage", "").replace("\\textemdash", "—").replace("∼", "~")
    t = re.sub(r"\\texorpdfstring\{([^}]*)\}\{[^}]*\}", r"\1", t)
    bib = ["--citeproc", "--bibliography", str(TEX / "GPT Framework Master.bib")]
    h = pandoc(t, "latex", "html5", ["--mathjax", *bib])
    md = pandoc(t, "latex", "gfm", bib)
    return save(slug, title, subtitle, tidy_html(h), md, path.name)


# ---------- OpenDocument ----------
def odt_doc(path, slug, title=None, subtitle=None, drop_lines=0):
    h = pandoc(path, "odt", "html5", ["--mathjax"], is_path=True)
    # the opening lines of these documents repeat the title and subtitle; drop them
    for _ in range(drop_lines):
        h = re.sub(r"^\s*<(p|h\d)[^>]*>.*?</\1>", "", h, count=1, flags=re.S)
    h = re.sub(r"<img[^>]*>", "", h)
    md = pandoc(h, "html", "gfm")
    return save(slug, title, subtitle, tidy_html(h), md, path.name)


# ---------- PDFs made by LaTeX or LibreOffice: rebuild headings and paragraphs ----------
def pdf_blocks(path, running=(), first_page=1, toc=None):
    raw = subprocess.run(["pdftotext", "-f", str(first_page), str(path), "-"], capture_output=True, text=True, check=True).stdout
    lines = [l.rstrip() for l in raw.replace("\f", "\n").split("\n")]
    heads = toc or {}
    blocks, buf, i = [], [], 0

    def flush():
        if buf:
            txt = " ".join(buf)
            txt = re.sub(r"(\w)- (\w)", lambda m: m.group(1) + m.group(2) if m.group(2).islower() else m.group(0), txt)
            blocks.append(("li" if txt.startswith("•") else "p", txt.lstrip("• ").strip()))
            buf.clear()

    width = max((len(l) for l in lines if l), default=100)
    while i < len(lines):
        l = lines[i].strip()
        if re.fullmatch(r"\d{1,2}", l) and not buf:
            nz = [j for j in range(i + 1, min(i + 8, len(lines))) if lines[j].strip()][:3]
            if any((l + " " + " ".join(lines[j].strip() for j in nz[:n])) in heads for n in range(1, len(nz) + 1)):
                pass  # a chapter number, handled below
            else:
                i += 1; continue
        elif not l or l in running or re.fullmatch(r"\d{1,3}", l) or l.startswith("📖"):
            if not l and buf and buf[-1].endswith((".", "?", "!", ":", "”", '"')): flush()
            i += 1; continue
        # numbered heading split over lines: "1.3" then "Title" (the title itself may wrap)
        if re.fullmatch(r"\d+(\.\d+)*", l):
            nz = [j for j in range(i + 1, min(i + 8, len(lines))) if lines[j].strip()][:3]
            hit = None
            for n in range(1, len(nz) + 1):
                cand = l + " " + " ".join(lines[j].strip() for j in nz[:n])
                if cand in heads: hit = (cand, nz[n - 1])
            if hit:
                flush(); blocks.append((heads[hit[0]], hit[0])); i = hit[1] + 1; continue
        # unnumbered heading wrapped over two lines
        if buf == [] and i + 1 < len(lines) and f"{l} {lines[i + 1].strip()}" in heads:
            flush(); blocks.append((heads[f"{l} {lines[i + 1].strip()}"], f"{l} {lines[i + 1].strip()}")); i += 2; continue
        if l in heads:
            flush(); blocks.append((heads[l], l)); i += 1; continue
        if l.startswith("•"): flush()
        buf.append(l)
        if len(l) < width * 0.72 and l.endswith((".", "?", "!", "”", '"', ":")): flush()
        i += 1
    flush()
    return blocks


def blocks_html(blocks):
    out, in_list = [], False
    for kind, txt in blocks:
        t = html.escape(txt, quote=False)
        if kind == "li":
            if not in_list: out.append("<ul>"); in_list = True
            out.append(f"<li>{t}</li>"); continue
        if in_list: out.append("</ul>"); in_list = False
        out.append(f"<{kind}>{t}</{kind}>")
    if in_list: out.append("</ul>")
    return "\n".join(out)


def latex_pdf_toc(path, pages):
    """Read the contents pages of a LaTeX PDF: '1 Title' -> h2, '1.2 Title' -> h3, '1.2.3 Title' -> h4."""
    raw = subprocess.run(["pdftotext", "-f", "1", "-l", str(pages), str(path), "-"], capture_output=True, text=True).stdout
    toc = {}
    for l in raw.split("\n"):
        m = re.match(r"^(\d+(?:\.\d+)*)\s+(.+?)(?:\s*\.(?:\s*\.)+\s*\d*)?$", l.strip())
        if m and not re.fullmatch(r"[\d\s.]+", m.group(2)):
            toc[f"{m.group(1)} {m.group(2).strip()}"] = f"h{min(4, m.group(1).count('.') + 2)}"
    return toc


def plan_to_end_poverty():
    path = POW / "Plan_to_end_poverty.pdf"
    toc = latex_pdf_toc(path, 9)
    toc["Introduction – People of the World: Ending Poverty by 2050"] = "h2"
    raw = subprocess.run(["pdftotext", "-f", "1", "-l", "9", str(path), "-"], capture_output=True, text=True).stdout
    for m in re.finditer(r"^(Appendix [A-Z]: .+?)\s*(?:\.\s*)+\d+$", raw, re.M):
        toc[m.group(1).strip()] = "appx"
    blocks = pdf_blocks(path, running=("Plan to End Poverty",), first_page=10, toc=toc)
    # split into chapters at each h2 so each gets its own page
    chapters, cur = [], None
    for b in blocks:
        if b[0] == "appx":
            if not cur or cur["num"] != "10":
                cur = {"title": "Appendices", "num": "10", "blocks": []}; chapters.append(cur)
            cur["blocks"].append(("h2", b[1])); continue
        if b[0] == "h2":
            cur = {"title": re.sub(r"^\d+\s+", "", b[1]), "num": (re.match(r"^(\d+)\s", b[1]) or [None, "0"])[1], "blocks": []}
            chapters.append(cur); continue
        if cur is None:
            cur = {"title": "Introduction – People of the World: Ending Poverty by 2050", "num": "0", "blocks": []}; chapters.append(cur)
        cur["blocks"].append(b)
    out = []
    for ch in chapters:
        if not ch["blocks"]: continue
        h = blocks_html([(k if k != "h2" else "h3", t) for k, t in ch["blocks"]])
        slug = f"plan-chapter-{int(ch['num']):02d}"
        out.append(save(slug, ch["title"], "The Plan to End Poverty", h, pandoc(h, "html", "gfm"), path.name) | {"chapter": int(ch["num"])})
    return out


def new_morality():
    path = POW / "The New Morality-  Humanity’s True Path Amid the Collapse of Celestial Governance.pdf"
    raw = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True).stdout
    # LibreOffice PDF: headings are short title-case lines on their own
    heads = {}
    for l in raw.split("\n"):
        s = l.strip()
        if 2 <= len(s.split()) <= 10 and not s.endswith((".", ",", ";", ":")) and s[:1].isupper() and sum(w[:1].isupper() for w in s.split()) >= len(s.split()) * 0.6 and not s.startswith("•"):
            heads[s] = "h2"
    heads.pop("Salvation and The New Morality: Humanity’s True Path Amid the Collapse of Celestial", None)
    blocks = pdf_blocks(path, toc=heads)
    blocks = [b for b in blocks if not b[1].startswith(("Salvation and The New Morality: Humanity’s True Path", "Governance"))][0:]
    h = blocks_html(blocks)
    return save("new-morality", "Salvation and the New Morality", "Humanity’s True Path Amid the Collapse of Celestial Governance", h, pandoc(h, "html", "gfm"), path.name)


def respace(page, late=False):
    """Old gateway text keeps a trace of line layout: words on a paragraph's first line are two spaces
    apart, wrapped lines three. A switch from three back to two marks a new paragraph."""
    parts = re.split(r"( {2,})", page)
    words, seps = parts[0::2], [len(x) for x in parts[1::2]]
    out, prev = [words[0]], None
    for k, w in enumerate(words[1:]):
        sep = seps[k]
        nxt = seps[k + 1] if k + 1 < len(seps) else 2
        brk = (prev is not None and prev >= 3 and sep == 2) if not late else (k >= 1 and seps[k - 1] >= 3 and prev == 2 and sep == 2 and (k < 2 or seps[k - 2] >= 3))
        if brk or w.startswith(("●", "•")):
            out.append("\n\n" + w.lstrip("●• ") if w.startswith(("●", "•")) else "\n\n" + w)
        else:
            out.append(" " + w)
        prev = sep
    return re.sub(r"[ \t]+", " ", "".join(out)).strip()


# ---------- documents that only survive as the old gateway's page-per-paragraph HTML ----------
def portal_doc(fname, slug, title, subtitle=""):
    s = (PORTAL / "documents" / fname).read_text(encoding="utf-8", errors="replace")
    pages = [html.unescape(re.sub(r"<[^>]+>", "", p)).strip() for p in re.findall(r"<p>(.*?)</p>", s, re.S)]
    if sum(p.count("   ") for p in pages) > 200:
        score = lambda ps: sum(bool(re.match(r"[a-z]", q)) for p in ps for q in p.split("\n\n"))
        a, b = [respace(p) for p in pages], [respace(p, True) for p in pages]
        pages = a if score(a) <= score(b) else b
    text = "\n\n".join(p for p in pages if p)
    # contents entries like "4.6.3 The Curve-Fitting Problem . . . 12" give us the headings
    heads = []
    for m in re.finditer(r"(\d+(?:\.\d+)+)\s+([A-Z][^.]{3,90}?)\s*(?:\.\s){3,}\.?\s*\d+", text):
        heads.append((m.group(1), m.group(2).strip()))
    body = text
    toc_end = 0
    for num, ttl in heads:
        k = body.find(f"{num} {ttl}", toc_end)
        if k >= 0: toc_end = max(toc_end, k + len(num) + len(ttl))
    out = []
    pos = 0
    marks = []
    for num, ttl in heads:
        k = body.find(f"{num} {ttl}", toc_end)
        if k > 0: marks.append((k, num, ttl))
    marks.sort()
    paras = lambda chunk: "".join(f"<p>{html.escape(p.strip(), quote=False)}</p>\n" for p in re.split(r"\n\n+", chunk) if len(p.strip()) > 1)
    start = body.find("\n\n", toc_end) if marks else 0
    if marks:
        out.append(paras(body[:body.rfind("Contents", 0, toc_end) if "Contents" in body[:toc_end] else 0]))
        pos = marks[0][0]
        for idx, (k, num, ttl) in enumerate(marks):
            end = marks[idx + 1][0] if idx + 1 < len(marks) else len(body)
            lvl = min(4, num.count(".") + 2)
            out.append(f"<h{lvl}>{html.escape(num + ' ' + ttl)}</h{lvl}>\n" + paras(body[k + len(num) + len(ttl) + 1:end]))
    else:
        out.append(paras(body))
    h = "".join(out)
    return save(slug, title, subtitle, h, pandoc(h, "html", "gfm"), fname + " (from the earlier gateway)")



UPD = SRC / "Library updates"


def toc_pages(path):
    """Pages (1-indexed) that are contents pages: many dotted leader lines."""
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True).stdout).group(1))
    out = []
    for p in range(1, min(n, 15) + 1):
        t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), str(path), "-"], capture_output=True, text=True).stdout
        if t.count(". . .") >= 5:
            out.append(p)
    return out


def latex_pdf_doc(path, slug, title, subtitle, running=()):
    tp = toc_pages(path)
    toc = latex_pdf_toc(path, max(tp))
    first = subprocess.run(["pdftotext", "-f", "1", "-l", "1", str(path), "-"], capture_output=True, text=True).stdout
    m = re.search(r"Abstract\s*\n(.*?)(?:\n\s*Contents|\Z)", first, re.S)
    abstract = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    abstract = re.sub(r"(\w)- (\w)", lambda k: k.group(1) + k.group(2) if k.group(2).islower() else k.group(0), abstract)
    blocks = pdf_blocks(path, running=running, first_page=max(tp) + 1, toc=toc)
    blocks = [(k, re.sub(r"\s{2,}", " ", re.sub(r"[⎪⎧⎨⎩⎫⎬⎭⎛⎜⎝⎞⎟⎠]", " ", t)).strip()) for k, t in blocks]
    h = (f"<h2>Abstract</h2>\n<p>{html.escape(abstract, quote=False)}</p>\n" if abstract else "") + blocks_html([b for b in blocks if b[1]])
    import shutil
    shutil.copy(path, OUT / f"{slug}.pdf")
    return save(slug, title, subtitle, h, pandoc(h, "html", "gfm"), path.name) | {"pdf": True}


def gdocs_pdf_doc(path, slug, title, subtitle):
    """Google Docs PDF with 'Part One: ...' and '1.1 ...' headings, preceded by an outline."""
    raw = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True).stdout
    heads = {}
    for l in raw.split("\n"):
        s = l.replace("\u200b", "").replace("●", "").strip()
        if re.match(r"^Part [A-Z][a-z]+: ", s): heads[s] = "h2"
        elif re.match(r"^\d+\.\d+ [A-Z]", s) and len(s) < 90 and not s.endswith("."): heads[s] = "h3"
    blocks = pdf_blocks(path, toc=heads)
    # drop the title lines and the outline: start at the second "Part One" heading
    starts = [i for i, b in enumerate(blocks) if b[0] == "h2" and b[1].startswith("Part One")]
    blocks = blocks[starts[-1]:] if starts else blocks
    h = blocks_html([(k, t.replace("\u200b", "")) for k, t in blocks])
    import shutil
    shutil.copy(path, OUT / f"{slug}.pdf")
    return save(slug, title, subtitle, h, pandoc(h, "html", "gfm"), path.name) | {"pdf": True}



TEXSRC = SRC / "latex-sources" / "v2"


def tex_main_doc(folder, slug, title, subtitle, bib=None, pdf=None):
    """A whole LaTeX paper (main.tex, with any \\input parts). The abstract becomes the opening section."""
    main = (folder / "main.tex").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", main, re.S)
    abstract = m.group(1).strip() if m else ""
    body = main[main.index("\\begin{document}") + len("\\begin{document}"):main.index("\\end{document}")]
    body = re.sub(r"\\begin\{abstract\}.*?\\end\{abstract\}|\\maketitle|\\tableofcontents|\\newpage|\\bibliographystyle\{[^}]*\}|\\bibliography\{[^}]*\}", "", body, flags=re.S)

    def inline_inputs(t):
        return re.sub(r"\\input\{([^}]+)\}", lambda k: inline_inputs((folder / (k.group(1) if k.group(1).endswith(".tex") else k.group(1) + ".tex")).read_text(encoding="utf-8", errors="replace")), t)
    body = inline_inputs(body).replace("\\part*{", "\\section*{")
    preamble = main[:main.index("\\begin{document}")]
    macros = "\n".join(l for l in preamble.split("\n") if l.strip().startswith(("\\newcommand", "\\DeclareMathOperator", "\\def")))
    doc = macros + "\n\\begin{document}\n" + (f"\\section*{{Abstract}}\n{abstract}\n" if abstract else "") + body + "\n\\end{document}\n"
    extra = ["--citeproc", "--bibliography", str(folder / bib)] if bib else []
    h = pandoc(doc, "latex", "html5", ["--mathjax", *extra])
    md = pandoc(doc, "latex", "gfm", extra)
    if pdf:
        import shutil
        shutil.copy(pdf, OUT / f"{slug}.pdf")
    return save(slug, title, subtitle, tidy_html(h), md, "LaTeX source") | {"pdf": bool(pdf)}


if __name__ == "__main__":
    cat = {"framework": [], "pathway": [], "papers": [], "plan": [], "other": []}
    parts = sorted(TEX.glob("Part *.tex"))
    for p in parts:
        if "What GPT Corrects" in p.name: continue
        n = int(re.match(r"Part (\d+)", p.name).group(1))
        cat["framework"].append(tex_doc(p, f"gpt-part-{n:02d}") | {"part": n})
        print("part", n)
    cat["papers"].append(tex_doc(TEX / "Transitional Mechanics.tex", "transitional-mechanics"))
    cat["papers"].append(tex_doc(TEX / "Part 30 - What GPT Corrects.tex", "what-gpt-corrects"))
    cat["pathway"] += [
        odt_doc(WEB / "Start Here.odt", "start-here", "Start Here: Graviton Pressure Theory", "A constraint-first pathway for humans and AI systems", drop_lines=3),
        odt_doc(WEB / "A Foundational Constraint Set for Any Complete Theory of Gravity.odt", "constraint-set", "The Gravity Constraint Set", "A foundational constraint set for any complete theory of gravity", drop_lines=2),
        odt_doc(WEB / "The GR Silence Map.odt", "gr-silence-map", "The GR Silence Map", "A strict comparative audit against the Constraint Set", drop_lines=3),
        odt_doc(WEB / "A constraints-first explanation for educated readers.odt", "not-alternative-gravity", "Why Graviton Pressure Theory Is Not “Alternative Gravity”", "A constraints-first explanation for educated readers", drop_lines=2),
        odt_doc(WEB / "Audit Questions for Theoretical Completeness.odt", "audit-questions", "Audit Questions for Theoretical Completeness", "Questions any complete theory of gravity should be able to answer", drop_lines=2),
    ]
    cat["papers"] += [
        portal_doc("from_gr_to_gpt.html", "from-gr-to-gpt", "From General Relativity to Graviton Pressure Theory", "Finishing Einstein’s Work"),
        odt_doc(WEB / "Charge as Gravitational flow bias.odt", "structure-before-uncertainty", "Structure Before Uncertainty", "Recovering mechanism in a universe that still works", drop_lines=2),
        tex_main_doc(TEXSRC / "a85eee92-The_Reduction_Conflation", "reduction-conflation", "The Reduction Conflation", "Numerical equivalence is not ontological compatibility", bib="references.bib", pdf=UPD / "The_Reduction_Conflation.pdf"),
        tex_main_doc(SRC / "latex-sources" / "constraints-revised", "operational-constraints-of-the-ep", "The Operational Constraints of the Equivalence Principle", "A mechanical analysis of the expansion paradox and vacuum pressure", pdf=SRC / "latex-sources" / "constraints-revised" / "main.pdf"),
        gdocs_pdf_doc(UPD / "The_Logical_Closure_of_the_EP.pdf", "logical-closure-of-the-ep", "The Logical Closure of the Equivalence Principle", "What we accepted when we accepted the Equivalence Principle on General Relativity's terms, and a proposal for true closure through causal mechanism"),
        portal_doc("The_Paradox_of_the_boulder.html", "paradox-of-the-boulder", "The Paradox of the Boulder", "A dual audit of force and geometry language"),
        portal_doc("Causal_audit_of_motion.html", "causal-audit-of-motion", "A Causal Audit of Motion"),
        tex_main_doc(TEXSRC / "b866d458-The_Mechanics_of_the_Medium", "mechanics-of-the-medium", "The Mechanics of the Medium", "The origin of primitives", pdf=UPD / "The_Mechanics_of_the_Medium.pdf"),
    ]
    cat["other"] += [
        odt_doc(GPT / "proof of reality of God.odt", "cosmic-mind", "An Intelligent Synthesis of Proofs for Cosmic Mind or God", "", drop_lines=1),
        new_morality(),
    ]
    cat["plan"] = plan_to_end_poverty()
    (OUT / "catalog.json").write_text(json.dumps(cat, indent=1, ensure_ascii=False), encoding="utf-8")
    for k, v in cat.items():
        print(k, len(v), sum(d["words"] for d in v))
