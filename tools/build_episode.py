#!/usr/bin/env python3
"""src/pX_eYY.txt → episodes/pX_eYY.md 변환 + 검증.

소스 형식:
  @title 1부 2화 — Boken som blev kvar
  @subtitle (남겨진 책)
  @meta 날짜|9월 27일 토요일 오전
  @intro 도입 설명 (여러 줄 가능)
  # 장면 1 — 장소 설명
  Speaker|A1|Svensk replik|한국어 번역
  @@footer
  (이후는 그대로 붙는 마크다운: 이번 화의 표현, 문화 메모, 다음 화 예고)

검증: 정확히 120턴, 레벨 태그 유효, 같은 화자 연속 발화 금지, 부별 목표 레벨 분포 ±6.
"""
import collections, os, re, sys

TARGETS = {
    "1": {"A1": 32, "A2": 38, "B1": 30, "B2": 20},
    "2": {"A1": 30, "A2": 35, "B1": 33, "B2": 22},
    "3": {"A1": 26, "A2": 32, "B1": 36, "B2": 26},
    "4": {"A1": 26, "A2": 30, "B1": 36, "B2": 28},
}
TOL = 6


def build(src):
    name = os.path.splitext(os.path.basename(src))[0]
    part = re.match(r"p(\d)_e\d\d", name).group(1)
    title = subtitle = ""
    meta, intro, rows, footer, errors = [], [], [], [], []
    in_footer = False
    n, prev = 0, None
    counts = collections.Counter()
    for lineno, raw in enumerate(open(src, encoding="utf-8"), 1):
        line = raw.rstrip("\n")
        if in_footer:
            footer.append(line)
            continue
        if not line.strip():
            continue
        if line.startswith("@@footer"):
            in_footer = True
        elif line.startswith("@title "):
            title = line[7:]
        elif line.startswith("@subtitle "):
            subtitle = line[10:]
        elif line.startswith("@meta "):
            meta.append(line[6:].split("|", 1))
        elif line.startswith("@intro "):
            intro.append(line[7:])
        elif line.startswith("# "):
            rows.append(["H", line[2:], None, None])
        else:
            parts = line.split("|")
            if len(parts) != 4:
                errors.append(f"{lineno}: 필드 4개가 아님: {line[:60]}")
                continue
            sp, lv, sv, ko = (p.strip() for p in parts)
            if lv not in TARGETS["1"]:
                errors.append(f"{lineno}: 잘못된 레벨 {lv}")
            if sp == prev:
                errors.append(f"{lineno}: 같은 화자 연속 ({sp})")
            prev = sp
            n += 1
            counts[lv] += 1
            rows.append(["T", n, sp, lv, sv, ko])
    if n != 120:
        errors.append(f"턴 수 {n} (120이어야 함)")
    for lv, t in TARGETS[part].items():
        if abs(counts[lv] - t) > TOL:
            errors.append(f"{lv} {counts[lv]}턴 — 목표 {t}±{TOL} 벗어남")

    # 장면별 턴 범위
    for i, r in enumerate(rows):
        if r[0] == "H":
            turns = []
            for r2 in rows[i + 1:]:
                if r2[0] == "H":
                    break
                turns.append(r2[1])
            r[2], r[3] = (turns[0], turns[-1]) if turns else (0, 0)

    dist = " · ".join(f"`{k}` {counts[k]}턴" for k in ["A1", "A2", "B1", "B2"]) + f" (총 {n}턴)"
    out = [f"# {title}", f"### {subtitle}", "", "| 항목 | 내용 |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in meta]
    out += [f"| 레벨 분포 | {dist} |", ""]
    out += [f"> {l}" if l else ">" for l in intro]
    for r in rows:
        if r[0] == "H":
            out.append(f"\n---\n\n## {r[1]} (턴 {r[2]:03d}–{r[3]:03d})\n")
        else:
            _, i, sp, lv, sv, ko = r
            out.append(f"**{i:03d}** {sp} `{lv}`  \n{sv}\n> {ko}\n")
    out.append("\n---\n")
    out += footer
    dst = os.path.join(os.path.dirname(os.path.abspath(src)), "..", "episodes", name + ".md")
    with open(os.path.normpath(dst), "w", encoding="utf-8") as f:
        f.write("\n".join(out).rstrip() + "\n")
    print(f"{name}: {dist}")
    for s in [r for r in rows if r[0] == "H"]:
        print(f"  {s[2]:03d}–{s[3]:03d} {s[1]}")
    return errors


if __name__ == "__main__":
    bad = False
    for src in sys.argv[1:]:
        errs = build(src)
        for e in errs:
            print("  ✗", e)
        bad |= bool(errs)
    sys.exit(1 if bad else 0)
