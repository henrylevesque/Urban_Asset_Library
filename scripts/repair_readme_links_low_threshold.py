"""
Low-threshold repair: auto-apply top candidate when it's in the same folder or confidence >= 0.5.
Writes `README.applied_fixes.md` summarizing applied changes per folder.

Run with:
C:/Users/leves/Nextcloud/GitHub/Urban_Asset_Library/.venv/Scripts/python.exe scripts\repair_readme_links_low_threshold.py
"""
from pathlib import Path
import re
from collections import defaultdict
import difflib

repo_root = Path(__file__).resolve().parent.parent
exclude_paths = {repo_root / 'README.md', repo_root / 'docs' / 'README.md'}

link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Build file index
all_files = [p for p in repo_root.rglob('*') if p.is_file()]
basename_map = defaultdict(list)
for p in all_files:
    basename_map[p.name.lower()].append(p)

summary = {'checked':0,'fixed':0,'reports':0}

def path_similarity(a:Path, b:Path)->int:
    a_parts = list(a.parts)
    b_parts = list(b.parts)
    score = 0
    for x,y in zip(reversed(a_parts), reversed(b_parts)):
        if x.lower() == y.lower():
            score += 1
        else:
            break
    return score

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
    applied = []
    unresolved = []
    for full_text, link in matches:
        if link.startswith('http://') or link.startswith('https://') or link.startswith('#'):
            continue
        link_path = link.split(' ')[0].split('#')[0].split('?')[0]
        if link_path.endswith('/'):
            if (folder / link_path.rstrip('/')).exists():
                continue
            else:
                unresolved.append(link)
                continue
        target = (folder / link_path)
        if target.exists():
            continue
        candidate_basename = Path(link_path).name.lower()
        direct_candidates = basename_map.get(candidate_basename, [])
        chosen = None
        confidence = 0.0
        if direct_candidates:
            # if one candidate in same folder, pick it
            same_folder = [c for c in direct_candidates if c.parent == folder]
            if len(same_folder) == 1:
                chosen = same_folder[0]
                confidence = 0.95
            else:
                # prefer same folder if multiple
                if same_folder:
                    chosen = same_folder[0]
                    confidence = 0.9
                else:
                    # pick best by path similarity
                    scored = [(path_similarity(folder, c), c) for c in direct_candidates]
                    scored.sort(reverse=True)
                    best_score, best_path = scored[0]
                    chosen = best_path
                    confidence = 0.6 + (best_score * 0.05)
        else:
            # fuzzy candidates
            all_basenames = list(basename_map.keys())
            matches_close = difflib.get_close_matches(candidate_basename, all_basenames, n=5, cutoff=0.4)
            candidates = []
            for mb in matches_close:
                candidates.extend(basename_map[mb])
            if candidates:
                scored = []
                for c in candidates:
                    name_sim = difflib.SequenceMatcher(None, candidate_basename, c.name.lower()).ratio()
                    path_sim = path_similarity(folder, c)
                    score = name_sim * 0.7 + (path_sim * 0.1)
                    scored.append((score, c))
                scored.sort(reverse=True)
                best_score, best_path = scored[0]
                chosen = best_path
                confidence = best_score
        # decision: apply if chosen in same folder OR confidence >= 0.5
        apply_change = False
        if chosen:
            if chosen.parent == folder:
                apply_change = True
            elif confidence >= 0.5:
                apply_change = True
        if apply_change:
            try:
                rel = chosen.relative_to(folder)
            except Exception:
                # fallback to absolute path relative to repo
                rel = chosen
            old = f']({link})'
            new = f']({rel.as_posix()})'
            text = text.replace(old, new)
            updated = True
            applied.append((link, rel.as_posix(), confidence, str(chosen)))
            summary['fixed'] += 1
        else:
            unresolved.append(link)
    if updated:
        readme.write_text(text, encoding='utf-8')
        # write applied fixes report
        report = folder / 'README.applied_fixes.md'
        lines = [f"# Applied fixes for {folder.name}\n", 'The following link replacements were applied:']
        for orig, rel, conf, full in applied:
            lines.append(f'- {orig} -> {rel} (confidence: {conf:.2f}, source: {full})')
        report.write_text('\n'.join(lines), encoding='utf-8')
        summary['reports'] = summary.get('reports',0) + 1
    if unresolved:
        # write or update broken links report
        report = folder / 'README.broken_links.md'
        report_lines = [f"# Broken links for {folder.name}\n"]
        report_lines.append('The following relative links in `README.md` could not be resolved automatically:')
        for b in unresolved:
            report_lines.append(f'- {b}')
        report.write_text('\n'.join(report_lines), encoding='utf-8')

print('Low-threshold repair summary:')
print(f"- README files checked: {summary['checked']}")
print(f"- Links auto-fixed: {summary['fixed']}")
print(f"- Applied-fixes reports created: {summary.get('reports',0)}")
