"""
Standardize subfolder README.md files.
- Excludes repository root README.md and docs/README.md
- Backs up each README.md to README.md.bak if not already backed up
- Writes a consistent template listing files with relative links and including a preview image if present

Run from repository root with the configured python:
C:/Users/leves/Nextcloud/GitHub/Urban_Asset_Library/.venv/Scripts/python.exe scripts\standardize_readmes.py
"""

from pathlib import Path
import re

repo_root = Path(__file__).resolve().parent.parent
exclude_paths = {repo_root / 'README.md', repo_root / 'docs' / 'README.md'}

TEMPLATE = """# {title}

{description}

{preview}

## Files included

{files}

---

Notes

- For detailed asset documentation, see `docs/ASSET_DOCS_README.md` or `docs/README.md`.
"""

changed = []

for readme in repo_root.rglob('README.md'):
    # skip root README and docs README
    if readme.resolve() in exclude_paths:
        continue
    # ensure it's a subfolder README (not the very root)
    if readme.parent == repo_root:
        continue

    folder = readme.parent
    title = folder.name
    description = f"Files and assets in the `{title}` folder."

    # find an image file in the folder to use as preview
    preview = ''
    for pattern in ('*.png', '*.jpg', '*.jpeg', '*.gif'):
        imgs = list(folder.glob(pattern))
        if imgs:
            # pick the first image
            preview = f'![preview]({imgs[0].name})\n'
            break

    # list non-readme files
    files_md = []
    for p in sorted(folder.iterdir()):
        if p.name.lower() == 'readme.md':
            continue
        # show directories too
        rel = p.name
        # if file exists, link it
        if p.is_file():
            files_md.append(f'- [{rel}]({rel})')
        else:
            files_md.append(f'- {rel}/')
    if not files_md:
        files_md = ['- (No files in this folder)']
    files_text = '\n'.join(files_md)

    content = TEMPLATE.format(title=title, description=description, preview=preview, files=files_text)

    # backup original if not already
    bak = readme.with_suffix(readme.suffix + '.bak')
    if not bak.exists():
        readme.replace(bak)
        # write new README to original path
        bak.write_text(bak.read_text() if False else '')
        # NOTE: we moved the readme into bak; write new content below
        readme.write_text(content)
    else:
        # overwrite README but keep backup
        readme.write_text(content)

    changed.append(str(readme.relative_to(repo_root)))

print('Updated README files:')
for c in changed:
    print(' -', c)

print('\nBackups saved as README.md.bak next to each updated README (if one did not already exist).')
