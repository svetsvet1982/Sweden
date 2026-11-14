#!/usr/bin/env python3
"""README.md 의 '대본 목차' 섹션을 src/*.txt 의 @title/@subtitle 로 다시 만든다."""
import glob, os, re
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.join(here, '..')
parts = {}
for f in sorted(glob.glob(os.path.join(root, 'src', 'k*_e*.txt'))):
    name = os.path.basename(f)[:-4]; p, e = re.match(r'k(\d)_e(\d\d)', name).groups()
    t = s = ''
    for line in open(f, encoding='utf-8'):
        if line.startswith('@title '): t = line[7:].strip().split('— ', 1)[-1]
        if line.startswith('@subtitle '): s = line[10:].strip().strip('()')
    parts.setdefault(p, []).append(f"| {int(e)} | [{t}](episodes/{name}.md) | {s} |")
n = sum(len(v) for v in parts.values())
out = [f"## 대본 목차 ({n}/105화 완성)", ""]
for p in sorted(parts):
    out += [f"### {p}부", "", "| 화 | 제목 | 뜻 |", "|---|---|---|"] + parts[p] + [""]
readme = os.path.join(root, 'README.md'); txt = open(readme, encoding='utf-8').read()
txt = re.split(r'\n## 대본 목차', txt)[0].rstrip() + "\n\n" + "\n".join(out)
open(readme, 'w', encoding='utf-8').write(txt.rstrip() + "\n")
print(n)
