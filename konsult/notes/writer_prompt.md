You are writing one episode of a Swedish-language business dialogue drama ("Frågan bakom frågan") for Korean learners of Swedish (B1–C1). Project dir: /home/user/Sweden/konsult. Do NOT commit or push; just create/edit files.

Task: write **part {P}, episode {E}** ({P}부 {E}화) as `src/p{P}_e{EE}.txt`, then build with `python3 tools/build_episode.py src/p{P}_e{EE}.txt` and fix until it exits 0 with no ✗ errors.

Read first: `bible.md` (characters, voices, levels, real-event rules), the outline for this episode and its neighbours in `{PARTFILE}`, `notes/continuity.md` (fully), the previous episode's source `{PREV}` if it exists (continue from it; also a format/quality reference — if none, read the docstring of tools/build_episode.py for the format), and the docstring of `tools/build_episode.py`.

Requirements:
- Exactly 120 turns; one turn = one speaker's line. Never the same speaker twice in a row (also across scene headers `# 장면 N — ...`).
- Follow the outline's scenes and approximate turn ranges (±5 per scene OK), use each of its four 핵심 표현 verbatim in the dialogue, and land its 엔딩 훅. If the outline contradicts established continuity, continuity wins; note it in your report.
- Level tags A2/B1/B2/C1 must honestly reflect the Swedish sentence difficulty; mix within scenes. Target per episode for this part: {TARGET} (validator allows ±6; aim within ±3).
- Natural, correct, idiomatic contemporary standard Swedish (rikssvenska). Business register in meetings, colloquial among colleagues (Amir: typ, asså, ba, sjukt among friends; perfect formal Swedish with clients). Henrik mixes English consulting jargon. Double-check grammar: en/ett gender, adjective agreement, V2 order, negation placement in subordinate clauses, definite forms, prepositions.
- The episode must be substantive: real consulting/management/audit/political reasoning with concrete (fictional) numbers, and accurate background on the real Swedish issue named in the outline (no invented quotes from real people/parties; real companies only as background news).
- Korean translation on every turn, natural and following the 번역 규칙 in continuity notes. Stage directions inside the Korean column in parentheses. No extra fields; no `|` inside text.
- Header: `@title {P}부 {E}화 — <Swedish title>`, `@subtitle (<Korean title>)`, `@meta` rows 날짜, 장소, 등장인물, 이번 화의 도구, 스웨덴 현안; `@intro` lines: short "**지난 이야기**" recap of the previous episode (or series intro for 1부 1화) + scene-setting paragraph.
- Footer after `@@footer`: "## 이번 화의 표현" table (10 rows: 레벨|표현|뜻|포인트), "## 현안 메모" (3–4 accurate bullets on the Swedish issue), "## 비즈니스 메모" (1–2 bullets explaining the tool), "## 다음 화 예고 — <next Swedish title>" teaser consistent with the outline (for a part's last episode, preview the next part's ep 1; for 4부 16화 write "## 시리즈를 마치며" instead).

After the build passes, append "### {P}부 {E}화" to `notes/continuity.md` with 4–8 bullets of new facts later episodes must respect (names, numbers, decisions, promises, running jokes).

Finally report in ≤5 lines: build distribution line, scene ranges, any outline deviations.
