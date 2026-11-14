#!/usr/bin/env python3
"""부별 기획 파일 검증: 화 수 15, 장면 턴 001–150 연속, 화별 단어 수."""
import re, glob, os
here = os.path.dirname(os.path.abspath(__file__))
for f in sorted(glob.glob(os.path.join(here, '..', 'part*.md'))):
    txt = open(f).read()
    eps = re.split(r'^### ', txt, flags=re.M)[1:]
    eps[-1] = re.split(r'^## ', eps[-1], flags=re.M)[0]
    bad = []
    for e in eps:
        rs = [(int(a), int(b)) for a, b in re.findall(r'^\s*-\s*\**(\d{3})[–-](\d{3})', e, flags=re.M)]
        ok = rs and rs[0][0] == 1 and rs[-1][1] == 150 and all(rs[i][1] + 1 == rs[i+1][0] for i in range(len(rs)-1))
        if not ok: bad.append(e.splitlines()[0][:40])
    w = [len(e.split()) for e in eps]
    print(f"{os.path.basename(f)}: {len(eps)}화, 단어 {min(w)}–{max(w)}, 턴범위 오류 {len(bad)} {bad}")
