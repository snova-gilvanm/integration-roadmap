import os, sys, json, re, datetime
WORK = os.environ.get("WORK", ".").rstrip("/") + "/"
REPO = os.environ.get("REPO", "")
SNAP = os.environ.get("SNAPSHOT") or datetime.date.today().isoformat()
TODAY = datetime.date.fromisoformat(SNAP)
import math
T = TODAY
# name: (category, homepage, one-liner, expected route code, sambanova status note)
M = {
"goose":("Coding agents","https://block.github.io/goose/","Block's open-source on-machine agent, desktop app and CLI, MCP-native.","native","SambaNova provider merged upstream (CP-3008). No guide on docs.sambanova.ai yet."),
"smolagents":("Agent frameworks","https://huggingface.co/docs/smolagents","Hugging Face's minimal code-first agent library.","native","SambaNova provider merged upstream (CP-3009). No guide yet."),
"OpenAI Agents SDK":("Agent frameworks","https://openai.github.io/openai-agents-python/","OpenAI's agent framework with handoffs, guardrails and tracing.","openai","Not started. Accepts a custom OpenAI client; verify tool calling on SambaNova models."),
"Letta":("Agent frameworks","https://www.letta.com/","Stateful agents with long-term memory (formerly MemGPT).","openai","Not started."),
"Strands Agents":("Agent frameworks","https://strandsagents.com/","AWS's model-driven agent SDK.","openai","Not started. Very high PyPI volume through AWS usage."),
"AG2":("Agent frameworks","https://ag2.ai/","Community fork and successor of AutoGen 0.2.","openai","Not started. AutoGen guide is live and may cover most of it."),
"CopilotKit":("App frameworks","https://www.copilotkit.ai/","React components and runtime for in-app AI copilots.","openai","Not started. Mastra (CP-3103) pairs with it often."),
"Hermes Agent":("Coding agents","https://hermes-agent.nousresearch.com/","Nous Research's open agent harness.","native","SambaNova provider merged upstream (CP-3007). No guide yet."),
"DeerFlow":("Agent frameworks","https://deerflow.tech/","ByteDance's deep-research multi-agent framework.","native","SambaNova provider merged upstream (CP-3006). No guide yet."),
"Crush":("Coding agents","https://charm.land/","Charm's terminal coding agent.","openai","Not started."),
"Zed":("Editors","https://zed.dev/","High-performance editor with built-in agent panel.","openai","Not started. Pairs with the JetBrains and Windsurf IDE items (CP-3104, CP-3105)."),
"Plandex":("Coding agents","https://plandex.ai/","Terminal agent for large multi-file tasks.","openai","Not started. Low recent activity."),
"Open Interpreter":("Coding agents","https://www.openinterpreter.com/","Natural-language interface that runs code locally.","openai","Not started."),
"Void":("Editors","https://voideditor.com/","Open-source Cursor alternative.","openai","Not started. No releases and little recent activity."),
"Tabby":("Editors","https://www.tabbyml.com/","Self-hosted coding assistant server.","openai","Not started."),
"Gemini CLI":("Coding agents","https://github.com/google-gemini/gemini-cli","Google's terminal agent. Qwen Code CLI (live) is a fork of it.","closed","Gemini models only as far as documented. Qwen Code CLI already covers the fork."),
"LobeChat":("Chat apps","https://lobehub.com/","Open-source chat UI with plugins and many providers.","native","Not started. Check whether SambaNova is already in its provider list."),
"Cherry Studio":("Chat apps","https://www.cherry-ai.com/","Desktop multi-provider AI client, strong in Asia.","openai","Not started. Relevant for the Japanese audience."),
"Jan":("Chat apps","https://jan.ai/","Offline-first desktop assistant with remote providers.","openai","Not started."),
"Chatbox":("Chat apps","https://chatboxai.app/","Cross-platform desktop and mobile LLM client.","openai","Not started."),
"NextChat":("Chat apps","https://nextchat.dev/","Self-hosted ChatGPT-style web UI.","openai","Not started. No commits last month and last release July 2025."),
"Chainlit":("App frameworks","https://chainlit.io/","Python framework for conversational AI UIs.","openai","Not started."),
"RAGFlow":("RAG and data","https://ragflow.io/","Deep-document RAG engine with agent workflows.","openai","Not started."),
"LightRAG":("RAG and data","https://github.com/HKUDS/LightRAG","Graph-based lightweight RAG.","openai","Not started."),
"Cognee":("RAG and data","https://www.cognee.ai/","Memory layer for agents built on knowledge graphs.","openai","Not started."),
"Graphiti":("RAG and data","https://www.getzep.com/","Zep's temporal knowledge graph for agent memory.","openai","Not started. Neo4j guide is live."),
"Firecrawl":("RAG and data","https://www.firecrawl.dev/","Web crawling and extraction API for LLM apps.","openai","Not started. LLM extraction calls a model; check custom base URL."),
"Crawl4AI":("RAG and data","https://crawl4ai.com/","Open-source LLM-friendly crawler.","openai","Not started. Uses LiteLLM, which already lists SambaNova."),
"Docling":("RAG and data","https://docling-project.github.io/docling/","IBM's document conversion toolkit for RAG.","openai","Not started. VLM pipelines can call an OpenAI-compatible API."),
"LanceDB":("RAG and data","https://lancedb.com/","Embedded multimodal vector database.","openai","Not started. Pairs with the vector DB items in Nov 2026."),
"Activepieces":("Automation","https://www.activepieces.com/","Open-source Zapier alternative with AI pieces.","openai","Not started. Pairs with Zapier (CP-3076)."),
"Windmill":("Automation","https://www.windmill.dev/","Developer platform for scripts, flows and apps.","openai","Not started."),
"Botpress":("Automation","https://botpress.com/","Chatbot and agent builder platform.","partner","Not started. Repo release is old; the cloud product is closed."),
"Promptfoo":("Evaluation and observability","https://www.promptfoo.dev/","LLM evals and red-teaming CLI.","openai","Not started. Pairs with Ragas and DeepEval (Q1 2027)."),
"Arize Phoenix":("Evaluation and observability","https://phoenix.arize.com/","Open-source tracing and evaluation.","openai","Not started. Pairs with Langfuse and LangSmith (in review)."),
"Opik":("Evaluation and observability","https://www.comet.com/site/products/opik/","Comet's open-source LLM evaluation and tracing.","openai","Not started."),
"Helicone":("Evaluation and observability","https://www.helicone.ai/","LLM observability proxy and gateway.","openai","Not started. Low recent activity."),
"Guardrails AI":("Safety","https://www.guardrailsai.com/","Validators for LLM inputs and outputs.","openai","Not started. Pairs with NeMo Guardrails (Q1 2027)."),
"Stagehand":("Browser and sandbox","https://www.stagehand.dev/","Browserbase's AI browser automation SDK.","openai","Not started. Browser Use guide is live."),
"Skyvern":("Browser and sandbox","https://www.skyvern.com/","Browser workflow automation with vision LLMs.","openai","Not started."),
"E2B":("Browser and sandbox","https://e2b.dev/","Cloud sandboxes for running agent code.","cookbook","Not started. Not a model consumer; a cookbook pairing with code agents fits."),
"TEN Framework":("Voice","https://theten.ai/","Real-time multimodal voice agent framework.","openai","Not started. Pairs with Deepgram and AssemblyAI (Q1 2027)."),
"Open Notebook":("Chat apps","https://www.open-notebook.ai/","Open-source NotebookLM alternative.","openai","Not started."),
"Perplexica":("Chat apps","https://github.com/ItzCrazyKns/Perplexica","Open-source AI search engine.","openai","Not started. No commits last month."),
"SillyTavern":("Chat apps","https://sillytavern.app/","Power-user chat frontend with a large community.","openai","Not started."),
"Khoj":("Chat apps","https://khoj.dev/","Personal AI second brain.","openai","Not started. No commits last month."),
}
# Repos and packages used for metrics (owner/repo | package):
# goose block/goose; smolagents huggingface/smolagents pypi:smolagents; OpenAI Agents SDK openai/openai-agents-python pypi:openai-agents;
# Letta letta-ai/letta pypi:letta; Strands Agents strands-agents/sdk-python pypi:strands-agents; AG2 ag2ai/ag2 pypi:ag2;
# CopilotKit CopilotKit/CopilotKit npm:@copilotkit/react-core; Hermes Agent NousResearch/hermes-agent; DeerFlow bytedance/deer-flow;
# Crush charmbracelet/crush; Zed zed-industries/zed; Plandex plandex-ai/plandex; Open Interpreter openinterpreter/open-interpreter pypi:open-interpreter;
# Void voideditor/void; Tabby TabbyML/tabby; Gemini CLI google-gemini/gemini-cli npm:@google/gemini-cli; LobeChat lobehub/lobe-chat;
# Cherry Studio CherryHQ/cherry-studio; Jan janhq/jan; Chatbox chatboxai/chatbox; NextChat ChatGPTNextWeb/NextChat; Chainlit Chainlit/chainlit pypi:chainlit;
# RAGFlow infiniflow/ragflow; LightRAG HKUDS/LightRAG pypi:lightrag-hku; Cognee topoteretes/cognee pypi:cognee; Graphiti getzep/graphiti pypi:graphiti-core;
# Firecrawl firecrawl/firecrawl pypi:firecrawl-py; Crawl4AI unclecode/crawl4ai pypi:crawl4ai; Docling docling-project/docling pypi:docling;
# LanceDB lancedb/lancedb pypi:lancedb; Activepieces activepieces/activepieces; Windmill windmill-labs/windmill; Botpress botpress/botpress;
# Promptfoo promptfoo/promptfoo npm:promptfoo; Arize Phoenix Arize-ai/phoenix pypi:arize-phoenix; Opik comet-ml/opik pypi:opik; Helicone Helicone/helicone;
# Guardrails AI guardrails-ai/guardrails pypi:guardrails-ai; Stagehand browserbase/stagehand npm:@browserbasehq/stagehand; Skyvern Skyvern-AI/skyvern pypi:skyvern;
# E2B e2b-dev/E2B pypi:e2b; TEN Framework TEN-framework/ten-framework; Open Notebook lfnovo/open-notebook; Perplexica ItzCrazyKns/Perplexica;
# SillyTavern SillyTavern/SillyTavern; Khoj khoj-ai/khoj pypi:khoj
WD=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
MON={m:i+1 for i,m in enumerate(["january","february","march","april","may","june","july","august","september","october","november","december"])}
def rel(s):
    if not s: return None
    s=s.lower().strip()
    if s=="today": return T
    if s=="yesterday": return T-datetime.timedelta(1)
    m=re.match(r"last (\w+)",s)
    if m and m.group(1) in WD:
        d=(T.weekday()-WD.index(m.group(1)))%7 or 7
        return T-datetime.timedelta(d)
    p=s.split()
    if p[0] in MON:
        mo=MON[p[0]]; y=int(p[1]) if len(p)>1 else (T.year if mo<=T.month else T.year-1)
        return datetime.date(y,mo,15)
    return None
def num(s):
    if s is None: return None
    m=re.match(r"([\d.]+)([kKM]?)",str(s))
    if not m: return None
    v=float(m.group(1)); return v*{"":1,"k":1e3,"K":1e3,"M":1e6}[m.group(2)]
clamp=lambda x:max(0,min(100,x))
out=[]
for f in sorted(x[8:-5] for x in os.listdir(WORK) if x.startswith("metrics_") and x.endswith(".json")):
    for r in json.load(open(WORK+f"metrics_{f}.json")):
        c,home,desc,route,status=M[r["name"]]
        st=num(r["stars"]); cm=num((r["commitsMonth"] or "").split("/")[0]); co=num(r["contributors"]); dl=num((r["downloads"] or "").split("/")[0]) if r["downloads"] else None
        d=rel(r["release"]) or rel(r["lastCommit"]); age=(T-d).days if d else None
        vis=clamp((math.log10(st)-3)/(5.3-3)*100) if st else None
        use=clamp((math.log10(dl)-4)/(7.7-4)*100) if dl else None
        rec=None if age is None else 100 if age<=30 else 75 if age<=90 else 50 if age<=180 else 25 if age<=365 else 0
        act=clamp(math.log10((cm or 0)+1)/math.log10(500)*100) if cm is not None else None
        con=clamp(math.log10(co)/math.log10(500)*100) if co else None
        parts=[x for x in (rec,act,con) if x is not None]
        rel_s=sum(parts)/len(parts) if parts else None
        W=[(vis,30),(use,25),(rel_s,30)]   # same weights as the page (reviews 15 are added in the browser)
        av=[(v,w) for v,w in W if v is not None]
        score=round(sum(v*w for v,w in av)/sum(w for _,w in av)*(1 if use is not None else 0.9)) if av else None
        out.append(dict(name=r["name"],repo=r["repo"],cat=c,home=home,desc=desc,route=route,status=status,
            stars=r["stars"],starsN=st,commits=r["commitsMonth"],contributors=r["contributors"],downloads=r["downloads"],dlN=dl,
            release=r["release"] or (("last commit "+r["lastCommit"]) if r["lastCommit"] else None),releaseAge=age,
            vis=round(vis) if vis is not None else None,use=round(use) if use is not None else None,rel=round(rel_s) if rel_s is not None else None,score=score,
            upstream="merged upstream" in status))
out.sort(key=lambda x:-(x["score"] or 0))
json.dump(out,open(WORK+"trending.json","w"),indent=0)
for x in out: print(x["score"],x["vis"],x["use"],x["rel"],x["name"])
