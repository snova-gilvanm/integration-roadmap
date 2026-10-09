---
name: "integration-backlog-monitor-v2"
description: "Maintain SambaNova's Integrations Roadmap artifact (epic CP-1521): refresh Jira, docs and radar data, edit or add content, track maintenance, turn Radar candidates into Jira tickets, or add new data sources while keeping the existing templates and using only official sources. Use for any request to update, refresh, fix, extend or explain the integrations roadmap page, its kanban board, timeline, catalog, stack rank, radar (trending tools, competitor gaps, signals, Create in Jira from the Radar, roadmap ticket templates), Maintenance tab (maintenance queue, asset inventory, cadences, proposals, Create in Jira, ticket templates and checklists, the label legend, the Jira maintenance label), or integration backlog. Supersedes integration-backlog-monitor (v1)."
---

# Integration Backlog Monitor

Maintain the SambaNova **Integrations Roadmap** artifact (epic CP-1521): refresh its data, edit its content, and add new data sources, always following the existing templates and never inventing information.

- **Artifact**: https://claude.ai/artifact/MV2P1NUii2NkA5hMSXGbRL (title "Integrations Roadmap", owner Gilvan Magalhaes)
- **Purpose**: one page that shows what is live on docs.sambanova.ai, what ships next and when, who owns it, the goal and deliverables of every task, how each tool connects to SambaNova, which new tools are worth integrating, and what needs maintenance when.
- **Version**: 2.2.0 (8 Oct 2026). Source of truth is the git repo `integration-roadmap`; see `CHANGELOG.md` in this folder for what changed in each version. v2 replaced v1 (keep v1 disabled so the two do not compete).

## Golden rules (read first, apply always)

1. **Official sources only.** Every fact on the page must come from a source listed in "Official sources" below, read in this session. If a fact cannot be verified, leave it out or show it as unknown ("n/a", "Not set", "No description yet"). Never fill gaps from memory or plausibility.
2. **Label anything not verified.** Expected integration routes for planned or trending tools are labelled as expected or unverified. Snapshot dates are shown for every data set.
3. **Ask before assuming.** When a request is ambiguous (which ticket, which window, which source), ask the user with AskUserQuestion before building.
4. **Never use the em dash character (U+2014)** in any text you write: page copy, replies, ticket notes. Verbatim quotes from Jira or the docs may keep their original punctuation.
5. **Confirm side effects.** Never create or edit Jira issues (this includes adding the `maintenance` label and creating tickets from approved proposals), Confluence pages, or scheduled tasks without the user's explicit OK. Publishing an update to this artifact is fine when the user asked for the change.
6. **Read before republish.** Always `Artifact action:"read"` the URL first, edit the saved file it returns (or rebuild from it), then publish with `url`. Never publish without `url` (that would create a separate artifact).
7. **Keep the template.** Reuse the existing tokens, components, vocabulary and layout. Light theme is the default (no `prefers-color-scheme` dark block); dark applies only when `data-theme="dark"` is set.
8. **Shared state is never overwritten.** Checklists, notes, stack scores, pins, radar signals, reviews, maintenance proposals and exposure ratings live in the artifact database and survive republishes. Do not write to them unless the user asks.
9. **Every label is explained.** Any tier, status, flag, pill, button, column or number added to the Maintenance or Radar tab gets a plain-language entry in the page's `TIP` (Maintenance) or `TIP_R` (Radar) map and a row in that tab's "What the labels mean" legend, written so anyone on the team understands it. Never ship a label without its explanation.

## Official sources

| Source | What it provides | How to read it |
|---|---|---|
| Jira epic **CP-1521** (sambanova.atlassian.net) | All child tickets: key, summary, status, assignee (and whether the account is active), issue type, labels (window labels and `maintenance`), created, resolution date, due date, window label (`int-oct-2026`, `int-nov-2026`, `int-dec-2026`, `int-q1-2027`, `int-q2-2027`), and the description (goal, links, "Expected outcome:" = deliverables, "Note:"/"Dependency:" lines) | Atlassian Rovo connector: `searchJiraIssuesUsingJql` (`parent = CP-1521`), `getJiraIssue` for descriptions. cloudId `sambanova.atlassian.net`. Results are large: use a subagent and write JSON to the work folder |
| **sambanova/docs** repo, `origin/main` (local clone, e.g. `~/Desktop/IntegrationProjects/docs`) | Published guides `en/integrations/*.mdx` and `ja/integrations/*.mdx`, frontmatter, last commit dates, `docs.json` versions (latest version = first `version` in navigation), categories and blurbs from `en/integrations/overview.mdx` tables | Request the folder with `request_cowork_directory`, then `git fetch` (if the network allows) and `git show origin/main:<path>`. Guides in review are read from their branches (`origin/CP-xxxx-...`) |
| **docs.sambanova.ai** | The deployed guides. Live links: `https://docs.sambanova.ai/docs/en/integrations/<slug>` and `/docs/ja/integrations/<slug>` | web_fetch for spot checks |
| **GitHub + package registries via shields.io** | Stars, commits last month (default branch), latest release date, contributors, monthly PyPI or npm downloads | `mcp__workspace__web_fetch` on `https://img.shields.io/github/stars/OWNER/REPO.json`, `.../github/commit-activity/m/...`, `.../github/release-date/...`, `.../github/last-commit/...`, `.../github/contributors/...`, `.../pypi/dm/PKG.json`, `.../npm/dm/PKG.json`. api.github.com returns nothing through web_fetch. If rate limited, retry with a query param such as `?cacheSeconds=1` |
| **Competitor integration lists** | Which third-party tools other providers document | Cerebras `https://inference-docs.cerebras.ai/integrations`; Groq `https://console.groq.com/docs/integrations`; Together `https://docs.together.ai/docs/inference/sdk-integrations` plus `https://docs.together.ai/llms.txt`; Fireworks `https://docs.fireworks.ai/llms.txt` (ecosystem and nexus sections); Novita `https://docs.novita.ai/llms.txt`; xAI `https://docs.x.ai/llms.txt` (developers/community); DeepSeek community list `https://raw.githubusercontent.com/deepseek-ai/awesome-deepseek-integration/main/README.md` (community, not official) |
| **Team input on the page** | User review ratings and sources, signals, checklists, notes | Artifact database (`ArtifactData`), read only |

Not reachable from this environment (do not work around): the GitHub MCP and api.github.com, OpenRouter app rankings (times out). Never use curl or Python to fetch a URL that web_fetch failed on.

## Page architecture

Single HTML file. Tabs (deep-linkable with `#overview`, `#board`, `#timeline`, `#catalog`, `#rank`, `#radar`, `#maint`, `#how`):

- **Overview**: hero with Goal / Deliverable / Roadmap progress bar; 5 KPI tiles (live integrations, in review, on the roadmap, open tickets, guides to refresh); Delivery windows (5 cards, one per window label, status-segmented bar + items); "How our live integrations connect" (one brand-coloured bar per mode with plain explanation + examples); "What the roadmap items need" (3 buckets: We can build it ourselves = doors open/upstream/adapter; Needs another company or a decision = partner/decision/dependency; No known route yet = closed) with clickable items; Needs attention (blocked, overdue, decision needed, closed door to confirm); Tickets closed per month (SVG bar chart from resolution dates).
- **Board**: kanban columns To do (New, Backlog, Up Next), In progress, Blocked, In review, Done (last 90 days). Scope chips Roadmap (tickets with a window, plus tickets labelled `radar`) / Maintenance and other / All, window and owner filters, search. Card: key, type, title, mode tag, window, door pill, PR, progress bar, due/overdue, owner initials.
- **Timeline**: Gantt Oct 2026 to Jun 2027, bars span the window, coloured by status, today line in orange; group by category, window or owner.
- **Catalog**: every integration (live, in review, planned) with category, mode, interface, webpage, docs links (EN/JA or PR), status and freshness flags (stale over 90 days, no JA, not in latest docs version).
- **Detail drawer** (click anything): for tickets: window, due, owner, opened, category, progress, Goal and context (description paragraphs), Deliverables checklist (from "Expected outcome", shared), How it connects, Links (webpage, references, Jira, PR, live guide), Notes from the ticket, Team notes (shared). For guides: blurb, intro, mode, docs health, links, related tickets.
- **Stack rank**: backlog roadmap items scored 1 to 5 on Customer asks 30, Ecosystem reach 25, Effort 20 (5 = easy), Strategic fit 25; pins override. Also lists open tickets labelled `radar` that have no window, tagged **Not scheduled**, with a note to add a window label in Jira.
- **Radar**: sub-views Trending tools, Competitor gaps, Signals log, How the Radar works (methodology: purpose, selection rules, metric sources, formulas, worked example, gap method, limits).
  - **What the labels mean** legend at the top (collapsible, localStorage `rLegend`): from candidate to Jira ticket, the seven ticket templates and when each is suggested, what happens after creation, and the Radar's other labels (expected route, signal confidence, gap statuses). Hover text from `TIP_R` on every label.
  - **Jira cell** (`jiraCell(name, from)`) on every Trending row, every Competitor gap row with status No coverage or On trending list, and every signal: **In Jira: CP-xxxx** when an open ticket names the tool (`openFor`); otherwise **Create in Jira** (viewers with the connector) or **Approve for Jira** / "Approved, not in Jira yet" (viewers without it).
  - **Create pop-up** (`openRadarCreate(src)`, same `<dialog id="m-dlg">`): a template dropdown with the suggested one marked, editable summary and markdown description from `draftRadar()`, "Reset to the template", fixed fields as tags (project CP, parent CP-1521, Story, labels `new-integration` and `radar`, Not scheduled, unassigned). Refuses to create when an open ticket already names the tool. On success the ticket joins the page at once, `rjira` records the key, and a signal it came from gets `key`.
- **Maintenance**:
  - 5 KPI tiles (open in Jira, overdue assets, due in 30 days, owner needed, proposed).
  - **What the labels mean** legend (collapsible, remembered per viewer in localStorage `mLegend`): tiers, statuses, flags, proposals, columns, ticket templates, and "How a score is calculated" with a worked example computed live (Gradio). Every label on the tab also carries a hover explanation from `TIP`.
  - **Maintenance queue**: open tickets labelled `maintenance` plus proposals not in Jira; customer defects and bugs first, then score. Jira rows show owner, a "Checklist d of n" bar and flags. Proposal rows show **Create in Jira** (viewers with the Atlassian connector) or **Approve for Jira** (viewers without it, pill "Approved, not in Jira yet"), plus Dismiss. A form below proposes a task by hand.
  - **Create in Jira pop-up** (`openCreate(item)`, a `<dialog id="m-dlg">`): summary and markdown description drafted by `draftTicket()` from the asset's template, all editable, "Reset to the template"; fixed fields shown as tags (project CP, parent CP-1521, Task, label `maintenance`, unassigned). Creates the ticket with the viewer's connector, adds it to the queue at once, and sets the proposal to `created` with the key. Errors branch on the mcp error code: missing or blocked connector offers "Approve instead"; `tool_error` shows Jira's reason; ambiguous outcomes (`server_unavailable`, `upstream_error`, `cancelled`) warn not to retry blindly and link a Jira search for the summary.
  - **What we maintain**: asset inventory with tier, last maintained and its source, cadence, next due, status, open tickets, team exposure rating, score. Asset drawer (`openAsset(id)`) shows a "How this score was calculated" table (`scoreTable`), why the tier, linked tickets with checklist counts, Propose maintenance, links.
  - **Schedule, next six months**; **Tiers and cadence**; **How the score works**.
  - Ticket drawer (`openTicket`) gains a **Jira checklist** section for tickets with a checklist (`checklistSec`), with the "behind" note.
- **How it works**: 4-step process, integration mode glossary, sources and refresh (includes a Maintenance paragraph).

### Embedded data block

`<script type="application/json" id="data">` holds `D`:

```
snapshot "YYYY-MM-DD", docsRef str, latest "v2.2.3", epic "CP-1521", epicDue "2027-06-30",
slots [[label_key, "Oct 2026", start, end], ...],
guides [{slug,name,group,sub,blurb,intro,home,modes[],iface,langs[],upd,age,ja,jaUpd,latest,lines,state:"live",tickets[]}],
review [same shape, state:"review"],
tickets [{key,summary,status,owner,created,resolved,due,slot,type,goal[],deliver[],urls[],notes[],
          labels[],itype,ownerOff,chk?[{g:stage heading, items:[{t,d:done}]}],
          slug?,cat?,modes?,iface?,door?,home?,review?,pr?}],
history [["YYYY-MM", closedCount], ...13 months],
trending [{name,repo,cat,home,desc,route,status,stars,starsN,commits,contributors,downloads,dlN,release,releaseAge,vis,use,rel,score,upstream}],
gaps {fetched, rows:[{name,cat,providers:[[provider,url]],n,ds,ours:{kind,ref,label}}], parity:[{provider,source,total,covered,tracked,community}]},
trendDate "YYYY-MM-DD",
radarT {stages [[evaluate,"Evaluate"],[build,"Build"],[docs,"Docs"],[review,"Review"],[publish,"Publish"]],
        order [openai, upstream, guide, package, partner, cookbook, evaluate],
        templates {key: {name, summary "{tool} ...", route, outcome, steps{evaluate[],build[],docs[],review[],publish[]}}},
        routeTpl {expected route: template key}},
maint {generated "YYYY-MM-DD", cadence {critical,high,medium,low} in months,
       assets [{id,name,tier,kind,tpl,slug?,home?,tickets[],base?{date,label,key},note,inferred}],
       stages [[key,"To do"],[...,"In progress"],[...,"In review"],[...,"Before closing"]],
       templates {pkg|upstream|repo|docs|listing|general: {name, outcome, steps{todo[],progress[],review[],close[]}}}}
```

The page reads `D.maint` with a fallback (empty inventory, default cadences), but a refresh must always rebuild it: `build.py` below does.

### Vocabulary (keep exactly)

- **Modes**: `native` Built-in provider; `openai` OpenAI-compatible (`https://api.sambanova.ai/v1`); `anthropic` Anthropic-compatible (`ANTHROPIC_BASE_URL=https://api.sambanova.ai`); `sdk` SambaNova package; `commercial` Marketplace or network; `app` Platform app; `adapter` Adapter or connector; `partner` Partner motion; `closed` No route today; `cookbook` Cookbook; `model` Model availability.
- **Interfaces**: code, cli, ide, nocode, cloud, partner.
- **Doors** (roadmap feasibility): open Self-serve config; upstream Upstream provider PR; adapter Build an adapter; decision Decision needed; partner Partner motion; closed Closed door; dependency Blocked on model.
- **Ticket types** come only from Jira labels, never from words in the summary: `maintenance` is Maintenance, `new-integration` is New integration, anything else is Other (validation, benchmarking, proof of concept, research). Same rule in `classify()` in `build.py` and in the page's live overlay.
- **Maintenance work** is identified only by the Jira label `maintenance`, never by words in the summary. Validation, benchmarking and POC tickets are not maintenance (decided 6 Oct 2026 for CP-2709, CP-2582, CP-2759, CP-2748).
- **Maintenance tiers and cadence**: critical = our code (SambaNova packages, internal repos), every 2 months; high = our provider module inside an external library, every 3 months; medium = docs guide for a third-party tool, every 6 months; low = marketplace or network listing, every 12 months (an assumption, not agreed). Tier comes from the guide's mode (`sdk` critical, `native` high, `openai`/`anthropic` medium, `commercial` low) unless `MAINT_TIER` in `build.py` overrides it; assets not in `MAINT_CONFIRMED` are shown as "Tier inferred".
- **Maintenance status**: Overdue, No record, Due soon (within 30 days), Scheduled. Last maintained = latest Done labelled ticket linked to the asset; critical and high fall back to the guide's docs update, medium and low use whichever is later; upstream-only assets use their merge ticket. Score = criticality (5/4/2/1) x 40 + team exposure (1 to 5) x 30 + urgency (time since last / cadence: under 50% 1, 80% 2, 100% 3, 150% 4, beyond or no record 5) x 30, as a weighted mean over the signals present, 0 to 100.
- **Ticket templates** (`MAINT_TEMPLATES` in `build.py`, chosen per asset by `TPL_OF_KIND`): SambaNova package (`pkg`), Provider module upstream (`upstream`, also for providers merged without a guide), Internal repo (`repo`), Docs guide (`docs`), Marketplace listing (`listing`), General maintenance (`general`, proposals with no asset). Each has an "Expected outcome" sentence and steps per stage; `{asset}` and `{since}` are filled in. Summary: `<asset> maintenance, <Mon YYYY>` (en-US dates). Description layout (verified in Jira on CP-3181): purpose line; "Why now" with last maintained and previous tickets; links; "Expected outcome:"; then `### To do`, `### In progress`, `### In review`, `### Before closing`, each followed by `- [ ]` lines, which Jira turns into native checkboxes; closing line "Created from the Integrations Roadmap Maintenance tab."
- **Checklist behind**: the ticket's status column requires earlier stages to be fully ticked: In progress or Blocked needs To do; In review needs To do and In progress; Done needs all four.
- **Proposal lifecycle** (`mprop`): proposed, then approved (no connector) or created (ticket made, `key` stored), or dismissed. Page suggestions are hidden while the asset has an open labelled ticket. Team proposals are hidden once a labelled ticket for the same asset has the same title (normalized), and otherwise show "CP-xxxx is already open for this asset".
- **Roadmap tickets from the Radar** are Jira Stories under CP-1521 labelled `new-integration` and `radar`, with no window label until someone schedules them. Description layout (verified in Jira on CP-3183): "{Tool}: {description}. Category: {category}."; "Why now:" with radar score and parts, stars, downloads, last release, competitors listing it, team signals and reviews; "Expected route (not verified): {template name}." plus the Radar note; a block with `Category: ...` and `Integration route: {route}` on separate lines; links (repository, website, competitor docs, earlier Done tickets); "Expected outcome:"; then `### Evaluate`, `### Build`, `### Docs`, `### Review`, `### Publish` with `- [ ]` lines; "Created from the Integrations Roadmap Radar." On refresh, `structured()` in `build.py` reads the Category and Integration route lines into the ticket's `cat` and `modes` when the ticket has no `PLAN` entry, so Radar tickets need no hand curation.
- **Radar templates** (`RADAR_TEMPLATES`, suggested by `ROUTE_TPL` from the tool's expected route): OpenAI-compatible config (`openai`; routes openai, anthropic), Upstream provider PR (`upstream`; native), Provider already upstream, guide missing (`guide`; native with the provider merged, decided in the page), SambaNova package or plugin (`package`; sdk), Partner or commercial (`partner`; partner, commercial), Cookbook (`cookbook`), Route unknown, evaluate first (`evaluate`; closed, app, adapter, and any gap or signal not on the trending list).
- **Duplicate guard**: only open tickets block Create in Jira. A ticket matches when `rjira` holds its key for the tool or the tool name appears as a whole word in the summary. Done tickets show in the draft as "Earlier ticket", so tools such as Hermes Agent (CP-3007, provider merged) can still get a guide ticket.
- **Checklist behind** for Radar tickets: In progress or Blocked needs Evaluate; In review needs Evaluate, Build and Docs; Done needs all five.
- **Renamed tools**: Llama Stack is now OGX (guide `ogx`, ticket CP-2961).
- **Progress**: Done = 100%; otherwise the share of ticked deliverables, never lower than the status weight (In Review 80, In Progress 40, Blocked 15, To do 0).

Mode and interface for live guides come from reading the guide (curated in `build.py` OLDKIND / MODE_OVR). For planned tickets they come only from the ticket description (curated in `build.py` PLAN). If the description does not say, do not set a mode; ask the user or leave it out.

### Shared database collections (capability `db`)

`deliverables/{ticketKey}` {done:{index:bool}, by, at}; `notes/{ticketKey}` {text, by, at}; `stack/{ticketKey}` {customer, reach, effort, strategic, by, at}; `pins/{ticketKey}` {pinned, by, at}; `radar/{id}` {name, conf, source, why, by, at}; `reviews/{safeName}` {name, rating, source, by, at}; `mprop/{id}` {status: proposed|approved|dismissed|created, title, asset, why, manual, key?, by, at}, where automatic proposals use the id `auto-<assetId>-<YYYY-MM>` and manual ones a random id; `mexp/{assetId}` {v: 1 to 5 or null, by, at}; `rjira/{safe tool name}` {name, status: approved|created, key?, by, at}; signals in `radar/{id}` gain `key` when a ticket is created from them. `by` is an opaque user id resolved with `user.profiles`.

### Capabilities (keep on every publish; omit `capabilities` to carry them forward)

`{"db":{}, "user":{"scopes":["profile"]}, "mcp":{"servers":[{"server":"Atlassian Rovo","tools":["searchJiraIssuesUsingJql","createJiraIssue"]}]}}` (createJiraIssue added in 2.1.0; each viewer consents once on first use). A non-empty `capabilities` object replaces the whole declaration, so always pass this full set when it changes. The page watches `parent = CP-1521 AND (statusCategory != Done OR resolved >= -120d)` every 5 minutes for viewers with the Atlassian connector (fields summary, status, assignee, duedate, labels, resolutiondate, created, issuetype). It overlays status, assignee and whether the account is active, due date, labels, issue type, window label and resolution date, and adds tickets missing from the snapshot, classified in the browser with the same rules as `classify()` in `build.py`. New tickets added live have no description data until the next refresh. A second watch reads checklists: `parent = CP-1521 AND (labels = maintenance OR labels = radar) AND (statusCategory != Done OR resolved >= -30d)`, fields `description`, `responseContentFormat:"adf"`, every 5 minutes; `parseAdfChk` turns `heading` + `taskList`/`taskItem` (`attrs.state` TODO or DONE) into `chk`, kept in `CHK` by key. Response shape (observed): `{issues:[{key, fields:{...}}], isLast}`. The create call: `callTool("Atlassian Rovo","createJiraIssue",{cloudId, projectKey:"CP", issueTypeName:"Task", summary, description, contentFormat:"markdown", parent:"CP-1521", additional_fields:{labels:["maintenance"]}}, {cache:false})`; payload `{key, webUrl, fields}`. Never change these calls without observing a real request and response in the session.

### Design template

Fonts: Sora (display), IBM Plex Sans (body), IBM Plex Mono (numbers). Tokens on `:root`: `--brand #974fc7` (SambaNova docs primary), `--brand-ink #6d2fa3`, `--flame #e8702a` (today line and highlights), semantic `--ok --work --bad --info --idle` with `-bg` variants, neutrals with a purple bias. Logo: base64 of `logo/new-logo.png` (light) and `new-logo-dark.png` from the docs repo. Components to reuse: `.card/.card-h/.card-b`, `.pill` (ok, work, bad, info, brand, flame), `.tag`, `.chip[aria-pressed]`, `.kpi`, `.kc` (kanban card), `.tw > table`, `.drawer` via `openTicket(key)` / `openGuide(slug)`, `modeTag(m)`, `ext(href, text)`. Maintenance helpers: `tip(node, text)` (hover and aria explanation), `statPill(status)`, `tierTag(tier)`, `scoreTable(state)`, `cbar(ticket)`, `checklistSec(drawerBody, ticket)`, `draftTicket(item)`, `openCreate(item)`, the `TIP` map and `.mdlg` dialog styles. New pills and buttons on the Maintenance tab must go through `tip()` (rule 9). Semantic colours mean status only; never use red/green to encode anything that is not status (for feasibility or mode breakdowns use the single brand colour with plain-language labels).

## Workflows

Use a work folder in the scratchpad, e.g. `WORK=/tmp/ibm` in bash. Copy this skill's `scripts/` folder into `$WORK/scripts/` before running them (the scripts ship as files next to this SKILL.md).

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
1. **Jira list**: subagent runs `searchJiraIssuesUsingJql` with `parent = CP-1521 ORDER BY key DESC`, fields summary, status, assignee, created, resolutiondate, duedate, labels, issuetype, paging (`key < CP-xxxx`) until all are read, and writes `$WORK/jira.json` as `[{key, summary, status, owner (displayName without " [External]"), ownerOff (assignee.active is false), created (YYYY-MM-DD), resolved, due, slot (the int-* label or null), labels (all labels), itype (issuetype name)}]`.
2. **Descriptions**: subagent calls `getJiraIssue` (markdown) for every slotted ticket and every open ticket, writes `$WORK/jira_desc.json` as `[{key, summary, desc}]` verbatim.
3. **Docs**: request the docs folder, `git fetch`, then `REPO=<path> REVIEW='slug=origin/branch,...' SNAPSHOT=<today> python3 scripts/extract.py`. Find review branches with `git branch -r | grep CP-` and check which guides exist only on a branch. Update PR numbers in `build.py` PR from the open PR list.
4. **Radar metrics**: split the trending list into batches of about 15 and give each subagent the shields.io endpoints above; each writes `$WORK/metrics_<x>.json` as `[{name, repo, stars, commitsMonth, release, lastCommit, contributors, downloads}]`, values exactly as returned, null when unavailable.
5. **Competitors**: one subagent reads the competitor lists above and writes `$WORK/competitors.json` `{fetched, providers:[{provider, source, items:[{name,url}], notes}]}` with only names actually seen.
6. Run `trending.py`, `build.py`, `gaps.py`, `build.py` again (gaps needs data.json; build then embeds gaps), then `inject.py` into the page read from the artifact.
7. Review diffs that matter: new or closed tickets, status moves, new guides, new gaps, maintenance tickets that are new or not linked to an asset (add them to `MAINT_TICKETS`). Update PLAN for new slotted tickets (rule: mode and door only from the description). Publish and report what moved.

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

### G. Maintenance
1. **Label tickets.** Propose which CP-1521 tickets are maintenance, wait for the user's OK, then read each ticket's current labels and call `editJiraIssue` with `fields.labels` set to the existing labels plus `maintenance` (the call replaces the whole list). Verify with JQL `parent = CP-1521 AND labels = maintenance`.
2. **Create tickets.** People normally create them on the page with Create in Jira. When the user asks Claude instead (for example for approved proposals: `read_db` collection `mprop`, query `["status","eq","approved"]`), draft each with the asset's template in exactly the layout above, show the drafts, wait for an OK, then call `createJiraIssue` (project CP, Task, parent CP-1521, label `maintenance`, markdown). Read the ticket back to confirm parent, label and checkboxes. Add the key to `MAINT_TICKETS` if the summary will not match the asset name. Setting the proposal to `created` with `write_db` needs artifact ownership; otherwise matching titles hide it automatically.
3. **Change the inventory.** Edit `MAINT_TICKETS`, `MAINT_REPOS`, `MAINT_UPSTREAM`, `MAINT_TIER` or `MAINT_CONFIRMED` in `build.py` from what the user confirms, rebuild `data.json` (or edit `D.maint` and use workflow B), and publish.
4. **Change a cadence or the score.** Update `MAINT_CADENCE` in `build.py` and the vocabulary above. Tier texts in the legend read the cadence from the data; the score weights and thresholds are written in the "How the score works" card, the legend's score section and the How it works Maintenance paragraph, so update those for score changes.
5. **Ownership.** Flag open labelled tickets with no assignee or an inactive one; reassigning or closing them is a Jira edit (rule 5).
6. **Change a ticket template.** Edit `MAINT_TEMPLATES` (or `TPL_OF_KIND`) in `build.py` after the user agrees the wording, keep the four stage keys, rebuild or edit `D.maint.templates`, and publish. Existing Jira tickets keep their old checklist.

### H. Radar to Jira
1. **Create tickets.** People normally use Create in Jira on the Radar. When the user asks Claude instead, check for an open ticket naming the tool first, draft with the suggested template in exactly the layout above, show the draft, wait for an OK, then call `createJiraIssue` (project CP, issue type Story, parent CP-1521, labels `new-integration` and `radar`, markdown, no window). Read it back to confirm the parent, labels and checkboxes.
2. **Schedule.** Scheduling is a Jira edit: add the window label (for example `int-q1-2027`) only with the user's OK (rule 5). The ticket then leaves Not scheduled and joins the Board's roadmap, Timeline and delivery windows.
3. **Change a template or the route map.** Edit `RADAR_TEMPLATES`, `RADAR_ORDER` or `ROUTE_TPL` in `build.py` after the user agrees the wording; keep the five stage keys and the Category and Integration route lines; rebuild or edit `D.radarT`; publish. Existing tickets keep their old checklist.
4. **Refresh.** Radar tickets need no `PLAN` row: their category and route come from the description. Add a `PLAN` row only to override with confirmed facts (for example after the Evaluate stage settles the route).

## Verification checklist before publishing
- Every number on the page traces to a file in `$WORK` fetched this session (or the previous published data, unchanged).
- `node --check` passes; no `prefers-color-scheme` dark block; `[hidden]{display:none!important}` present.
- No em dash in text you wrote (`inject.py` warns).
- `D.maint.assets` is present and not empty; open `#maint` and check the queue and inventory render; the number of labelled tickets on the page matches Jira `parent = CP-1521 AND labels = maintenance`.
- `D.maint.templates` has all six templates and `stages` has four entries; a Create in Jira pop-up opens with a filled draft.
- Every new label on the Maintenance or Radar tab has a `TIP` or `TIP_R` entry and a legend row (rule 9).
- `D.radarT` has seven templates and five stages; a Radar Create in Jira pop-up opens with the suggested template; Stack rank shows Radar tickets without a window as Not scheduled.
- `python3 tests/check_build.py` passes (maintenance data, Radar templates and every ticket's type match the page).
- Test with a stubbed `window.claude` (db, user, mcp returning the observed shapes) in a headless browser: create success, `tool_error`, `server_not_connected`, an ambiguous error, and no connector; no page errors; no horizontal scroll at 390 px.
- Snapshot dates updated (`SNAPSHOT`, `DOCSREF`, `TRENDDATE`).
- Publish with `url`, omit `icon`, omit `capabilities` unless they change.
- After publishing, one functional check if storage code changed: write a probe doc, `ArtifactData list`, delete it with `if_version`.

## Orientation snapshot (5 Oct 2026, re-verify before use)
65 live guides (latest docs version v2.2.3), 3 in review (Langfuse CP-3074, LangSmith CP-3075, Zapier CP-3076), 38 slotted roadmap tickets CP-3074 to CP-3111 across Oct 2026 to Q2 2027, 168 child tickets in CP-1521, epic due 2027-06-30. Main owners: Gilvan Magalhaes (roadmap), Jorge Piedrahita (maintenance), Kwasi Ankomah (upstream providers), Luis Salazar, Rodrigo Maldonado. Upstream SambaNova providers merged without a guide: goose (CP-3008), smolagents (CP-3009), Hermes Agent (CP-3007), DeerFlow (CP-3006). Hermes Agent's 251k stars as reported by shields.io needs confirming.

Maintenance (8 Oct 2026): 15 tickets labelled `maintenance` (CP-3182 RooCode Oct, created from the page; CP-3181, CP-3170, CP-2979, CP-2961, CP-2937, CP-2692, CP-2691, CP-2652, CP-2505, CP-2475, CP-2413, CP-2330, CP-2293, CP-2157), 7 open: CP-3181 term-llm Oct (New, unassigned, first ticket made from a template, 0 of 9 checklist items), CP-3170 LiteLLM Oct (In Review), CP-2979 LangChain streaming (In Progress, Customer Defect), CP-2937 LiteLLM May (New, assignee inactive, likely superseded by CP-3170), CP-2652 pipecat (New, unassigned), CP-2475 AISK (New, assignee inactive), CP-2330 OpenHands (New, assignee inactive). Inventory: 71 inferred assets (13 critical, 17 high, 39 medium, 2 low), none confirmed yet. AISK has no repository link recorded.

Radar (8 Oct 2026): first roadmap ticket created from the Radar is CP-3183 "Firecrawl integration" (Story, labels `new-integration` and `radar`, Not scheduled, 0 of 10 checklist items). Ticket types now come only from labels: 127 New integration, 28 Other, 15 Maintenance in the snapshot.

## Scripts

The scripts live in `scripts/` next to this file. Run them with `WORK`, `REPO`, `SNAPSHOT`, `DOCSREF`, `REVIEW`, `TRENDDATE` set. Order for a full refresh: `extract.py`, `trending.py`, `build.py`, `gaps.py`, `build.py`, `inject.py`.

| Script | Reads | Writes |
|---|---|---|
| `extract.py` | docs repo (`REPO`, `REVIEW`) | `$WORK/guides.json` |
| `trending.py` | `$WORK/metrics_*.json` | `$WORK/trending.json` |
| `build.py` | `guides.json`, `jira.json`, `jira_desc.json`, `trending.json`, `gaps.json` | `$WORK/data.json` (the whole `D`, including `maint`) |
| `gaps.py` | `competitors.json`, `data.json` | `$WORK/gaps.json` |
| `inject.py` | a page and `data.json` | the page with its data block replaced |

The curated maps (OLDKIND, MODE_OVR, HOME, PLAN, PR, the MAINT_* maps, MAINT_TEMPLATES, TPL_OF_KIND, RADAR_TEMPLATES, RADAR_ORDER and ROUTE_TPL in `build.py`; M in `trending.py`; G and COVERED in `gaps.py`) are the only hand-maintained facts: change them only with evidence from an official source or the user's decision, and record the change in `CHANGELOG.md`.
