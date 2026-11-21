"""Restore German capitalisation in reference lists. Pandoc's citeproc title-cases titles as if
English ("Annalen Der Physik"); German capitalises nouns only. Run on src/library/*.html and *.md."""
import re, sys, pathlib
TITLES = [
    "Annalen der Physik",
    "Die Grundlage der allgemeinen Relativitätstheorie",
    "Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften",
    "Sitzungsberichte der Königlich Preussischen Akademie der Wissenschaften",
    "Sitzungsberichte der Preussischen Akademie der Wissenschaften, Physikalisch-mathematische Klasse",
    "Äther und Relativitätstheorie",
    "Über das Relativitätsprinzip und die aus demselben gezogenen Folgerungen",
    "Über den anschaulichen Inhalt der quantentheoretischen Kinematik und Mechanik",
    "Über die Elektricitätsmenge, welche bei galvanischen Strömen durch den Querschnitt der Kette fliesst",
    "Über die Wärme-Leitungsfähigkeit der Metalle",
    "Über die Ablenkung eines Lichtstrals von seiner geradlinigen Bewegung",
    "Über die Berechnung molekularer Eigenfrequenzen",
    "Über die kräftefreie Bewegung in der relativistischen Quantenmechanik",
    "Über Integrale der hydrodynamischen Gleichungen, welche den Wirbelbewegungen entsprechen",
    "Über magnetische Manganlegierungen",
    "Über verschiedene für die Anwendung bequeme Formen der Hauptgleichungen der mechanischen Wärmetheorie",
    "Zeitschrift für Physik",
]
UMLAUT = re.compile(r'<span>([ÄÖÜäöüß])</span>')  # bibtex accent braces become bare spans
NOCASE = re.compile(r'<span class="nocase">([^<>]*)</span>')
def fix(text):
    prev = None
    while prev != text:  # unwrap nested nocase markers (they carry no styling)
        prev, text = text, UMLAUT.sub(r"\1", NOCASE.sub(r"\1", text))
    n = 0
    for t in TITLES:
        text, k = re.subn(re.escape(t), t, text, flags=re.IGNORECASE)
        n += k
    text, k = re.subn(r"Gravity Probe b\b", "Gravity Probe B", text); n += k  # citeproc lowercases the lone letter
    return text, n
if __name__ == "__main__":
    for p in map(pathlib.Path, sys.argv[1:]):
        s = p.read_text(encoding="utf-8"); t, n = fix(s)
        if t != s:
            p.write_text(t, encoding="utf-8"); print(p.name, n)
