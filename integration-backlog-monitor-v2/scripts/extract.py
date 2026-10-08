import os, sys, json, re, datetime
WORK = os.environ.get("WORK", ".").rstrip("/") + "/"
REPO = os.environ.get("REPO", "")          # local clone of github.com/sambanova/docs
SNAP = os.environ.get("SNAPSHOT") or datetime.date.today().isoformat()
TODAY = datetime.date.fromisoformat(SNAP)
import subprocess, collections
R=REPO
def sh(*a): return subprocess.run(a,cwd=R,capture_output=True,text=True).stdout
# categories + one-line blurbs from the Integrations overview page
ov=sh('git','show','origin/main:en/integrations/overview.mdx'); cat={}; g=s_=None
for line in ov.splitlines():
    if line.startswith('## '): g=line[3:].strip(); s_=None
    elif line.startswith('### '): s_=line[4:].strip()
    m=re.match(r'\|\s*\[([^\]]+)\]\(/en/integrations/([^)#]+)\)\s*\|\s*(.*?)\s*\|',line)
    if m: cat.setdefault(m.group(2),[]).append(dict(name=m.group(1),group=g,sub=s_,blurb=m.group(3)))
nav=json.loads(sh('git','show','origin/main:docs.json'))
# versions
vers=[]
def walk(o,ver=None,acc=None):
    if isinstance(o,dict):
        if 'version' in o: ver=o['version']; vers.append(ver)
        for k,v in o.items(): walk(v,ver,acc)
    elif isinstance(o,list):
        for x in o: walk(x,ver,acc)
    elif isinstance(o,str) and '/integrations/' in o and ver is not None:
        acc.setdefault(ver,set()).add(o.split('/integrations/')[-1])
acc={}; walk(nav['navigation'],None,acc)
latest=vers[0] if vers else None
print('versions',vers[:4],'latest',latest)
today=TODAY
def lastdate(ref,path):
    o=sh('git','log','-1','--format=%ad','--date=short',ref,'--',path).strip()
    return o or None
def mode_of(t,slug):
    tl=t.lower(); modes=[]
    if re.search(r'anthropic[_ -]base[_ -]url|anthropic-compatible|/v1/messages',tl): modes.append('anthropic')
    if re.search(r'openai[- ]compatible|openai_base_url|base_url\s*=|baseurl|api\.sambanova\.ai/v1|openai_api_base|openai-compatible',tl): modes.append('openai')
    if re.search(r'pip install[^\n]*(langchain-sambanova|llama-index-llms-sambanova|sambanova)|npm (i|install)[^\n]*sambanova|@ai-sdk/sambanova|langchain_sambanova|sambanova import|from sambanova',tl): modes.append('sdk')
    if re.search(r'select \*\*sambanova\*\*|choose \*\*sambanova\*\*|sambanova as (the |a )?(model )?provider|provider[^\n]{0,40}sambanova|sambanova/[a-z]',tl): modes.append('native')
    return list(dict.fromkeys(modes))
def surface(t):
    tl=t.lower(); s=[]
    if re.search(r'