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
    "design-pattern-notes": "디자인 패턴",
    "software-principle-notes": "소프트웨어 원칙",
    "math-algorithm-notes": "수학/알고리즘",
    "game-technique-notes": "게임 기법",
    "game-design-notes": "게임 디자인",
    "game-misc-notes": "게임 잡기술",
    "unity-feature-notes": "Unity 기능",
}

HEADING_RE  = re.compile(r'^## ([\d~, ]+)\. (.+)$')
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

# idea-notes: tags from index table (no per-entry tag lines)
idea_path = notes_dir / "idea-notes.md"
if idea_path.exists():
    idea_content = idea_path.read_text(encoding='utf-8')
    full_heads = {}
    in_items = False
    for line in idea_content.split('\n'):
        if '## 항목별 노트' in line:
            in_items = True
            continue
        if in_items:
            m = re.match(r'^## (\d+)\. (.+)$', line)
            if m:
                full_heads[m.group(1)] = m.group(2).strip()
    for line in idea_content.split('\n'):
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 7:
            continue
        num = parts[1]
        if not num.isdigit() or num not in full_heads:
            continue
        title   = full_heads[num]
        heading = f"{num}. {title}"
        for t in extract_valid_tags(parts[3]) + extract_valid_tags(parts[5]):
            tag_to_entries[f'#{t}'].append({
                'note': 'idea-notes', 'display': '아이디어',
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
