"""Imports the Plan to End Poverty working papers (Civic Credits, Poverty Elimination Centers, LifeLink)
into src/library/ and adds them to catalog.json under "working".

    python tools/import_poverty.py [folder holding "Civic Credits", "PEC" and "lifelink"]

Needs pandoc and pdftotext. The 2025 edition of the Plan itself is imported by import_library.py.
"""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import import_library as L  # noqa: E402

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/mnt/user-data/uploads")
CC, PEC, LL = SRC / "Civic Credits", SRC / "PEC", SRC / "lifelink"

# (programme, group, slug, file stem, folder, title, subtitle, date, has pdf)
DOCS = [
    ("civic-credits", "Start here", "cc-ending-poverty-by-2050", "Ending Poverty by 2050", CC,
     "Ending Poverty by 2050: Civic Credits, Explained", "A complete public lecture for first-time audiences", "2025-09", True),
    ("civic-credits", "Start here", "cc-everyday-guide", "Civic Credits — Everyday Guide (for Ordinary Citizens And Small Businesses)", CC,
     "Civic Credits, Simply", "An everyday guide for citizens and small businesses", "2025-09", "pdf-only"),
    ("civic-credits", "How it works", "cc-technical-white-paper", "Civic Credits — Technical White Paper (logic, Mechanics, Objections)", CC,
     "Civic Credits: A Debt-Free Employment and Settlement System for Essential Work", "Technical white paper: logic, mechanics and objections", "2025-09", "pdf-only"),
    ("civic-credits", "How it works", "cc-funding-and-operations", "Funding and Operations for Civic Credits", CC,
     "Funding and Operations for Civic Credits", "Utilizing public resources: the Civic Clearinghouse and the daily wage cycle", "2025-08", True),
    ("civic-credits", "How it works", "cc-national-integration", "National Integration of Civic Credits into Existing Payment Systems", CC,
     "National Integration of Civic Credits into Existing Payment Systems", "White paper", "2025-08", True),
    ("civic-credits", "Foundations", "cc-civic-charter-for-resources", "Civic Charter for Resources", CC,
     "Civic Charter for Resources", "Adopted by People of the World", "2025-11", True),
    ("civic-credits", "Foundations", "cc-proposal-2024", "Civic Credits Proposal", CC,
     "Civic Credits System Proposal", "Building economic foundations for all · first proposal, 2024", "2024-05", True),

    ("poverty-elimination-centers", "Start here", "pec-proposal", "Poverty Elimination Centers", PEC,
     "Poverty Elimination Centers", "Programmes, finance, operations, outreach and risk", "2024-05", True),
    ("poverty-elimination-centers", "Running a centre", "pec-operational-guidelines", "Operational Guidelines for Poverty Elimination Centers", PEC,
     "Operational Guidelines for Poverty Elimination Centers", "", "2024-05", True),
    ("poverty-elimination-centers", "Running a centre", "pec-civic-credits-integration", "The Integration of Civic Credits and Poverty Elimination Centers", PEC,
     "The Integration of Civic Credits and Poverty Elimination Centers", "A comprehensive plan for global economic and social transformation", "2024-05", False),
    ("poverty-elimination-centers", "Project planning", "pec-project-charter", "Project Charter for Poverty Elimination Centers (PECs)", PEC,
     "Project Charter for Poverty Elimination Centers", "", "2024-05", True),
    ("poverty-elimination-centers", "Project planning", "pec-charter-review", "Poverty Elimination Centers - Review", PEC,
     "Project Charter Review for Poverty Elimination Centers", "", "2024-05", False),
    ("poverty-elimination-centers", "Project planning", "pec-work-breakdown", "Detailed Work Breakdown Structure (WBS)", PEC,
     "Detailed Work Breakdown Structure for Poverty Elimination Centers", "", "2024-05", True),

    ("lifelink", "Start here", "ll-open-letter", "Lifelink interest letter", LL,
     "The Future Begins with LifeLink", "An open letter to the citizens of the world", "2025-01", False),
    ("lifelink", "Start here", "ll-synergy-proposal", "LifeLink, Civic Credits, and Poverty Elimination Centers (PECs) Synergy Proposal", LL,
     "LifeLink, Civic Credits and Poverty Elimination Centers: Synergy Proposal", "How the three instruments work as one system", "2025-01", False),
    ("lifelink", "Start here", "ll-daily-implementation", "LifeLink Daily Implementation", LL,
     "LifeLink Daily Implementation and Quality of Life", "A day with LifeLink, morning to evening", "2025-01", True),
    ("lifelink", "Design", "ll-design-specification", "Lifelink design specification", LL,
     "LifeLink Core Specification", "", "2025-01", True),
    ("lifelink", "Design", "ll-tablet", "The LifeLink Tablet", LL,
     "The LifeLink Tablet", "Civic engagement and societal integration", "2025-01", True),
    ("lifelink", "Devices", "ll-look-smart-glasses", "look smart glasses", LL, "LifeLink Look Smart Glasses", "Technical specification and integration", "2025-01", True),
    ("lifelink", "Devices", "ll-hear-buds", "Hear Buds", LL, "LifeLink Hear Buds", "Technical specification and integration", "2025-01", True),
    ("lifelink", "Devices", "ll-smartwatch", "Smartwatch", LL, "LifeLink Smartwatch", "Technical specification and integration", "2025-01", True),
    ("lifelink", "Devices", "ll-touch-smart-ring", "Touch Smart Ring", LL, "LifeLink Touch Smart Ring", "Technical specification and integration", "2025-01", True),
]
STRATEGIES = [  # (group, stem after "LifeLink ")
    ("Building and funding it", "Development & Execution Plan"), ("Building and funding it", "Technical Development Roadmap"),
    ("Building and funding it", "Hardware & Infrastructure Deployment Plan"), ("Building and funding it", "Funding & Sustainability Model"),
    ("Building and funding it", "Economic & Market Integration Strategy"), ("Building and funding it", "Interoperability & Cross-Platform Integration Plan"),
    ("Serving people", "Education & Digital Literacy Strategy"), ("Serving people", "Health & Wellness Strategy"),
    ("Serving people", "Community & Social Impact Strategy"), ("Serving people", "Humanitarian & Global Aid Strategy"),
    ("Serving people", "Environmental Sustainability & Climate Action Plan"), ("Serving people", "User Experience & Public Training Guide"),
    ("Safeguards and governance", "Ethical AI & Data Privacy Framework"), ("Safeguards and governance", "Legal & Ethical Safeguards Framework"),
    ("Safeguards and governance", "Policy & Regulatory Compliance Framework"), ("Safeguards and governance", "Smart Governance & AI Policy Strategy"),
    ("Safeguards and governance", "Crisis Management & Security Protocols"), ("Safeguards and governance", "Cultural & Ethical Adoption Strategy"),
    ("Growing worldwide", "Global Civic Adoption Plan"), ("Growing worldwide", "Global Expansion & Strategic Scaling Plan"),
    ("Growing worldwide", "Strategic Partnership & Outreach Plan"), ("Growing worldwide", "Public Communications & Media Strategy"),
    ("Growing worldwide", "Impact Assessment & Measurement Plan"),
]
for g, stem in STRATEGIES:
    DOCS.append(("lifelink", g, "ll-" + L.re.sub(r"[^a-z0-9]+", "-", stem.lower().replace("&", "and")).strip("-"), "LifeLink " + stem, LL,
                 "LifeLink " + stem.replace("&", "and"), "", "2025-01", True))


def same(a, b):
    k = lambda s: re.sub(r"[^a-z]", "", s.lower().replace("&", "and"))
    return k(a)[:25] == k(b)[:25] or k(b) in k(a) or k(a) in k(b)


def strip_title(h, title):
    """Drop a leading heading or paragraph that only repeats the title (and an empty Step label line)."""
    for _ in range(2):
        m = re.match(r"\s*<(h\d|p)[^>]*>(.*?)</\1>", h, re.S)
        if not m: break
        txt = L.html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        if not txt or same(txt, title) or re.match(r"^(step \d+:|📌)", txt, re.I) and len(txt) < 80:
            h = h[m.end():]
        else:
            break
    return h


def pdf_only(path):
    """Text PDFs from a word processor: rebuild headings, paragraphs and list items from line lengths."""
    raw = L.subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True, check=True).stdout
    lines = [l.strip().replace("\u2011", "-") for l in raw.replace("\f", "\n").split("\n")]
    lines = [l for l in lines if not re.fullmatch(r"\d{1,3}", l)]
    width = max(len(l) for l in lines)
    blocks, buf = [], []

    def flush():
        if buf:
            t = " ".join(buf)
            blocks.append(("li", t[1:].strip()) if t[:1] in "•-" else ("p", t))
            buf.clear()
    for i, l in enumerate(lines):
        if not l:
            flush(); continue
        nxt = next((x for x in lines[i + 1:] if x), "")
        if not buf and len(l) < 70 and not l.endswith((".", ",", ";", ":")) and l[:1].isupper() and len(l.split()) <= 10 \
                and (nxt[:1].isupper() or nxt[:1].isdigit()):
            blocks.append(("h3", l)); continue
        if l[:1] in "•" and buf:
            flush()
        buf.append(l)
        if l.endswith((".", "?", "!", ":", "”", '"')) and len(l) < width * 0.85:
            flush()
    flush()
    return L.blocks_html(blocks)


if __name__ == "__main__":
    catp = L.OUT / "catalog.json"
    cat = json.loads(catp.read_text(encoding="utf-8"))
    working = []
    for prog, group, slug, stem, folder, title, sub, date, pdf in DOCS:
        if pdf == "pdf-only":
            src = folder / f"{stem}.pdf"
            h = pdf_only(src)
        else:
            src = folder / f"{stem}.odt"
            h = L.pandoc(src, "odt", "html5", is_path=True)
            h = re.sub(r"<img[^>]*>", "", h)
            h = re.sub(r"<figure>\s*(<figcaption>.*?</figcaption>)?\s*</figure>", "", h, flags=re.S)
        h = L.tidy_html(h)
        h = strip_title(h, title)
        h = h.replace("[]", "")
        h = re.sub(r"<(h\d)([^>]*)>(.*?)</\1>", lambda m: f"<{m.group(1)}{m.group(2)}>{re.sub(r'</?strong>', '', m.group(3))}</{m.group(1)}>", h, flags=re.S)
        e = L.save(slug, title, sub, h, L.pandoc(h, "html", "gfm"), src.name)
        if pdf:
            shutil.copy(folder / f"{stem}.pdf", L.OUT / f"{slug}.pdf")
        e |= {"programme": prog, "group": group, "date": date, "pdf": bool(pdf)}
        working.append(e)
        print(f"{slug:48s} {e['words']:6d} words  pdf={bool(pdf)}")
    cat["working"] = working
    catp.write_text(json.dumps(cat, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(working), "documents,", sum(e["words"] for e in working), "words")
