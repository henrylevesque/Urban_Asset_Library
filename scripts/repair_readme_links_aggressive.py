"""
Aggressive repair for broken relative links in subfolder README.md files.
- Uses fuzzy basename matching (difflib) and path-similarity heuristics.
- If a candidate meets a confidence threshold, the README link is updated.
- Otherwise, a `README.repair_suggestions.md` is created containing ranked suggestions, and `README.broken_links.md` is written for unresolved links.

Run with:
C:/Users/leves/Nextcloud/GitHub/Urban_Asset_Library/.venv/Scripts/python.exe scripts\repair_readme_links_aggressive.py
"""
from pathlib import Path
import re
from collections import defaultdict
import difflib

repo_root = Path(__file__).resolve().parent.parent
exclude_paths = {repo_root / 'README.md', repo_root / 'docs' / 'README.md'}

link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Build a list of all candidate files (excluding README.broken_links.md and backups)
all_files = [p for p in repo_root.rglob('*') if p.is_file() and p.name not in ('README.broken_links.md','README.repair_suggestions.md')]
# map lowercase basename to list of paths
basename_map = defaultdict(list)
for p in all_files:
    basename_map[p.name.lower()].append(p)

summary = {'checked':0,'fixed':0,'suggestions':0}

# helper to compute path similarity score
def path_similarity(a:Path, b:Path)->int:
    # count common trailing parts
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
    broken_links = []
    suggestions_report = []
    for full_text, link in matches:
        if link.startswith('http://') or link.startswith('https://') or link.startswith('#'):
            continue
        link_path = link.split(' ')[0].split('#')[0].split('?')[0]
        if link_path.endswith('/'):
            if (folder / link_path.rstrip('/')).exists():
                continue
            else:
                broken_links.append(link)
                continue
        target = (folder / link_path)
        if target.exists():
            continue
        candidate_basename = Path(link_path).name.lower()
        direct_candidates = basename_map.get(candidate_basename, [])
        chosen = None
        confidence = 0.0
        # exact basename match found elsewhere
        if direct_candidates:
            if len(direct_candidates) == 1:
                chosen = direct_candidates[0]
                confidence = 0.9
            else:
                # pick best by path similarity
                scored = [(path_similarity(folder, c), c) for c in direct_candidates]
                scored.sort(reverse=True)
                best_score, best_path = scored[0]
                chosen = best_path
                confidence = 0.75 + (best_score * 0.05)
        else:
            # fuzzy match basenames
            all_basenames = list(basename_map.keys())
            matches_close = difflib.get_close_matches(candidate_basename, all_basenames, n=5, cutoff=0.6)
            if matches_close:
                # gather candidate paths for each basename
                candidates = []
                for mb in matches_close:
                    candidates.extend(basename_map[mb])
                # score candidates by combined similarity (difflib ratio + path similarity)
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
        # decide whether to apply
        if chosen and confidence >= 0.7:
            rel = chosen.relative_to(folder)
            old = f']({link})'
            new = f']({rel.as_posix()})'
            text = text.replace(old, new)
            updated = True
            summary['fixed'] += 1
        else:
            # compose suggestions (top 3)
            suggestions = []
            # if any direct candidates, include them
            candidate_list = direct_candidates if direct_candidates else []
            if not candidate_list:
                # try fuzzy candidates
                matches_close = difflib.get_close_matches(candidate_basename, list(basename_map.keys()), n=5, cutoff=0.5)
                for mb in matches_close:
                    candidate_list.extend(basename_map[mb])
            # rank and take top 3
            ranked = []
            for c in candidate_list:
                name_sim = difflib.SequenceMatcher(None, candidate_basename, c.name.lower()).ratio()
                path_sim = path_similarity(folder, c)
                ranked.append((name_sim + (path_sim*0.1), c))
            ranked.sort(reverse=True)
            for score, c in ranked[:3]:
                suggestions.append((score, c))
            suggestions_text = []
            for score, c in suggestions:
                try:
                    rel = c.relative_to(folder)
                except Exception:
                    rel = c
                suggestions_text.append(f'- {c} (suggested relative: {rel.as_posix()} , score: {score:.2f})')
            suggestions_report.append((link, suggestions_text))
            broken_links.append(link)
    if updated:
        readme.write_text(text, encoding='utf-8')
    if suggestions_report:
        report = folder / 'README.repair_suggestions.md'
        lines = [f'# Repair suggestions for {folder.name}\n', 'The script could not confidently fix the following links. Suggestions (ranked) follow:']
        for link, sug in suggestions_report:
            lines.append(f'\n**Original link:** {link}')
            lines.extend(sug)
        report.write_text('\n'.join(lines), encoding='utf-8')
        summary['suggestions'] += 1
    if broken_links and not suggestions_report:
        # if there are broken links without suggestions, write broken_links report
        report = folder / 'README.broken_links.md'
        report_lines = [f"# Broken links for {folder.name}\n"]
        report_lines.append('The following relative links in `README.md` could not be resolved automatically:')
        for b in broken_links:
            report_lines.append(f'- {b}')
        report.write_text('\n'.join(report_lines), encoding='utf-8')

print('Aggressive repair summary:')
print(f"- README files checked: {summary['checked']}")
print(f"- Links auto-fixed: {summary['fixed']}")
print(f"- Suggestion reports created: {summary['suggestions']}")
