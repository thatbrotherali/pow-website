"""Publish one second-edition part of Graviton Pressure Theory to the site's library.

    python tools/publish_part.py <part folder> <slug> [--path url-path] [--lead "..."]

The part folder holds part<NN>.tex (which inputs ../common/preamble), part<NN>.bib, the
compiled part<NN>.pdf, and figs/ with an .svg beside every figure .pdf.  The script writes
src/library/<slug>.{html,md,tex,bib,pdf}, copies the SVG figures to src/library/figures/<slug>/,
and updates the part's entry in src/library/catalog.json.  It needs pandoc.
"""
import argparse, json, re, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import status_marks as SM
from import_library import pandoc, tidy_html, save, braced

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "src" / "library"


def macro(t, name):
    m = re.search(r"\\newcommand\{\\" + name + r"\}\{", t)
    return braced(t, m.end() - 1)[0] if m else ""


def body_of(t):
    b = t[t.index("\\begin{document}") + len("\\begin{document}"):t.index("\\end{document}")]
    for pat in (r"\\gptitle", r"\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}", r"\\clearpage", r"\\newpage",
                r"\\bibliography\{[^}]*\}", r"\\enlargethispage\{[^}]*\}", r"\\FloatBarrier"):
        b = re.sub(pat, "", b)
    # standalone sources (Parts 1-4, 6, 7, 11-24) carry their own title page and contents
    b = re.sub(r"\\begin\{titlepage\}.*?\\end\{titlepage\}", "", b, flags=re.S)
    b = re.sub(r"\\tableofcontents|\\thispagestyle\{[^}]*\}|\\setcounter\{page\}\{\d+\}", "", b)
    return b


def resolve_footnotemarks(b):
    """\\footnotemark{} ... \\footnotetext{..} groups (used inside boxes) become ordinary footnotes."""
    def group(m):
        block = m.group(0)
        texts = []
        for k in [x.end() - 1 for x in re.finditer(r"\\footnotetext\{", block)]:
            texts.append(braced(block, k)[0])
        main = re.sub(r"\\addtocounter\{footnote\}\{-?\d+\}|\\stepcounter\{footnote\}", "", block)
        main = re.sub(r"\\footnotetext\{", "\\\\FNTEXT{", main)
        while "\\FNTEXT{" in main:  # drop the texts
            k = main.index("\\FNTEXT{")
            main = main[:k] + main[braced(main, k + 7)[1]:]
        it = iter(texts)
        main = re.sub(r"\\footnotemark(\{\})?", lambda _: "\\footnote{" + next(it) + "}", main)
        assert next(it, None) is None, "more footnote texts than marks"
        return main
    # a group runs from the first \footnotemark to the last \footnotetext that follows it
    return re.sub(r"\\footnotemark.*?\\footnotetext\{[^\n]*?(?=\n\s*\n|\\end\{)", group, b, flags=re.S)


def number_refs(b, part):
    labels = {}
    for env, word in (("figure", "Figure"), ("table", "Table")):
        for i, m in enumerate(re.finditer(r"\\begin\{" + env + r"\}.*?\\end\{" + env + r"\}", b, re.S), 1):
            for lab in re.findall(r"\\label\{([^}]+)\}", m.group(0)):
                labels[lab] = f"{part}.{i}"
    # equations: number them as print does, (1), (2), ..., and show the number on the web with \tag
    eq, count = {}, [0]
    def tag_eq(m):
        body = m.group(0); count[0] += 1; no = str(count[0])
        labs = re.findall(r"\\label\{([^}]+)\}", body)
        for lab in labs:
            eq[lab] = no
            body = body.replace("\\label{" + lab + "}", "")
        return body.replace("\\end{equation}", "\\tag{" + no + "}\\end{equation}")
    b = re.sub(r"\\begin\{equation\}.*?\\end\{equation\}", tag_eq, b, flags=re.S)
    b = re.sub(r"\\eqref\{([^}]+)\}", lambda m: f"({eq[m.group(1)]})" if m.group(1) in eq else m.group(0), b)
    b = re.sub(r"\\ref\{([^}]+)\}", lambda m: labels.get(m.group(1), eq.get(m.group(1), m.group(0))), b)
    return b


def to_web(b, part, slug):
    b = b.replace("\\textsuperscript{,}", "")
    # pandoc drops a number that opens a cell in a >{\raggedright\arraybackslash} column: keep the spec plain
    b = re.sub(r">\{\\raggedright(\\arraybackslash)?\}", "", b)
    b = re.sub(r"\\fn\{([^}]+)\}", r"\\footnote{\\citealp{\1}.}", b)
    b = resolve_footnotemarks(b)
    b = number_refs(b, part)
    b = re.sub(r"\\includegraphics(\[[^\]]*\])?\{([^}]+?)(\.pdf)?\}", r"\\includegraphics{assets/figures/\2.svg}", b)
    return b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder"); ap.add_argument("slug")
    ap.add_argument("--path"); ap.add_argument("--lead")
    a = ap.parse_args()
    folder = Path(a.folder).resolve()
    tex_path = next(folder.glob("part*.tex"))
    t = tex_path.read_text(encoding="utf-8")
    part, title, subtitle = int(macro(t, "gptpart")), macro(t, "gpttitle"), macro(t, "gptsubtitle")
    bib = tex_path.with_suffix(".bib")

    web = SM.to_tokens(to_web(body_of(t), part, a.slug))
    args = ["--mathjax", "--citeproc", "--bibliography", str(bib)]
    h = SM.to_html(pandoc(web, "latex", "html5", args))
    h = SM.KEY_HTML + tidy_html(h)
    # pandoc numbers nothing on the web; drop the unnumbered class it would add to starred sections
    h = re.sub(r'<figure>\s*<img src="(assets/figures/[^"]+)"[^>]*/>', r'<figure>\n<img src="\1" alt="" />', h)
    # numbered sections carry their print numbers (starred ones stay unnumbered)
    sec = [0, 0]
    def num(m):
        if m.group(1) == "2":
            sec[0] += 1; sec[1] = 0; no = f"{part}.{sec[0]}"
        else:
            sec[1] += 1; no = f"{part}.{sec[0]}.{sec[1]}"
        return f'<h{m.group(1)} id="{m.group(2)}"><span class="secno">{no}</span> '
    h = re.sub(r'<h([23]) id="([^"]+)">', num, h)
    # tables and figures carry their numbers on the web as in print; widths are left to the stylesheet
    h = re.sub(r'<table style="[^"]*">', "<table>", h)
    h = re.sub(r'<col style="[^"]*" />', "<col />", h)
    for tag, word, env in (("figcaption", "Figure", "figure"), ("caption", "Table", "table")):
        n = iter(range(1, 1000))
        h = re.sub(rf"<{tag}>(\s*<p>)?", lambda m: f"<{tag}>{m.group(1) or ''}<strong>{word} {part}.{next(n)}.</strong> ", h)
    md = SM.KEY_MD + SM.to_md(pandoc(web, "latex", "gfm", args))
    import fix_german_titles as FG  # citeproc title-cases German titles as if English
    h, md = FG.fix(h)[0], FG.fix(md)[0]
    entry = save(a.slug, title, subtitle, h, md, f"Part {part} - {title} (2nd ed.).tex")

    # self-contained LaTeX source, bibliography and PDF beside the web copies
    pre = (folder.parent / "common" / "preamble.tex").read_text(encoding="utf-8")
    flat = t.replace("\\input{../common/preamble}", pre).replace("\\graphicspath{{figs/}}", "\\graphicspath{{figs/}}")
    (LIB / f"{a.slug}.tex").write_text(flat, encoding="utf-8")
    shutil.copy(bib, LIB / f"{a.slug}.bib")
    shutil.copy(tex_path.with_suffix(".pdf"), LIB / f"{a.slug}.pdf")
    figs = sorted((folder / "figs").glob("*.svg"))
    if figs:
        d = LIB / "figures" / a.slug
        d.mkdir(parents=True, exist_ok=True)
        for f in figs:
            shutil.copy(f, d / f.name)

    cat_path = LIB / "catalog.json"
    cat = json.loads(cat_path.read_text(encoding="utf-8"))
    for i, e in enumerate(cat["framework"]):
        if e["slug"] == a.slug:
            new = {**e, **entry, "part": part, "pdf": True}
            if a.path: new["path"] = a.path
            if a.lead: new["lead"] = a.lead
            cat["framework"][i] = new
            break
    else:
        raise SystemExit(f"{a.slug} is not in the framework catalogue")
    cat_path.write_text(json.dumps(cat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(new, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
