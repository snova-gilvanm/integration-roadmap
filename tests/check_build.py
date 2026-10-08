"""Regression check: build.py must rebuild the maintenance data that is on the published page.

Usage (from the repo root):  python3 tests/check_build.py
Reads artifact/index.html (the last published page), reconstructs build.py's inputs from its data
block, runs build.py, and compares D.maint (cadence, stages, templates, every asset) with the page.
Run it after changing any MAINT_* map or template, then update artifact/index.html when you publish.
"""
import json, os, re, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, '.claude', 'skills', 'integration-backlog-monitor-v2')
html = open(os.path.join(ROOT, 'artifact', 'index.html'), encoding='utf-8').read()
D = json.loads(re.search(r'id="data">(.*?)</script>', html, re.S).group(1).replace('<\\/', '</'))
work = tempfile.mkdtemp()
raw = lambda g: dict(slug=g['slug'], title=g['name'], group=g['group'], sub=g['sub'], blurb=g['blurb'], intro=g['intro'],
                     links=[g['home']] if g.get('home') else [], surface=g.get('langs', []), upd=g['upd'], age=g['age'],
                     ja=g['ja'], jaUpd=g['jaUpd'], latest=g['latest'], lines=g['lines'])
json.dump(dict(latest=D['latest'], guides=[raw(g) for g in D['guides']], review=[raw(g) for g in D['review']]), open(f'{work}/guides.json', 'w'))
keys = ['key', 'summary', 'status', 'owner', 'ownerOff', 'created', 'resolved', 'due', 'slot', 'labels', 'itype']
json.dump([{k: t.get(k) for k in keys} for t in D['tickets']], open(f'{work}/jira.json', 'w'))
json.dump([], open(f'{work}/jira_desc.json', 'w'))
json.dump(D['trending'], open(f'{work}/trending.json', 'w'))
env = dict(os.environ, WORK=work, SNAPSHOT=D['maint']['generated'])
subprocess.run([sys.executable, os.path.join(SKILL, 'scripts', 'build.py')], env=env, check=True, stdout=subprocess.DEVNULL)
a, b = json.load(open(f'{work}/data.json'))['maint'], D['maint']
problems = [k for k in ('cadence', 'stages', 'templates') if a.get(k) != b.get(k)]
A, B = {x['id']: x for x in a['assets']}, {x['id']: x for x in b['assets']}
if set(A) != set(B): problems.append(f'asset ids differ: only build {sorted(set(A)-set(B))}, only page {sorted(set(B)-set(A))}')
for i in set(A) & set(B):
    for k in set(A[i]) | set(B[i]):
        if A[i].get(k) != B[i].get(k): problems.append(f'{i}.{k}: build={A[i].get(k)!r} page={B[i].get(k)!r}')
print('OK: build.py reproduces the page\'s maintenance data' if not problems else 'MISMATCH:\n  ' + '\n  '.join(problems[:20]))
sys.exit(1 if problems else 0)
