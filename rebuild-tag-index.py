#!/usr/bin/env python3
"""Regenerate tag-index.md from all note files.
Called automatically by .git/hooks/pre-commit on every commit."""

import re
from pathlib import Path
from collections import defaultdict

notes_dir = Path(__file__).parent

VALID_TAG = re.compile(r'^[가-힣A-Za-z0-9_-]+$')

def extract_valid_tags(text):
    bt   = re.findall(r'`#([^`]+)`', text)
    bare = re.findall(r'(?:^|\s)#([가-힣A-Za-z0-9_-]+)', text)
    return [t for t in (bt + bare) if VALID_TAG.match(t)]

ENTRY_NOTES = {
    # design-pattern
    "design-pattern-behavioral":              "디자인 패턴 (행위)",
    "design-pattern-creational-structural":   "디자인 패턴 (생성·구조)",
    "design-pattern-architecture":            "디자인 패턴 (아키텍처)",
    # software-principle
    "software-principle-simplicity":          "소프트웨어 원칙 (단순성)",
    "software-principle-design":              "소프트웨어 원칙 (설계)",
    "software-principle-quality-laws":        "소프트웨어 원칙 (코드품질·법칙)",
    # math-algorithm
    "math-algorithm-interpolation":           "수학/알고리즘 (보간·변환)",
    "math-algorithm-probability":             "수학/알고리즘 (확률·통계)",
    "math-algorithm-spatial-algo":            "수학/알고리즘 (공간·알고리즘)",
    # game-technique
    "game-technique-mechanics":               "게임 기법 (게임필·시각)",
    "game-technique-combat":                  "게임 기법 (전투·수치)",
    "game-technique-systems":                 "게임 기법 (시스템·아키텍처)",
    # game-design
    "game-design-gameplay":                   "게임 디자인 (게임필·UX)",
    "game-design-systems":                    "게임 디자인 (시스템·밸런싱)",
    # game-misc
    "game-misc-ui-rendering":                 "게임 잡기술 (UI·렌더링)",
    "game-misc-architecture-data":            "게임 잡기술 (아키텍처·데이터)",
    # unity-feature
    "unity-feature-core":                     "Unity 기능 (코어·라이프사이클)",
    "unity-feature-ui":                       "Unity 기능 (UI 시스템)",
    "unity-feature-misc":                     "Unity 기능 (오디오·렌더링·에디터)",
    # csharp-syntax (category-based, ### N. headings)
    "csharp-syntax-type-null-pattern":        "C# 문법 (타입·null·패턴)",
    "csharp-syntax-generic-expression-type":  "C# 문법 (제네릭·표현식·자료형)",
    "csharp-syntax-async-infra-collection":   "C# 문법 (비동기·인프라·컬렉션)",
}

# matches both ## N. and ### N. headings (for csharp-syntax with ### N.)
HEADING_RE  = re.compile(r'^#{2,3} ([\d~, ]+)\. (.+)$')
BTAG_START  = re.compile(r'^`#')
BARE_TAG_RE = re.compile(r'^#[가-힣A-Za-z]')

tag_to_entries = defaultdict(list)

for note_name, display in ENTRY_NOTES.items():
    path = notes_dir / f"{note_name}.md"
    if not path.exists():
        continue
    lines = path.read_text(encoding='utf-8').split('\n')
    in_fullnote = in_code = False
    current = None

    for line in lines:
        if line.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.strip() == '# 풀노트':
            in_fullnote = True
            continue
        if in_fullnote and re.match(r'^# [^#]', line):
            in_fullnote = False
            continue

        if in_fullnote:
            m = HEADING_RE.match(line)
            if m:
                num, title = m.group(1).strip(), m.group(2).strip()
                current = {'heading': f"{num}. {title}", 'title': title}
                continue

            is_tag = (BTAG_START.match(line) or
                      (BARE_TAG_RE.match(line) and not line.startswith('## ')))
            if is_tag and current:
                for t in extract_valid_tags(line):
                    tag_to_entries[f'#{t}'].append({
                        'note': note_name, 'display': display,
                        'heading': current['heading'], 'title': current['title'],
                    })

# idea-notes: tags from index table (dispatcher), links → sub-files
IDEA_SUB = {
    **{n: 'idea-notes-architecture' for n in range(1, 21)},
    **{n: 'idea-notes-principles'   for n in range(21, 28)},
    **{n: 'idea-notes-unity-tools'  for n in range(28, 44)},
}
IDEA_DISPLAY = {
    'idea-notes-architecture': '아이디어 (아키텍처·패턴)',
    'idea-notes-principles':   '아이디어 (법칙·원칙·테스트)',
    'idea-notes-unity-tools':  '아이디어 (Unity·도구·메타)',
}

idea_path = notes_dir / "idea-notes.md"
if idea_path.exists():
    for line in idea_path.read_text(encoding='utf-8').split('\n'):
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 6:
            continue
        num_str = parts[1]
        if not num_str.isdigit():
            continue
        num = int(num_str)
        title = parts[2].strip()
        note_file = IDEA_SUB.get(num, 'idea-notes')
        display = IDEA_DISPLAY.get(note_file, '아이디어')
        heading = f"{num_str}. {title}"
        for t in extract_valid_tags(parts[3]) + extract_valid_tags(parts[5]):
            tag_to_entries[f'#{t}'].append({
                'note': note_file, 'display': display,
                'heading': heading, 'title': title,
            })

# Generate tag-index.md
sorted_tags = sorted(tag_to_entries.keys())
total = sum(len(v) for v in tag_to_entries.values())

out = [
    "# 태그 인덱스",
    "",
    f"> 전체 태그 **{len(sorted_tags)}개** · 항목 링크 **{total}개**  ",
    "> pre-commit hook이 커밋 시 자동 갱신.",
    "",
    "---",
    "",
]
for tag in sorted_tags:
    out.append(f"## {tag}")
    out.append("")
    for e in tag_to_entries[tag]:
        link = f"[[{e['note']}#{e['heading']}|{e['title']}]]"
        out.append(f"- {link} · _{e['display']}_")
    out.append("")

(notes_dir / "tag-index.md").write_text('\n'.join(out), encoding='utf-8')
print(f"tag-index.md rebuilt: {len(sorted_tags)} tags, {total} links")
