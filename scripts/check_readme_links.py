"""Check relative links in subfolder README.md files (excluding repo root and docs README).

Prints a summary of files checked and any broken links found.

Run with the repo's python:
C:/Users/leves/Nextcloud/GitHub/Urban_Asset_Library/.venv/Scripts/python.exe scripts\check_readme_links.py
"""

from pathlib import Path
import re

repo_root = Path(__file__).resolve().parent.parent
exclude_paths = {repo_root / 'README.md', repo_root / 'docs' / 'README.md'}

# find markdown links like [text](path) or ![alt](path)
link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

results = []

for readme in sorted(repo_root.rglob('README.md')):
    if readme.resolve() in exclude_paths:
        continue
    if readme.parent == repo_root:
        continue
    folder = readme.parent
    text = readme.read_text(encoding='utf-8')
    matches = link_pattern.findall(text)
    # matches is a list of tuples (text, link)
    links = [m[1] for m in matches]
    broken = []
    for link in links:
        # ignore absolute URLs and anchors
        if link.startswith('http://') or link.startswith('https://') or link.startswith('#'):
            continue
        # remove optional title after space and fragments/queries
        link_path = link.split(' ')[0].split('#')[0].split('?')[0]
        # treat directory links (ending with /) as OK if directory exists
        if link_path.endswith('/'):
            if not (folder / link_path.rstrip('/')).exists():
                broken.append(link)
            continue
        target = (folder / link_path)
        if not target.exists():
            broken.append(link)
    results.append((str(readme.relative_to(repo_root)), broken))

# print summary
total = len(results)
print(f'Checked {total} subfolder README.md files for link validity.\n')
any_broken = False
for path, broken in results:
    if broken:
        any_broken = True
        print(f'- {path}: {len(broken)} broken link(s)')
        for b in broken:
            print(f'    - {b}')

if not any_broken:
    print('No broken relative links found in subfolder README.md files.')
else:
    print('\nPlease review the above README files to correct or remove the broken links.')
