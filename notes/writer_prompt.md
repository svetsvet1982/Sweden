You are writing one episode of a Swedish-language dialogue drama for Korean learners of Swedish. Repo: /home/user/Sweden. Do NOT commit or push; just create files.

Task: write **part {P}, episode {E}** ({P}부 {E}화) as source file `src/p{P}_e{EE}.txt`, then build it with `python3 tools/build_episode.py src/p{P}_e{EE}.txt` and fix until it exits 0 with no ✗ errors.

Read first (fully): `bible.md` (characters, voices, level-mixing rules), `{PARTFILE}` (the outline for this episode and its neighbours), `notes/continuity.md`, the previous episode's source `{PREV}` (continue directly from it; also the format + quality reference), and the docstring of `tools/build_episode.py` (source format).

Requirements:
- Exactly 120 turns. One turn = one speaker's line. Never the same speaker twice in a row (even across scene breaks).
- Follow the outline's scenes and approximate turn ranges for this episode (±5 per scene OK), its 핵심 표현 (use each of the four key sentences verbatim somewhere in the dialogue), and its 엔딩 훅. If the outline contradicts established continuity, continuity wins; note the deviation in your report.
- Level tags A1/A2/B1/B2 must honestly reflect the Swedish sentence difficulty. Mix levels within scenes (not in blocks). Target for this part per episode: {TARGET} (validator allows ±6; aim within ±2).
- Natural, correct, idiomatic contemporary Swedish (Stockholm speech for Linnea/Ida/Maggan; Ahmed uses suburb slang like "walla", "len", "aa", "typ"; Oskar terse Norrland "Jo."/"Nä."; Britt Norrland dialect touches). Double-check grammar: en/ett gender, adjective agreement, V2 word order, subordinate-clause negation placement, definite forms.
- Korean translation on every turn: natural spoken Korean matching personality and the politeness rules in continuity notes (번역 규칙).
- Stage directions, if needed, go inside the Korean translation in parentheses. Do not add extra fields.
- Header: @title "{P}부 {E}화 — <Swedish title>", @subtitle "(<Korean title>)", @meta rows 날짜, 장소, 등장인물, @intro lines: short "지난 이야기" recap of the previous episode + scene-setting paragraph.
- Footer after `@@footer`: "## 이번 화의 표현" table (8–10 rows: 레벨|표현|뜻|포인트), "## 문화 메모" (2–4 accurate bullets about Sweden), "## 다음 화 예고 — {NEXT}" teaser consistent with the outline (for a part's final episode, preview the next part's first episode; for the series finale, write "## 시리즈를 마치며" instead).
- Stay consistent with continuity notes; pick up open threads. New small details are fine but must be recorded.

After the build passes, append "### {P}부 {E}화" to `notes/continuity.md` with 4–8 bullets of new facts later episodes must respect.

Finally report briefly: build distribution line, scene ranges, continuity bullets added, any outline deviations.
