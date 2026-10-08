import os, sys, json, re, datetime
WORK = os.environ.get("WORK", ".").rstrip("/") + "/"
REPO = os.environ.get("REPO", "")
SNAP = os.environ.get("SNAPSHOT") or datetime.date.today().isoformat()
TODAY = datetime.date.fromisoformat(SNAP)
import collections
B = WORK

G = json.load(open(B + 'guides.json'))
JD = {j['key']: j for j in json.load(open(B + 'jira_desc.json'))}

# ---------- published guides: curated mode / interface / homepage ----------
# vendor = built-in provider, package = SambaNova package, compat = OpenAI-compatible, commercial = marketplace/network
OLDKIND = {"adk":"compat","agentzero":"vendor","agno":"compat","aisuite":"vendor","autogen":"compat","aws":"commercial","aws-marketplace":"commercial","blackboxai":"compat","browser-use":"compat","camel-ai":"compat","claude-code":"compat","cline":"compat","codex":"compat","composio":"compat","continue":"vendor","crew-ai":"vendor","cursor":"compat","datarobot":"compat","dify":"vendor","docker-compose-agents":"compat","elevenlabs":"compat","exa":"compat","fastmcp":"compat","flowise":"package","google-workspace":"compat","gradio":"package","haystack":"compat","hugging-face":"vendor","humeai":"vendor","inspectai":"compat","instructor":"compat","kilocode":"vendor","langchain":"package","langflow":"compat","langgraph":"package","librechat":"compat","linkup":"package","litellm":"vendor","livekit":"compat","llama-index":"package","lm-evalharness":"compat","make":"compat","mem0":"compat","milvus":"package","n8n":"compat","neo4j":"compat","ogx":"compat","open-worker":"compat","openclaw":"compat","opencode":"compat","openhands":"compat","openrouter-byok":"vendor","openwebui":"compat","oumi":"vendor","pi":"compat","pipecat":"package","qwen-code-cli":"compat","roocode":"vendor","semantic-kernel":"compat","term-llm":"vendor","twelvelabs":"compat","vapi":"package","vercel":"package","vscode":"compat","weave":"package"}
K2M = {'vendor': 'native', 'package': 'sdk', 'compat': 'openai', 'commercial': 'commercial'}
MODE_OVR = {'claude-code': ['anthropic'], 'langfuse': ['openai'], 'langsmith': ['openai'], 'zapier': ['app']}
HOME = {"camel-ai":"https://www.camel-ai.org/","langgraph":"https://www.langchain.com/langgraph","litellm":"https://www.litellm.ai/","llama-index":"https://www.llamaindex.ai/","mem0":"https://mem0.ai/","n8n":"https://n8n.io/","pipecat":"https://www.pipecat.ai/","qwen-code-cli":"https://github.com/QwenLM/qwen-code","roocode":"https://roocode.com/","vapi":"https://vapi.ai/","crew-ai":"https://www.crewai.com/","aws":"https://aws.amazon.com/privatelink/","aws-marketplace":"https://aws.amazon.com/marketplace/","oumi":"https://oumi.ai/","adk":"https://google.github.io/adk-docs/","browser-use":"https://browser-use.com/","docker-compose-agents":"https://github.com/docker/compose-for-agents","fastmcp":"https://gofastmcp.com/","gradio":"https://www.gradio.app/","google-workspace":"https://workspace.google.com/","langchain":"https://www.langchain.com/","pi":"https://pi.dev/","weave":"https://wandb.ai/site/weave/","vercel":"https://ai-sdk.dev/","agno":"https://www.agno.com/","claude-code":"https://www.claude.com/product/claude-code","agentzero":"https://www.agent-zero.ai/","codex":"https://github.com/openai/codex","exa":"https://exa.ai/","aisuite":"https://github.com/andrewyng/aisuite","open-worker":"https://github.com/andrewyng/openworker","vscode":"https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio","hugging-face":"https://huggingface.co/","inspectai":"https://inspect.aisi.org.uk/","lm-evalharness":"https://github.com/EleutherAI/lm-evaluation-harness","ogx":"https://ogx-ai.github.io/docs","term-llm":"https://term-llm.com/","semantic-kernel":"https://learn.microsoft.com/en-us/semantic-kernel/","instructor":"https://python.useinstructor.com/","autogen":"https://microsoft.github.io/autogen/stable/","haystack":"https://haystack.deepset.ai/","linkup":"https://www.linkup.so/","milvus":"https://milvus.io/","neo4j":"https://neo4j.com/","twelvelabs":"https://www.twelvelabs.io/","livekit":"https://livekit.io/","elevenlabs":"https://elevenlabs.io/","humeai":"https://www.hume.ai/","openrouter-byok":"https://openrouter.ai/","openwebui":"https://openwebui.com/","librechat":"https://www.librechat.ai/","opencode":"https://opencode.ai/","openclaw":"https://openclaw.ai/","openhands":"https://www.openhands.dev/","make":"https://www.make.com/","composio":"https://composio.dev/","cline":"https://cline.bot/","continue":"https://www.continue.dev/","cursor":"https://cursor.com/","kilocode":"https://kilocode.ai/","blackboxai":"https://www.blackbox.ai/","dify":"https://dify.ai/","datarobot":"https://www.datarobot.com/","flowise":"https://flowiseai.com/","langflow":"https://www.langflow.org/","langfuse":"https://langfuse.com/","langsmith":"https://www.langchain.com/langsmith","zapier":"https://zapier.com/"}
CLI = {'claude-code','codex','opencode','qwen-code-cli','pi','term-llm','openclaw','aider'}
IDE = {'cline','continue','cursor','kilocode','roocode','vscode','blackboxai','jetbrains','windsurf'}
def iface_of(slug, group, sub):
    if slug in CLI: return 'cli'
    if slug in IDE: return 'ide'
    if slug in ('aws', 'aws-marketplace'): return 'cloud'
    if group == 'Interfaces and low-code' or slug in ('openhands','agentzero','open-worker','dify','elevenlabs','humeai','vapi','make','n8n','flowise','langflow','datarobot','langfuse','zapier','google-workspace','openrouter-byok'): return 'nocode'
    return 'code'

def guide_rec(g, state):
    s = g['slug']
    modes = MODE_OVR.get(s) or [K2M[OLDKIND.get(s, 'compat')]]
    home = HOME.get(s) or (g['links'][0] if g['links'] else None)
    grp = g['group'] or ('Evaluation and monitoring' if s in ('langfuse','langsmith') else 'Interfaces and low-code' if s=='zapier' else None)
    sub = g['sub'] or ('Observability' if s in ('langfuse','langsmith') else 'Low-code platforms' if s=='zapier' else None)
    return dict(slug=s, name=g['title'], group=grp, sub=sub, blurb=g['blurb'], intro=g['intro'],
                home=home, modes=modes, iface=iface_of(s, grp, sub), langs=g['surface'], upd=g['upd'], age=g['age'],
                ja=g['ja'], jaUpd=g['jaUpd'], latest=g['latest'], lines=g['lines'], state=state)
guides = [guide_rec(g, 'live') for g in G['guides']]
review = {g['slug']: guide_rec(g, 'review') for g in G['review']}

# ---------- Jira ----------
rows = json.load(open(B + 'jira.json'))   # [{key,summary,status,owner,ownerOff,created,resolved,due,slot,labels,itype}]

SLOT_META = {
 'int-oct-2026': ('Oct 2026', '2026-10-01', '2026-10-31'),
 'int-nov-2026': ('Nov 2026', '2026-11-01', '2026-11-30'),
 'int-dec-2026': ('Dec 2026', '2026-12-01', '2026-12-31'),
 'int-q1-2027': ('Q1 2027', '2027-01-01', '2027-03-31'),
 'int-q2-2027': ('Q2 2027', '2027-04-01', '2027-06-30')}

# curated plan metadata for the slotted roadmap: slug, category, modes, iface, door (from each ticket description only)
PLAN = {
 'CP-3074': ('langfuse','Evaluation and monitoring',['openai'],'nocode','open'),
 'CP-3075': ('langsmith','Evaluation and monitoring',['openai'],'nocode','open'),
 'CP-3076': ('zapier','Interfaces and low-code',['app'],'nocode','decision'),
 'CP-3077': ('azure-ai-foundry','Hyperscalers and data platforms',['openai'],'cloud','open'),
 'CP-3078': ('salesforce','Enterprise platforms',['partner'],'partner','partner'),
 'CP-3079': ('pinecone','Vector DB and search',['closed'],'code','closed'),
 'CP-3080': ('qdrant','Vector DB and search',['openai'],'code','open'),
 'CP-3081': ('weaviate','Vector DB and search',['openai'],'code','open'),
 'CP-3082': ('chroma','Vector DB and search',['openai'],'code','open'),
 'CP-3083': ('pgvector','Vector DB and search',['cookbook'],'code','open'),
 'CP-3084': ('ollama','Inference servers',['closed'],'cli','closed'),
 'CP-3085': ('vllm','Inference servers',['openai'],'code','open'),
 'CP-3086': ('vertex-ai','Hyperscalers and data platforms',['partner'],'partner','partner'),
 'CP-3087': ('databricks','Hyperscalers and data platforms',['openai'],'cloud','open'),
 'CP-3088': ('supabase','Vector DB and search',['openai'],'code','open'),
 'CP-3089': ('portkey','Interfaces and low-code',['native'],'nocode','open'),
 'CP-3090': ('voiceflow','Interfaces and low-code',['openai'],'nocode','open'),
 'CP-3091': ('snowflake-cortex','Hyperscalers and data platforms',['closed'],'cloud','closed'),
 'CP-3092': ('deepgram','Voice and contact center',['openai'],'code','open'),
 'CP-3093': ('assemblyai','Voice and contact center',['openai'],'code','open'),
 'CP-3094': ('nemo-guardrails','Safety and guardrails',['openai'],'code','open'),
 'CP-3095': ('llama-guard','Safety and guardrails',['model'],'code','dependency'),
 'CP-3096': ('ragas','Evaluation and monitoring',['openai'],'code','open'),
 'CP-3097': ('deepeval','Evaluation and monitoring',['openai'],'code','open'),
 'CP-3098': ('braintrust','Evaluation and monitoring',['openai'],'nocode','open'),
 'CP-3099': ('salesforce-open-connector','Enterprise platforms',['adapter'],'nocode','adapter'),
 'CP-3100': ('servicenow','Enterprise platforms',['adapter'],'nocode','adapter'),
 'CP-3101': ('dspy','Frameworks',['openai'],'code','open'),
 'CP-3102': ('pydantic-ai','Frameworks',['openai'],'code','open'),
 'CP-3103': ('mastra','Frameworks',['native'],'code','upstream'),
 'CP-3104': ('jetbrains','Developer tools',['openai'],'ide','open'),
 'CP-3105': ('windsurf','Developer tools',['closed'],'ide','closed'),
 'CP-3106': ('aider','Developer tools',['openai'],'cli','open'),
 'CP-3107': ('genesys','Voice and contact center',['partner'],'partner','partner'),
 'CP-3108': ('five9','Voice and contact center',['partner'],'partner','partner'),
 'CP-3109': ('talkdesk','Voice and contact center',['partner'],'partner','closed'),
 'CP-3110': ('azure-catalog','Hyperscalers and data platforms',['partner'],'partner','partner'),
 'CP-3111': ('vertex-model-garden','Hyperscalers and data platforms',['partner'],'partner','partner'),
}
PR = {'CP-3074': 1012, 'CP-3075': 1015, 'CP-3076': 1028}   # open docs PRs per ticket; update from the sambanova/docs PR list

def clean(d):
    d = re.sub(r'<custom[^>]*>(.*?)</custom>', r'\1', d or '')
    return d.strip()
def parse_desc(d):
    d = clean(d)
    urls = []
    for u in re.findall(r'https?://[^\s)\]>"<]+', d):
        u = u.rstrip('.,;')
        if u not in urls: urls.append(u)
    eo = re.search(r'Expected outcome:?\s*(.*?)(?:\n\s*\n|$)', d, re.S)
    deliver = []
    if eo:
        t = eo.group(1).strip().rstrip('.')
        parts = re.split(r',\s*then\s+|\.\s+|,\s+(?=(?:a|an|the|and|plus|named|intro|listing|go|both|models|launch|technical|working|swap|published|external|reference|catalogue|metric|test|custom|proxy|adapter|connector|transformation|optimisation|agent|setup|verified|recommended|requirements|either|cookbook|Edge|voice|time|demo|sample|configuration|Model|listing)\b)', t)
        for x in parts:
            x = re.sub(r'^(and|plus|then)\s+', '', x.strip()).strip().rstrip('.')
            if len(x) > 2: deliver.append(x[0].upper() + x[1:])
    body = re.sub(r'Expected outcome:.*', '', d, flags=re.S)
    body = re.sub(r'Roadmap slot:.*', '', body)
    notes = re.findall(r'(?:^|\n)\s*(?:Note|Dependency):\s*(.*)', body)
    paras = [p.strip() for p in re.split(r'\n\s*\n|\n', body) if p.strip()]
    goal = [p for p in paras if not re.match(r'^https?://', p) and not re.match(r'^(Note|Dependency):', p)]
    return dict(goal=goal[:4], deliver=deliver, urls=urls[:6], notes=notes)

def parse_chk(d):
    # Jira checkboxes come back in markdown as "- [ ] item" / "- [x] item" under "### Stage" headings
    out, cur = [], 'Checklist'
    for line in (d or '').split('\n'):
        h = re.match(r'^#{1,6}\s+(.*)', line)
        if h: cur = h.group(1).strip(); continue
        m = re.match(r'^\s*[-*]\s+\[( |x|X)\]\s+(.*)', line)
        if m:
            g = next((x for x in out if x['g'] == cur), None)
            if not g: g = {'g': cur, 'items': []}; out.append(g)
            g['items'].append({'t': m.group(2).strip(), 'd': m.group(1) != ' '})
    return out or None

def classify(s):
    if re.search(r'partnership', s, re.I): return 'Partnership'
    if re.search(r'listing', s, re.I): return 'Catalog listing'
    if re.search(r'cookbook', s, re.I): return 'Cookbook'
    if re.search(r'mainten|mantain|maintanance|fix|typo|bugs|test|benchmark|validation|move ', s, re.I): return 'Maintenance'
    if re.search(r'brief|POC|showcase|eval', s, re.I): return 'Enablement'
    return 'Integration'

tickets = []
for r in rows:
    meta = PLAN.get(r['key'])
    jd = JD.get(r['key'])
    pd = parse_desc(jd['desc']) if jd else None
    t = dict(r)
    t['labels'] = r.get('labels') or []
    t['itype'] = r.get('itype')
    t['ownerOff'] = bool(r.get('ownerOff'))
    t['type'] = 'Maintenance' if 'maintenance' in t['labels'] else classify(r['summary'])
    if pd: t.update(goal=pd['goal'], deliver=pd['deliver'], urls=pd['urls'], notes=pd['notes'])
    if jd and 'maintenance' in t['labels']:
        c = parse_chk(jd['desc'])
        if c: t['chk'] = c
    if meta:
        slug, cat, modes, iface, door = meta
        t.update(slug=slug, cat=cat, modes=modes, iface=iface, door=door, home=(pd['urls'][0] if pd and pd['urls'] else None))
        if slug in review: t['review'] = True
    if r['key'] in PR: t['pr'] = PR[r['key']]
    if r['key'] == 'CP-3076': t['deliver'] = ['A written recommendation: SambaNova app on the Zapier developer platform, or a request to join the AI step provider list', 'If the app path wins, a chat completion action submitted for Zapier review']
    tickets.append(t)

# link published guides to delivery tickets by name
def norm(x): return re.sub(r'[^a-z0-9]', '', x.lower())
alias = {'vscode': ['vscodeaitoolkit', 'foundry'], 'llama-index': ['llamaindex'], 'milvus': ['zilliz', 'milvus'], 'crew-ai': ['crewai'],
         'langgraph': ['langraph', 'langgraph'], 'lm-evalharness': ['lmevaluationharness'], 'qwen-code-cli': ['qwencode'],
         'roocode': ['roocode'], 'blackboxai': ['blackbox'], 'docker-compose-agents': ['dockercomposeagents'], 'weave': ['weave'], 'aisuite': ['aisuite'],
         'camel-ai': ['camel'], 'open-worker': ['openworker'], 'hugging-face': ['huggingface'], 'openwebui': ['openwebui'],
         'litellm': ['litellm'], 'inspectai': ['inspectai'], 'kilocode': ['kilocode'], 'adk': ['adkintegration'], 'browser-use': ['browseruse']}
for g in guides:
    keys = alias.get(g['slug'], [norm(g['name'])])
    hit = [t['key'] for t in tickets if any(k and k in norm(t['summary']) for k in keys)]
    g['tickets'] = hit[:6]

# delivery history: resolved Done tickets per month, rolling 13 months
hist = collections.Counter()
for t in tickets:
    if t['status'] == 'Done' and t['resolved']:
        hist[t['resolved'][:7]] += 1
months = []
y, m = (TODAY.year - 1, TODAY.month)      # rolling 13 months ending with the snapshot month
while (y, m) <= (TODAY.year, TODAY.month):
    k = f'{y}-{m:02d}'; months.append([k, hist.get(k, 0)])
    m += 1
    if m == 13: y, m = y + 1, 1

# ---------- maintenance inventory (curated; change only with the user's confirmation) ----------
MAINT_CADENCE = {'critical': 2, 'high': 3, 'medium': 6, 'low': 12}   # months; low is an assumption, not agreed
TIER_OF_MODE = {'sdk': 'critical', 'native': 'high', 'openai': 'medium', 'anthropic': 'medium', 'commercial': 'low'}
KIND_OF_MODE = {'sdk': 'SambaNova package', 'native': 'Built-in provider upstream', 'openai': 'Docs guide, OpenAI-compatible',
                'anthropic': 'Docs guide, Anthropic-compatible', 'commercial': 'Marketplace or network'}
NOTE_OF_TIER = {'critical': "Tier inferred from the guide's mode (SambaNova package). Confirm the package or plugin is maintained by SambaNova.",
                'high': "Tier inferred from the guide's mode (built-in provider). Confirm the provider code was contributed and is kept up by SambaNova.",
                'medium': "Docs only: the tool's code belongs to its maintainers. Keep the guide's models, steps and screenshots current.",
                'low': "Procurement or private networking path. Check the listing and links."}
MAINT_TICKETS = {'litellm': ['CP-3170', 'CP-2937', 'CP-2692'], 'term-llm': ['CP-3181'], 'langchain': ['CP-2979', 'CP-2691', 'CP-2293'], 'ogx': ['CP-2961'],
                 'pipecat': ['CP-2652'], 'neo4j': ['CP-2505'], 'openhands': ['CP-2330'], 'aisk': ['CP-2475'],
                 'sdk-client-tests': ['CP-2413']}   # CP-2157 (all integrations) is portfolio-wide and not linked to one asset
MAINT_REPOS = [   # internal repos named in tickets: (id, name, home or None, note)
 ('aisk', 'AI Starter Kit (AISK)', None, 'Named in CP-2475. Repository link not recorded on this page yet.'),
 ('sdk-client-tests', 'SDK client tests', 'https://github.com/snova-jorgep/sdk_client_test', 'Test repository linked from CP-2413 (Stainless tests).')]
MAINT_UPSTREAM = [('goose', 'CP-3008'), ('smolagents', 'CP-3009'), ('Hermes Agent', 'CP-3007'), ('DeerFlow', 'CP-3006')]   # merged upstream, no guide yet
# Jira ticket templates used by the page's "Create in Jira" pop-up. {asset} = asset name, {since} = " since <last maintained date>" or "".
# Every step becomes a "- [ ]" checkbox under its stage heading; keep the four stage keys.
MAINT_STAGES = [['todo', 'To do'], ['progress', 'In progress'], ['review', 'In review'], ['close', 'Before closing']]
MAINT_TEMPLATES = {
 "pkg": {
  "name": "SambaNova package",
  "outcome": "{asset} works with the latest SambaNova models and its dependencies are current, with a new release if anything changed.",
  "steps": {
   "todo": [
    "Read the framework's and {asset}'s changelogs{since}",
    "Check open issues and PRs on the package repo"
   ],
   "progress": [
    "Update dependencies",
    "Run the tests against SambaNova Cloud with current models",
    "Replace deprecated models in code, defaults and examples"
   ],
   "review": [
    "Open a PR and get it reviewed",
    "Check the docs guide (EN and JA) still matches"
   ],
   "close": [
    "Publish a new version if code changed",
    "Record the versions tested in a comment"
   ]
  }
 },
 "upstream": {
  "name": "Provider module upstream",
  "outcome": "the SambaNova provider works with {asset}'s latest release and current SambaNova models, with an upstream PR for anything that broke.",
  "steps": {
   "todo": [
    "Read {asset}'s release notes{since}",
    "Check upstream issues that mention SambaNova"
   ],
   "progress": [
    "Run the provider against SambaNova Cloud on the latest release",
    "Check chat, streaming and tool calling with current models",
    "Update the provider's model list if models changed"
   ],
   "review": [
    "Open an upstream PR for any fix and link it here",
    "Check the docs guide (EN and JA)"
   ],
   "close": [
    "Link the merged PR or note that nothing changed",
    "Record the {asset} version tested"
   ]
  }
 },
 "repo": {
  "name": "Internal repo",
  "outcome": "dependencies, models and examples in {asset} are current and the tests pass.",
  "steps": {
   "todo": [
    "Review open issues and PRs",
    "Check which SambaNova models the code uses"
   ],
   "progress": [
    "Update dependencies",
    "Replace deprecated models",
    "Run the tests or CI and fix failures"
   ],
   "review": [
    "Get the changes reviewed and merged"
   ],
   "close": [
    "Note what changed and the versions tested"
   ]
  }
 },
 "docs": {
  "name": "Docs guide",
  "outcome": "the guide's models, steps, code samples and screenshots match the current version of {asset} and SambaNova Cloud, in English and Japanese.",
  "steps": {
   "todo": [
    "Check {asset}'s release notes for setup or configuration changes{since}"
   ],
   "progress": [
    "Follow the guide end to end with the latest version",
    "Update model names, steps, samples and screenshots"
   ],
   "review": [
    "Open a docs PR and get it reviewed",
    "Update the Japanese guide to match"
   ],
   "close": [
    "Confirm the guide is in the latest docs version",
    "Link the PR or note that nothing changed"
   ]
  }
 },
 "listing": {
  "name": "Marketplace listing",
  "outcome": "the listing's description, models, pricing and links are current.",
  "steps": {
   "todo": [
    "Open the listing and note what is out of date"
   ],
   "progress": [
    "Request or make the updates"
   ],
   "review": [
    "Check the published listing"
   ],
   "close": [
    "Note what changed"
   ]
  }
 },
 "general": {
  "name": "General maintenance",
  "outcome": "the change is made, reviewed and recorded.",
  "steps": {
   "todo": [
    "Confirm the scope"
   ],
   "progress": [
    "Make the changes"
   ],
   "review": [
    "Get the changes reviewed"
   ],
   "close": [
    "Note what changed"
   ]
  }
 }
}
TPL_OF_KIND = {'SambaNova package': 'pkg', 'Built-in provider upstream': 'upstream', 'Provider merged upstream, no guide yet': 'upstream',
               'Internal repo': 'repo', 'Marketplace or network': 'listing'}   # docs guides use 'docs'; anything else 'general'
MAINT_TIER = {}          # asset id -> tier, only for tiers the team confirmed differ from the mode rule
MAINT_CONFIRMED = set()  # asset ids whose tier the team confirmed; all others show "Tier inferred"
def maint_inventory():
    TK = {t['key']: t for t in tickets}
    TR = {x['name']: x for x in (json.load(open(B+'trending.json')) if os.path.exists(B+'trending.json') else [])}
    out = []
    def add(a):
        a['tier'] = MAINT_TIER.get(a['id'], a['tier']); a['inferred'] = a['id'] not in MAINT_CONFIRMED
        a['tpl'] = TPL_OF_KIND.get(a['kind'], 'docs' if a['kind'].startswith('Docs guide') else 'general'); out.append(a)
    for tier in ('critical', 'high'):
        for g in guides:
            m = g['modes'][0]
            if TIER_OF_MODE.get(m) == tier:
                add(dict(id=g['slug'], name=g['name'], tier=tier, kind=KIND_OF_MODE[m], slug=g['slug'], tickets=MAINT_TICKETS.get(g['slug'], []), note=NOTE_OF_TIER[tier]))
        if tier == 'critical':
            for i, n, h, note in MAINT_REPOS:
                a = dict(id=i, name=n, tier='critical', kind='Internal repo', tickets=MAINT_TICKETS.get(i, []), note=note)
                if h: a['home'] = h
                add(a)
        if tier == 'high':
            for n, key in MAINT_UPSTREAM:
                t = TK.get(key); a = dict(id='up-' + re.sub(r'[^a-z0-9]', '-', n.lower()), name=n, tier='high', kind='Provider merged upstream, no guide yet', tickets=[],
                    note=f'SambaNova provider merged upstream through {key}. No guide on docs.sambanova.ai yet.')
                if t and t.get('resolved'): a['base'] = dict(date=t['resolved'], label=f'Provider merged upstream ({key})', key=key)
                if TR.get(n, {}).get('home'): a['home'] = TR[n]['home']
                add(a)
    for tier in ('medium', 'low'):
        for g in guides:
            m = g['modes'][0]
            if TIER_OF_MODE.get(m) == tier:
                add(dict(id=g['slug'], name=g['name'], tier=tier, kind=KIND_OF_MODE[m], slug=g['slug'], tickets=MAINT_TICKETS.get(g['slug'], []), note=NOTE_OF_TIER[tier]))
    unlinked = [t['key'] for t in tickets if 'maintenance' in t['labels'] and t['key'] != 'CP-2157' and not any(t['key'] in a['tickets'] for a in out)]
    if unlinked: print('maintenance tickets not linked to an asset (add to MAINT_TICKETS):', unlinked)
    return dict(generated=SNAP, cadence=MAINT_CADENCE, assets=out, templates=MAINT_TEMPLATES, stages=MAINT_STAGES)

D = dict(snapshot=SNAP, docsRef=os.environ.get('DOCSREF','origin/main'), latest=G['latest'], epic='CP-1521', epicDue='2027-06-30',
         slots=[[k, *v] for k, v in SLOT_META.items()], guides=guides, review=list(review.values()), tickets=tickets, history=months,
         trending=(json.load(open(B+'trending.json')) if os.path.exists(B+'trending.json') else []), gaps=(json.load(open(B+'gaps.json')) if os.path.exists(B+'gaps.json') else dict(fetched=None,rows=[],parity=[])), trendDate=os.environ.get('TRENDDATE', SNAP), maint=maint_inventory())
json.dump(D, open(B + 'data.json', 'w'), separators=(',', ':'))
print('data.json written:', len(guides), 'guides,', len(tickets), 'tickets')
