import os, sys, json, re, datetime
WORK = os.environ.get("WORK", ".").rstrip("/") + "/"
C=json.load(open(WORK+'competitors.json')); D=json.load(open(WORK+'data.json'))
# canonical -> (category, aliases[], ours) ; ours: ('review',slug)|('planned',key)|('ticket',key)|('trending',name)|None
G=[
("GitHub Copilot","Coding agents",["GitHub Copilot","VS Code (Copilot Chat)","Copilot App","Copilot CLI","OAI Compatible Provider for Copilot"],None),
("Claude Agent SDK","Agent frameworks",["Claude Agent SDK","Claude Code Agent (sandbox example)"],None),
("Claude Desktop / Cowork","Chat apps",["Claude Desktop","Claude Desktop / Cowork"],None),
("Factory Droid","Coding agents",["Factory Droid"],None),
("Tavily","Search and data",["Tavily"],None),
("Firecrawl","Search and data",["Firecrawl"],("trending","Firecrawl")),
("Parallel","Search and data",["Parallel"],None),
("E2B","Browser and sandbox",["E2B"],("trending","E2B")),
("Browserbase / Stagehand","Browser and sandbox",["Stagehand","BrowserBase"],("trending","Stagehand")),
("Anchor Browser","Browser and sandbox",["Anchor Browser"],None),
("Arize Phoenix","Evaluation and observability",["Arize Phoenix","Arize"],("trending","Arize Phoenix")),
("Opik","Evaluation and observability",["Opik"],("trending","Opik")),
("Helicone","Evaluation and observability",["Helicone"],("trending","Helicone")),
("MLflow","Evaluation and observability",["MLflow"],None),
("Maxim","Evaluation and observability",["Maxim"],None),
("Keywords AI","Gateways",["Keywords AI"],None),
("Cloudflare AI Gateway","Gateways",["Cloudflare AI Gateway"],("ticket","CP-2437")),
("Kong API Gateway","Gateways",["Kong API Gateway"],None),
("Vercel AI Gateway","Gateways",["Vercel AI Gateway"],None),
("Requesty","Gateways",["Requesty"],None),
("AISIX / API7","Gateways",["AISIX / API7"],None),
("TrueFoundry","Gateways",["TrueFoundry"],None),
("Operant","Gateways",["Operant"],None),
("Portkey","Gateways",["Portkey"],("planned","CP-3089")),
("Amazon Bedrock","Cloud platforms",["Amazon Bedrock (Provider Keys)"],None),
("AWS AgentCore","Cloud platforms",["AWS AgentCore"],None),
("Microsoft Foundry","Cloud platforms",["Microsoft Foundry"],("planned","CP-3077")),
("Google Vertex AI","Cloud platforms",["Google Cloud Vertex AI"],("planned","CP-3086")),
("Strands Agents","Agent frameworks",["Strands Agents"],("trending","Strands Agents")),
("AG2","Agent frameworks",["AG2","AutoGen (AG2)"],("trending","AG2")),
("Mastra","Agent frameworks",["Mastra"],("planned","CP-3103")),
("Pydantic AI","Agent frameworks",["Pydantic AI","PydanticAI"],("planned","CP-3102")),
("DSPy","Agent frameworks",["DSPy"],("planned","CP-3101")),
("OpenAI Agents SDK","Agent frameworks",["OpenAI Agents SDK"],("trending","OpenAI Agents SDK")),
("smolagents","Agent frameworks",["smolagents"],("trending","smolagents")),
("Llama Stack","Agent frameworks",["Llama Stack"],("ticket","CP-2012")),
("Aider","Coding agents",["Aider"],("planned","CP-3106")),
("Braintrust","Evaluation and observability",["Braintrust"],("planned","CP-3098")),
("Langfuse","Evaluation and observability",["Langfuse"],("review","langfuse")),
("LangSmith","Evaluation and observability",["LangSmith"],("review","langsmith")),
("Next.js","App frameworks",["Next.js"],None),
("FlutterFlow","App frameworks",["FlutterFlow"],None),
("Poe","Chat apps",["Poe"],None),
("Reducto","Search and data",["Reducto"],None),
("Unstructured","Search and data",["Unstructured"],None),
("Cartesia","Voice",["Cartesia"],None),
("xRx","Voice",["xRx"],None),
("EchoKit","Voice",["EchoKit"],None),
("JigsawStack","Search and data",["JigsawStack"],("ticket","CP-2197")),
("Cherry Studio","Chat apps",["Cherry Studio"],("trending","Cherry Studio")),
("Chatbox","Chat apps",["Chatbox"],("trending","Chatbox")),
("LobeChat","Chat apps",["LobeChat"],("trending","LobeChat")),
("NextChat","Chat apps",["ChatGPT-Next-Web"],("trending","NextChat")),
("RAGFlow","Search and data",["RAGFlow"],("trending","RAGFlow")),
("Raycast","Chat apps",["Raycast"],None),
("FastGPT","Agent builders",["FastGPT"],None),
("MaxKB","Agent builders",["MaxKB"],None),
("DB-GPT","Agent builders",["DB-GPT"],None),
("Big-AGI","Chat apps",["Big-AGI"],None),
("Immersive Translate","Chat apps",["Immersive Translate"],None),
("Zotero","Chat apps",["Zotero"],None),
("avante.nvim / codecompanion.nvim","Editors",["avante.nvim","codecompanion.nvim"],None),
("Eino (Go)","Agent frameworks",["Eino"],None),
("DeepSearcher","Search and data",["DeepSearcher"],None),
("5ire","Chat apps",["5ire"],None),
("One API","Gateways",["One API"],None),
]
# competitor names that map to one of our live guides (for parity counts)
COVERED={"Agno":"agno","CrewAI":"crew-ai","Browser-Use":"browser-use","BrowserUse":"browser-use","Browser Use (sandbox example)":"browser-use","Vercel AI SDK":"vercel","AI Suite":"aisuite","Milvus":"milvus","Cline":"cline","OpenCode":"opencode","KiloCode":"kilocode","Kilo Code":"kilocode","Roo Code":"roocode","Docker":"docker-compose-agents","Weave (Weights & Biases)":"weave","Weights & Biases":"weave","Exa":"exa","Hugging Face":"hugging-face","HuggingFace":"hugging-face","LlamaIndex":"llama-index","Instructor":"instructor","LangChain":"langchain","LangGraph":"langgraph","LiveKit":"livekit","ElevenLabs":"elevenlabs","Hume AI":"humeai","LiteLLM":"litellm","OpenRouter":"openrouter-byok","AWS Marketplace":"aws-marketplace","Dify":"dify","AutoGen":"autogen","Gradio":"gradio","Composio":"composio","Claude Code":"claude-code","Claude Code (via Together Link / LiteLLM)":"claude-code","Codex CLI":"codex","Codex CLI / Codex app / ChatGPT":"codex","Codex (sandbox example)":"codex","Pi Code":"pi","Pi":"pi","Cursor IDE":"cursor","Cursor":"cursor","VS Code":"vscode","Continue":"continue","LibreChat":"librechat","AI Toolkit":"vscode"}
PROV=[p for p in C['providers']]
def who(aliases):
    out=[]
    for p in PROV:
        names={i['name']:i.get('url') for i in p['items']}
        for a in aliases:
            if a in names: out.append([p['provider'],names[a]]); break
    return out
rows=[]
for name,cat,al,ours in G:
    w=who(al)
    if not w: continue
    st=None
    if ours:
        k,v=ours
        if k=='ticket':
            t=next(t for t in D['tickets'] if t['key']==v); st=dict(kind='ticket',ref=v,label=f"{v} {t['status']}" )
        elif k=='planned': st=dict(kind='planned',ref=v,label=f"Planned {v}")
        elif k=='review': st=dict(kind='review',ref=v,label="In review")
        elif k=='trending': st=dict(kind='trending',ref=v,label="On trending list")
    else: st=dict(kind='gap',ref=None,label="No coverage")
    rows.append(dict(name=name,cat=cat,providers=w,n=len([x for x in w if x[0]!='DeepSeek']),ds=any(x[0]=='DeepSeek' for x in w),ours=st))
rows.sort(key=lambda r:(-r['n'],r['ours']['kind']!='gap',r['name']))
# parity per provider
par=[]
for p in PROV:
    names=[i['name'] for i in p['items']]
    cov=[n for n in names if n in COVERED]
    gapn=[r['name'] for r in rows if any(x[0]==p['provider'] for x in r['providers'])]
    par.append(dict(provider=p['provider'],source=p['source'],total=len(names),covered=len(set(COVERED[n] for n in cov)),tracked=len(gapn),community=p['provider']=='DeepSeek'))
json.dump(dict(fetched=C['fetched'],rows=rows,parity=par),open(WORK+'gaps.json','w'))
for r in rows: print(r['n'],r['ds'],r['name'],r['ours']['label'],[x[0] for x in r['providers']])
for p in par: print(p)
