---
name: "integration-backlog-monitor"
description: "Maintain SambaNova's Integrations Roadmap artifact (epic CP-1521): refresh Jira, docs and radar data, edit or add content, or add new data sources while keeping the existing templates and using only official sources. Use for any request to update, refresh, fix, extend or explain the integrations roadmap page, its kanban board, timeline, catalog, stack rank, radar (trending tools, competitor gaps), or integration backlog."
---

# Integration Backlog Monitor

Maintain the SambaNova **Integrations Roadmap** artifact (epic CP-1521): refresh its data, edit its content, and add new data sources, always following the existing templates and never inventing information.

- **Artifact**: https://claude.ai/artifact/MV2P1NUii2NkA5hMSXGbRL (title "Integrations Roadmap", owner Gilvan Magalhaes)
- **Purpose**: one page that shows what is live on docs.sambanova.ai, what ships next and when, who owns it, the goal and deliverables of every task, how each tool connects to SambaNova, and which new tools are worth integrating.

## Golden rules (read first, apply always)

1. **Official sources only.** Every fact on the page must come from a source listed in "Official sources" below, read in this session. If a fact cannot be verified, leave it out or show it as unknown ("n/a", "Not set", "No description yet"). Never fill gaps from memory or plausibility.
2. **Label anything not verified.** Expected integration routes for planned or trending tools are labelled as expected or unverified. Snapshot dates are shown for every data set.
3. **Ask before assuming.** When a request is ambiguous (which ticket, which window, which source), ask the user with AskUserQuestion before building.
4. **Never use the em dash character (U+2014)** in any text you write: page copy, replies, ticket notes. Verbatim quotes from Jira or the docs may keep their original punctuation.
5. **Confirm side effects.** Never create or edit Jira issues, Confluence pages, or scheduled tasks without the user's explicit OK. Publishing an update to this artifact is fine when the user asked for the change.
6. **Read before republish.** Always `Artifact action:"read"` the URL first, edit the saved file it returns (or rebuild from it), then publish with `url`. Never publish without `url` (that would create a separate artifact).
7. **Keep the template.** Reuse the existing tokens, components, vocabulary and layout. Light theme is the default (no `prefers-color-scheme` dark block); dark applies only when `data-theme="dark"` is set.
8. **Shared state is never overwritten.** Checklists, notes, stack scores, pins, radar signals and reviews live in the artifact database and survive republishes. Do not write to them unless the user asks.

## Official sources

| Source | What it provides | How to read it |
|---|---|---|
| Jira epic **CP-1521** (sambanova.atlassian.net) | All child tickets: key, summary, status, assignee, created, resolution date, due date, window label (`int-oct-2026`, `int-nov-2026`, `int-dec-2026`, `int-q1-2027`, `int-q2-2027`), and the description (goal, links, "Expected outcome:" = deliverables, "Note:"/"Dependency:" lines) | Atlassian Rovo connector: `searchJiraIssuesUsingJql` (`parent = CP-1521`), `getJiraIssue` for descriptions. cloudId `sambanova.atlassian.net`. Results are large: use a subagent and write JSON to the work folder |
| **sambanova/docs** repo, `origin/main` (local clone, e.g. `~/Desktop/IntegrationProjects/docs`) | Published guides `en/integrations/*.mdx` and `ja/integrations/*.mdx`, frontmatter, last commit dates, `docs.json` versions (latest version = first `version` in navigation), categories and blurbs from `en/integrations/overview.mdx` tables | Request the folder with `request_cowork_directory`, then `git fetch` (if the network allows) and `git show origin/main:<path>`. Guides in review are read from their branches (`origin/CP-xxxx-...`) |
| **docs.sambanova.ai** | The deployed guides. Live links: `https://docs.sambanova.ai/docs/en/integrations/<slug>` and `/docs/ja/integrations/<slug>` | web_fetch for spot checks |
| **GitHub + package registries via shields.io** | Stars, commits last month (default branch), latest release date, contributors, monthly PyPI or npm downloads | `mcp__workspace__web_fetch` on `https://img.shields.io/github/stars/OWNER/REPO.json`, `.../github/commit-activity/m/...`, `.../github/release-date/...`, `.../github/last-commit/...`, `.../github/contributors/...`, `.../pypi/dm/PKG.json`, `.../npm/dm/PKG.json`. api.github.com returns nothing through web_fetch. If rate limited, retry with a query param such as `?cacheSeconds=1` |
| **Competitor integration lists** | Which third-party tools other providers document | Cerebras `https://inference-docs.cerebras.ai/integrations`; Groq `https://console.groq.com/docs/integrations`; Together `https://docs.together.ai/docs/inference/sdk-integrations` plus `https://docs.together.ai/llms.txt`; Fireworks `https://docs.fireworks.ai/llms.txt` (ecosystem and nexus sections); Novita `https://docs.novita.ai/llms.txt`; xAI `https://docs.x.ai/llms.txt` (developers/community); DeepSeek community list `https://raw.githubusercontent.com/deepseek-ai/awesome-deepseek-integration/main/README.md` (community, not official) |
| **Team input on the page** | User review ratings and sources, signals, checklists, notes | Artifact database (`ArtifactData`), read only |

Not reachable from this environment (do not work around): the GitHub MCP and api.github.com, OpenRouter app rankings (times out). Never use curl or Python to fetch a URL that web_fetch failed on.

## Page architecture

Single HTML file. Tabs (deep-linkable with `#overview`, `#board`, `#timeline`, `#catalog`, `#rank`, `#radar`, `#how`):

- **Overview**: hero with Goal / Deliverable / Roadmap progress bar; 5 KPI tiles (live integrations, in review, on the roadmap, open tickets, guides to refresh); Delivery windows (5 cards, one per window label, status-segmented bar + items); "How our live integrations connect" (one brand-coloured bar per mode with plain explanation + examples); "What the roadmap items need" (3 buckets: We can build it ourselves = doors open/upstream/adapter; Needs another company or a decision = partner/decision/dependency; No known route yet = closed) with clickable items; Needs attention (blocked, overdue, decision needed, closed door to confirm); Tickets closed per month (SVG bar chart from resolution dates).
- **Board**: kanban columns To do (New, Backlog, Up Next), In progress, Blocked, In review, Done (last 90 days). Scope chips Roadmap / Maintenance and other / All, window and owner filters, search. Card: key, type, title, mode tag, window, door pill, PR, progress bar, due/overdue, owner initials.
- **Timeline**: Gantt Oct 2026 to Jun 2027, bars span the window, coloured by status, today line in orange; group by category, window or owner.
- **Catalog**: every integration (live, in review, planned) with category, mode, interface, webpage, docs links (EN/JA or PR), status and freshness flags (stale over 90 days, no JA, not in latest docs version).
- **Detail drawer** (click anything): for tickets: window, due, owner, opened, category, progress, Goal and context (description paragraphs), Deliverables checklist (from "Expected outcome", shared), How it connects, Links (webpage, references, Jira, PR, live guide), Notes from the ticket, Team notes (shared). For guides: blurb, intro, mode, docs health, links, related tickets.
- **Stack rank**: backlog roadmap items scored 1 to 5 on Customer asks 30, Ecosystem reach 25, Effort 20 (5 = easy), Strategic fit 25; pins override.
- **Radar**: sub-views Trending tools, Competitor gaps, Signals log, How the Radar works (methodology: purpose, selection rules, metric sources, formulas, worked example, gap method, limits).
- **How it works**: 4-step process, integration mode glossary, sources and refresh.

### Embedded data block

`<script type="application/json" id="data">` holds `D`:

```
snapshot "YYYY-MM-DD", docsRef str, latest "v2.2.3", epic "CP-1521", epicDue "2027-06-30",
slots [[label_key, "Oct 2026", start, end], ...],
guides [{slug,name,group,sub,blurb,intro,home,modes[],iface,langs[],upd,age,ja,jaUpd,latest,lines,state:"live",tickets[]}],
review [same shape, state:"review"],
tickets [{key,summary,status,owner,created,resolved,due,slot,type,goal[],deliver[],urls[],notes[],
          slug?,cat?,modes?,iface?,door?,home?,review?,pr?}],
history [["YYYY-MM", closedCount], ...13 months],
trending [{name,repo,cat,home,desc,route,status,stars,starsN,commits,contributors,downloads,dlN,release,releaseAge,vis,use,rel,score,upstream}],
gaps {fetched, rows:[{name,cat,providers:[[provider,url]],n,ds,ours:{kind,ref,label}}], parity:[{provider,source,total,covered,tracked,community}]},
trendDate "YYYY-MM-DD"
```

### Vocabulary (keep exactly)

- **Modes**: `native` Built-in provider; `openai` OpenAI-compatible (`https://api.sambanova.ai/v1`); `anthropic` Anthropic-compatible (`ANTHROPIC_BASE_URL=https://api.sambanova.ai`); `sdk` SambaNova package; `commercial` Marketplace or network; `app` Platform app; `adapter` Adapter or connector; `partner` Partner motion; `closed` No route today; `cookbook` Cookbook; `model` Model availability.
- **Interfaces**: code, cli, ide, nocode, cloud, partner.
- **Doors** (roadmap feasibility): open Self-serve config; upstream Upstream provider PR; adapter Build an adapter; decision Decision needed; partner Partner motion; closed Closed door; dependency Blocked on model.
- **Ticket types** (from summary): Partnership, Catalog listing, Cookbook, Maintenance, Enablement, Integration.
- **Progress**: Done = 100%; otherwise the share of ticked deliverables, never lower than the status weight (In Review 80, In Progress 40, Blocked 15, To do 0).

Mode and interface for live guides come from reading the guide (curated in `build.py` OLDKIND / MODE_OVR). For planned tickets they come only from the ticket description (curated in `build.py` PLAN). If the description does not say, do not set a mode; ask the user or leave it out.

### Shared database collections (capability `db`)

`deliverables/{ticketKey}` {done:{index:bool}, by, at}; `notes/{ticketKey}` {text, by, at}; `stack/{ticketKey}` {customer, reach, effort, strategic, by, at}; `pins/{ticketKey}` {pinned, by, at}; `radar/{id}` {name, conf, source, why, by, at}; `reviews/{safeName}` {name, rating, source, by, at}. `by` is an opaque user id resolved with `user.profiles`.

### Capabilities (keep on every publish; omit `capabilities` to carry them forward)

`{"db":{}, "user":{"scopes":["profile"]}, "mcp":{"servers":[{"server":"Atlassian Rovo","tools":["searchJiraIssuesUsingJql"]}]}}`. The page watches `parent = CP-1521 AND (statusCategory != Done OR resolved >= -120d)` every 5 minutes for viewers with the Atlassian connector and overlays status, assignee, due date, window label and resolution date.

### Design template

Fonts: Sora (display), IBM Plex Sans (body), IBM Plex Mono (numbers). Tokens on `:root`: `--brand #974fc7` (SambaNova docs primary), `--brand-ink #6d2fa3`, `--flame #e8702a` (today line and highlights), semantic `--ok --work --bad --info --idle` with `-bg` variants, neutrals with a purple bias. Logo: base64 of `logo/new-logo.png` (light) and `new-logo-dark.png` from the docs repo. Components to reuse: `.card/.card-h/.card-b`, `.pill` (ok, work, bad, info, brand, flame), `.tag`, `.chip[aria-pressed]`, `.kpi`, `.kc` (kanban card), `.tw > table`, `.drawer` via `openTicket(key)` / `openGuide(slug)`, `modeTag(m)`, `ext(href, text)`. Semantic colours mean status only; never use red/green to encode anything that is not status (for feasibility or mode breakdowns use the single brand colour with plain-language labels).

## Workflows

Use a work folder in the scratchpad, e.g. `WORK=/tmp/ibm` in bash. Recreate the scripts from the "Scripts" section into `$WORK/scripts/` before running them.

### A. Change wording, layout or a feature
1. `Artifact action:"read" url:<artifact>` and Read the saved file fully.
2. Edit that file with Edit (keep tokens and components). Respect rule 4.
3. Syntax-check the inline script: extract the last `<script>` block and run `node --check`.
4. Publish with `url` and a short `label`. Tell the user in one or two sentences what changed.

### B. Correct or add data without a full refresh
1. Read the artifact, then extract the data block into `$WORK/data.json` (Python: regex `id="data">(.*?)</script>` with DOTALL, replace `<\/` with `</`, write the group).
2. Verify the new fact in an official source in this session, then edit `data.json` (and the curated maps in the scripts so the next refresh keeps it).
3. `WORK=$WORK python3 scripts/inject.py page.html page.new.html`, check, publish `page.new.html` with `url`.

### C. Full refresh (Jira + docs + radar)
1. **Jira list**: subagent runs `searchJiraIssuesUsingJql` with `parent = CP-1521 ORDER BY key DESC`, fields summary, status, assignee, created, resolutiondate, duedate, labels, paging (`key < CP-xxxx`) until all are read, and writes `$WORK/jira.json` as `[{key, summary, status, owner (displayName without " [External]"), created (YYYY-MM-DD), resolved, due, slot (the int-* label or null)}]`.
2. **Descriptions**: subagent calls `getJiraIssue` (markdown) for every slotted ticket and every open ticket, writes `$WORK/jira_desc.json` as `[{key, summary, desc}]` verbatim.
3. **Docs**: request the docs folder, `git fetch`, then `REPO=<path> REVIEW='slug=origin/branch,...' SNAPSHOT=<today> python3 scripts/extract.py`. Find review branches with `git branch -r | grep CP-` and check which guides exist only on a branch. Update PR numbers in `build.py` PR from the open PR list.
4. **Radar metrics**: split the trending list into batches of about 15 and give each subagent the shields.io endpoints above; each writes `$WORK/metrics_<x>.json` as `[{name, repo, stars, commitsMonth, release, lastCommit, contributors, downloads}]`, values exactly as returned, null when unavailable.
5. **Competitors**: one subagent reads the competitor lists above and writes `$WORK/competitors.json` `{fetched, providers:[{provider, source, items:[{name,url}], notes}]}` with only names actually seen.
6. Run `trending.py`, `build.py`, `gaps.py`, `build.py` again (gaps needs data.json; build then embeds gaps), then `inject.py` into the page read from the artifact.
7. Review diffs that matter: new or closed tickets, status moves, new guides, new gaps. Update PLAN for new slotted tickets (rule: mode and door only from the description). Publish and report what moved.

### D. Add a new data source
1. Confirm with the user which official source and what question it answers.
2. Fetch it into `$WORK/<source>.json` with the source URL and fetch date inside the file.
3. Add it to `D` in `build.py` (new key), render it with existing components, and add the source to the "Sources and refresh" card in How it works (and to the Radar methodology if it affects scores).
4. Show the snapshot date next to the data. If it changes a score, document the formula change in the methodology view.

### E. Add a roadmap ticket's metadata (PLAN in build.py)
`'CP-xxxx': (slug, category, [modes], iface, door)`. Read the ticket description: a custom base URL or OpenAI-compatible provider = `openai`/`open`; named provider contributed upstream = `native`/`upstream`; spec adapter or transformation script = `adapter`; curated provider list or listing = `partner`; no documented route = `closed`; "decide between" = `decision`; waiting on a model = `model`/`dependency`. Category must be one already used unless the user agrees a new one.

### F. Trending candidates and competitor providers
- A trending candidate must be open source with a public GitHub repo, not live/in review/planned, about 5k stars or more or a high-volume package, in one of the catalog categories. Add it to `M` in `trending.py` with category, official homepage, one-line description taken from its own site or README, expected route and status text, then collect its metrics.
- Score: Visibility = (log10(stars) - 3) / 2.3 x 100; Usage = (log10(downloads/mo) - 4) / 3.7 x 100; Reliability = mean of release recency (30d 100, 90d 75, 180d 50, 1y 25, older 0), log10(commits+1)/log10(500) x 100, log10(contributors)/log10(500) x 100; Reviews = (rating - 1) / 4 x 100. Score = weighted mean 30/25/30/15 over present signals, x 0.9 when downloads are missing. All capped 0 to 100. The page recomputes the score in the browser so team review ratings count. If the formula changes, update the methodology view and its worked example.
- A new competitor provider: add its official integrations index to step C.5, add aliases in `gaps.py` G, and keep DeepSeek labelled as a community list.

## Verification checklist before publishing
- Every number on the page traces to a file in `$WORK` fetched this session (or the previous published data, unchanged).
- `node --check` passes; no `prefers-color-scheme` dark block; `[hidden]{display:none!important}` present.
- No em dash in text you wrote (`inject.py` warns).
- Snapshot dates updated (`SNAPSHOT`, `DOCSREF`, `TRENDDATE`).
- Publish with `url`, omit `icon`, omit `capabilities` unless they change.
- After publishing, one functional check if storage code changed: write a probe doc, `ArtifactData list`, delete it with `if_version`.

## Orientation snapshot (5 Oct 2026, re-verify before use)
65 live guides (latest docs version v2.2.3), 3 in review (Langfuse CP-3074, LangSmith CP-3075, Zapier CP-3076), 38 slotted roadmap tickets CP-3074 to CP-3111 across Oct 2026 to Q2 2027, 168 child tickets in CP-1521, epic due 2027-06-30. Main owners: Gilvan Magalhaes (roadmap), Jorge Piedrahita (maintenance), Kwasi Ankomah (upstream providers), Luis Salazar, Rodrigo Maldonado. Upstream SambaNova providers merged without a guide: goose (CP-3008), smolagents (CP-3009), Hermes Agent (CP-3007), DeerFlow (CP-3006). Hermes Agent's 251k stars as reported by shields.io needs confirming.

## Scripts

Recreate each file below in `$WORK/scripts/` exactly, then run with `WORK`, `REPO`, `SNAPSHOT`, `DOCSREF`, `REVIEW`, `TRENDDATE` set. Order for a full refresh: extract.py, trending.py, build.py, gaps.py, build.py, inject.py. The curated maps (OLDKIND, MODE_OVR, HOME, PLAN, PR in build.py; M in trending.py; G and COVERED in gaps.py) are the only hand-maintained facts: change them only with evidence from an official source.

### scripts/extract.py

See the full skill documentation in the repository or the deployed version for the complete script files.
