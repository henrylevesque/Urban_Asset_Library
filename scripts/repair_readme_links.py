"""
Attempt to repair broken relative links in subfolder README.md files.
- For each broken relative link, search the repo for files with the same basename (case-insensitive).
- If a single candidate is found, update the README to point to that file (relative path from the README folder).
- If multiple or zero candidates are found, create a `README.broken_links.md` in the same folder listing unresolved links.

Backups: original README.md.bak should exist from previous standardization run. This script will overwrite README.md in place (but keeps README.md.bak).

Run with:
C:/Users/leves/Nextcloud/GitHub/Urban_Asset_Library/.venv/Scripts/python.exe scripts\repair_readme_links.py
"""
from pathlib import Path
import re
from collections import defaultdict

repo_root = Path(__file__).resolve().parent.parent
exclude_paths = {repo_root / 'README.md', repo_root / 'docs' / 'README.md'}

link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Build a map of lowercase basenames to matching file paths in the repo
file_index = defaultdict(list)
for p in repo_root.rglob('*'):
    if p.is_file():
        file_index[p.name.lower()].append(p)

summary = {
    'checked': 0,
    'fixed': 0,
    'reports': 0,
}

for readme in sorted(repo_root.rglob('README.md')):
    if readme.resolve() in exclude_paths:
        continue
    if readme.parent == repo_root:
        continue
    summary['checked'] += 1
    folder = readme.parent
    text = readme.read_text(encoding='utf-8')
    matches = link_re.findall(text)
    if not matches:
        continue
    updated = False
    broken_links = []
    for full_text, link in matches:
        # skip external and anchors
        if link.startswith('http://') or link.startswith('https://') or link.startswith('#'):
            continue
        link_path = link.split(' ')[0].split('#')[0].split('?')[0]
        if link_path.endswith('/'):
            # directory link — check exists
            if (folder / link_path.rstrip('/')).exists():
                continue
            else:
                broken_links.append(link)
                continue
        target = (folder / link_path)
        if target.exists():
            continue
        # attempt repair by basename
        candidate_basename = Path(link_path).name.lower()
        candidates = file_index.get(candidate_basename, [])
        if not candidates:
            broken_links.append(link)
            continue
        if len(candidates) == 1:
            candidate = candidates[0]
            # compute relative path from folder to candidate
            rel = candidate.relative_to(folder)
            # replace the link in text
            old = f']({link})'
            new = f']({rel.as_posix()})'
            text = text.replace(old, new)
            updated = True
            summary['fixed'] += 1
        else:
            # multiple candidates — try to pick one in same top-level area
            # prefer candidate in same immediate subfolder or same category
            chosen = None
            for c in candidates:
                # prefer same folder name if possible
                if c.parent == folder:
                    chosen = c
                    break
            if not chosen:
                # prefer candidate under same top-level category (first part of path)
                folder_parts = folder.parts
                for c in candidates:
                    if len(c.parts) > 1 and c.parts[0] in folder_parts:
                        chosen = c
                        break
            if chosen:
                rel = chosen.relative_to(folder)
                old = f']({link})'
                new = f']({rel.as_posix()})'
                text = text.replace(old, new)
                updated = True
                summary['fixed'] += 1
            else:
                broken_links.append(link)
    if updated:
        readme.write_text(text, encoding='utf-8')
    if broken_links:
        report = folder / 'README.broken_links.md'
        report_lines = [f"# Broken links for {folder.name}\n"]
        report_lines.append('The following relative links in `README.md` could not be resolved automatically:')
        for b in broken_links:
            report_lines.append(f'- {b}')
        report_text = '\n'.join(report_lines)
        report.write_text(report_text, encoding='utf-8')
        summary['reports'] += 1

print('Repair summary:')
print(f"- README files checked: {summary['checked']}")
print(f"- Links auto-fixed: {summary['fixed']}")
print(f"- Broken-link reports created: {summary['reports']}")

print('\nReports are saved as README.broken_links.md and are ignored by .gitignore.')
