#!/usr/bin/env python3
"""src/*.txt + bible.md → pdf/ (부별 PDF 4개 + 전체 PDF 1개).

필요: pip install markdown playwright, Noto CJK 폰트, Chromium.
CHROMIUM 환경변수로 실행 파일 경로를 바꿀 수 있다 (기본 /opt/pw-browsers/chromium).
"""
import glob, html, os, re, sys
import markdown
from playwright.sync_api import sync_playwright

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "pdf")
PARTS = {
    1: ("1부 · 가을", "Ursäkta, jobbar du här?", "#b5562b"),
    2: ("2부 · 겨울", "Mörker och ljus", "#2f5d8a"),
    3: ("3부 · 봄", "Isen släpper", "#4f7d3a"),
    4: ("4부 · 여름", "Skärgården", "#b08a1e"),
}
LEVEL_COLORS = {"A1": "#3c8d5a", "A2": "#2f7fa8", "B1": "#8a5bb0", "B2": "#c0473b"}

CSS = """
@page { size: A4; margin: 18mm 17mm 18mm 17mm; }
* { box-sizing: border-box; }
body { font-family: 'Noto Serif CJK KR', 'Noto Serif CJK JP', serif; font-size: 10pt; line-height: 1.55; color: #222; }
h1, h2, h3, .sans { font-family: 'Noto Sans CJK KR', 'Noto Sans CJK JP', sans-serif; }
.cover { height: 255mm; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; page-break-after: always; }
.cover .t { font-size: 46pt; font-weight: 700; letter-spacing: 2px; margin: 0; }
.cover .s { font-size: 14pt; color: #555; margin-top: 8mm; }
.cover .m { font-size: 10.5pt; color: #777; margin-top: 30mm; line-height: 1.9; }
.partpage { height: 255mm; display: flex; flex-direction: column; justify-content: center; text-align: center; page-break-before: always; page-break-after: always; }
.partpage .n { font-size: 30pt; font-weight: 700; }
.partpage .sv { font-size: 18pt; font-style: italic; margin-top: 6mm; }
.toc { page-break-after: always; }
.toc h2 { font-size: 16pt; border-bottom: 2px solid #333; padding-bottom: 2mm; }
.toc table { width: 100%; border-collapse: collapse; font-size: 9.5pt; }
.toc td { padding: 1.2mm 2mm; border-bottom: 1px solid #e3e3e3; }
.toc td.p { color: #888; width: 18mm; }
.ep { page-break-before: always; }
.ep-head { border-left: 6px solid var(--c); padding: 2mm 0 2mm 5mm; margin-bottom: 4mm; }
.ep-head .no { font-family: 'Noto Sans CJK KR', sans-serif; font-size: 9pt; color: var(--c); font-weight: 700; letter-spacing: 1px; }
.ep-head h1 { font-size: 20pt; margin: 1mm 0 0 0; }
.ep-head .ko { font-size: 11pt; color: #666; }
table.meta { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 3mm 0; }
table.meta td { border: 1px solid #ddd; padding: 1.5mm 2.5mm; vertical-align: top; }
table.meta td.k { background: #f5f5f3; width: 22mm; font-family: 'Noto Sans CJK KR', sans-serif; }
.intro { background: #f7f5f0; border-radius: 2mm; padding: 3mm 4mm; font-size: 9.3pt; color: #444; margin-bottom: 3mm; }
.intro p { margin: 0 0 1.5mm 0; }
h2.scene { font-size: 11.5pt; color: var(--c); margin: 6mm 0 2.5mm 0; padding-bottom: 1mm; border-bottom: 1px solid #ddd; page-break-after: avoid; }
.turn { display: grid; grid-template-columns: 9mm 21mm 1fr; column-gap: 2mm; padding: 1.3mm 0; border-bottom: 1px dotted #e5e5e5; page-break-inside: avoid; }
.turn .num { font-family: 'Noto Sans CJK KR', sans-serif; font-size: 7.5pt; color: #aaa; padding-top: 0.8mm; }
.turn .who { font-family: 'Noto Sans CJK KR', sans-serif; font-size: 8.5pt; font-weight: 700; padding-top: 0.4mm; }
.turn .lv { display: inline-block; font-size: 6.8pt; color: #fff; border-radius: 1mm; padding: 0 1.2mm; margin-top: 0.6mm; font-weight: 700; }
.turn .sv { font-size: 10.3pt; color: #111; }
.turn .ko { font-size: 8.8pt; color: #666; margin-top: 0.4mm; }
.footer-md { page-break-before: auto; margin-top: 6mm; font-size: 9.2pt; }
.footer-md h2 { font-size: 12pt; margin: 5mm 0 2mm 0; border-bottom: 1px solid #ccc; padding-bottom: 1mm; }
.footer-md table { border-collapse: collapse; width: 100%; font-size: 8.6pt; margin: 2mm 0; }
.footer-md th, .footer-md td { border: 1px solid #ddd; padding: 1.3mm 2mm; vertical-align: top; text-align: left; }
.footer-md th { background: #f2f2ef; font-family: 'Noto Sans CJK KR', sans-serif; }
.footer-md code { font-family: 'Noto Sans CJK KR', sans-serif; font-size: 7.5pt; background: #eee; padding: 0 1mm; border-radius: 1mm; }
.bible { page-break-before: always; font-size: 9.5pt; }
.bible h1 { font-size: 18pt; } .bible h2 { font-size: 13pt; margin-top: 6mm; border-bottom: 1px solid #ccc; }
.bible table { border-collapse: collapse; width: 100%; font-size: 8.6pt; margin: 2mm 0; }
.bible th, .bible td { border: 1px solid #ddd; padding: 1.2mm 2mm; vertical-align: top; text-align: left; }
.bible th { background: #f2f2ef; }
.bible pre { background: #f5f5f5; padding: 2mm; font-size: 8pt; white-space: pre-wrap; }
.legend { font-family: 'Noto Sans CJK KR', sans-serif; font-size: 8.5pt; margin-top: 6mm; }
.legend span.lv { color: #fff; border-radius: 1mm; padding: 0 1.5mm; font-weight: 700; margin-right: 1mm; }
"""

def md(text):
    return markdown.markdown(text, extensions=["tables"])

def inline(text):
    return md(text).removeprefix("<p>").removesuffix("</p>")

def parse(path):
    d = {"title": "", "subtitle": "", "meta": [], "intro": [], "rows": [], "footer": []}
    in_footer = False
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if in_footer:
            d["footer"].append(line); continue
        if not line.strip(): continue
        if line.startswith("@@footer"): in_footer = True
        elif line.startswith("@title "): d["title"] = line[7:]
        elif line.startswith("@subtitle "): d["subtitle"] = line[10:]
        elif line.startswith("@meta "): d["meta"].append(line[6:].split("|", 1))
        elif line.startswith("@intro "): d["intro"].append(line[7:])
        elif line.startswith("# "): d["rows"].append(("H", line[2:]))
        else:
            sp, lv, sv, ko = (p.strip() for p in line.split("|"))
            d["rows"].append(("T", sp, lv, sv, ko))
    return d

def episode_html(path, color):
    d = parse(path)
    m = re.match(r"(\d)부 (\d+)화 — (.*)", d["title"])
    no, title = (f"{m.group(1)}부 {m.group(2)}화", m.group(3)) if m else ("", d["title"])
    h = [f'<section class="ep" style="--c:{color}">',
         f'<div class="ep-head"><div class="no">{no}</div><h1>{html.escape(title)}</h1>'
         f'<div class="ko">{html.escape(d["subtitle"])}</div></div>',
         '<table class="meta">'] + [f'<tr><td class="k">{html.escape(k)}</td><td>{inline(v)}</td></tr>' for k, v in d["meta"]] + ["</table>"]
    if d["intro"]:
        h.append('<div class="intro">' + "".join(f"<p>{inline(i)}</p>" for i in d["intro"]) + "</div>")
    n = 0
    for r in d["rows"]:
        if r[0] == "H":
            h.append(f'<h2 class="scene">{html.escape(r[1])}</h2>')
        else:
            n += 1
            _, sp, lv, sv, ko = r
            h.append(f'<div class="turn"><div class="num">{n:03d}</div>'
                     f'<div><div class="who">{html.escape(sp)}</div><span class="lv" style="background:{LEVEL_COLORS.get(lv, "#888")}">{lv}</span></div>'
                     f'<div><div class="sv">{inline(sv)}</div><div class="ko">{inline(ko)}</div></div></div>')
    h.append('<div class="footer-md">' + md("\n".join(d["footer"])) + "</div></section>")
    return title, d["subtitle"], "\n".join(h)

def cover(sub, meta):
    return (f'<div class="cover"><p class="t sans">Lyktan</p><p class="s">{sub}</p>'
            f'<p class="m">{meta}</p></div>')

def legend():
    return ('<div class="legend">레벨 표시: ' + " ".join(
        f'<span class="lv" style="background:{c}">{k}</span>' for k, c in LEVEL_COLORS.items()) + "</div>")

def doc(body, title):
    return f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>'

def part_body(p):
    name, sv, color = PARTS[p]
    eps = [episode_html(f, color) for f in sorted(glob.glob(os.path.join(ROOT, "src", f"p{p}_e*.txt")))]
    toc = '<div class="toc"><h2>' + name + ' — 목차</h2><table>' + "".join(
        f'<tr><td class="p">{i}화</td><td><b>{html.escape(t)}</b></td><td>{html.escape(s.strip("()"))}</td></tr>'
        for i, (t, s, _) in enumerate(eps, 1)) + "</table></div>"
    pp = f'<div class="partpage" style="color:{color}"><div class="n sans">{name}</div><div class="sv">{sv}</div></div>'
    return pp + toc + "".join(e[2] for e in eps)

def render(pw, html_text, out, title):
    b = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM", "/opt/pw-browsers/chromium"))
    pg = b.new_page()
    pg.set_content(html_text, wait_until="load")
    pg.pdf(path=out, format="A4", print_background=True, display_header_footer=True,
           header_template="<span></span>",
           footer_template=f'<div style="width:100%;font-size:7pt;color:#999;text-align:center;font-family:sans-serif">'
                           f'Lyktan · {html.escape(title)} · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
           margin={"top": "16mm", "bottom": "16mm", "left": "15mm", "right": "15mm"})
    b.close()
    print("wrote", os.path.relpath(out, ROOT))

def main():
    os.makedirs(OUT, exist_ok=True)
    bible = '<section class="bible">' + md(open(os.path.join(ROOT, "bible.md"), encoding="utf-8").read()) + "</section>"
    meta = "스웨덴어 대화 드라마 · 4부 × 14화 × 120턴<br>A1–B2 혼합 · 스웨덴어 대사 + 한국어 번역"
    with sync_playwright() as pw:
        parts = {}
        for p in PARTS:
            parts[p] = part_body(p)
            name, sv, _ = PARTS[p]
            render(pw, doc(cover(f"{name} — <i>{sv}</i>", meta + legend()) + parts[p], f"Lyktan {name}"),
                   os.path.join(OUT, f"Lyktan_{p}부.pdf"), name)
        full = cover("스톡홀름의 작은 서점에서 시작된 사계절", meta + legend()) + bible + "".join(parts[p] for p in PARTS)
        render(pw, doc(full, "Lyktan 전체"), os.path.join(OUT, "Lyktan_전체.pdf"), "전체")

if __name__ == "__main__":
    main()
