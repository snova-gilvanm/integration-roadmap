# Changelog

Versions of the `integration-backlog-monitor` skill for the Integrations Roadmap artifact
(https://claude.ai/artifact/MV2P1NUii2NkA5hMSXGbRL). Newest first.

## 2.2.0 (2026-10-08)

Page
- Radar: Create in Jira on Trending tools, Competitor gaps and the Signals log, shown only when no open
  ticket names the tool ("In Jira: CP-xxxx" otherwise). The pop-up suggests one of seven templates from
  the tool's expected route (OpenAI-compatible config, Upstream provider PR, Provider already upstream with
  the guide missing, SambaNova package or plugin, Partner or commercial, Cookbook, Route unknown) and
  drafts the ticket from the Radar's data. Tickets are Stories under CP-1521 labelled `new-integration`
  and `radar`, with no window. Viewers without the connector get Approve for Jira.
- Radar legend ("What the labels mean") and hover explanations (`TIP_R`) on the Radar's labels.
- Stack rank lists Radar tickets without a window as Not scheduled; the Board counts them as roadmap.
- Checklists of Radar tickets are read from Jira; Checklist behind uses the five Radar stages.
- Ticket types come only from Jira labels: Maintenance, New integration or Other (change made directly
  on the page before this release; folded into the skill here).
- Fixes: long Stack rank titles no longer overflow on phones; long legend labels wrap.

Skill
- `build.py`: `classify()` uses labels only; `RADAR_TEMPLATES`, `RADAR_STAGES`, `RADAR_ORDER`,
  `ROUTE_TPL` produce `D.radarT`; `structured()` reads the Category and Integration route lines into
  `cat` and `modes` for tickets without a `PLAN` row; checklists parsed for `radar` tickets too; the
  unlinked-maintenance warning uses the page's name rule.
- Rule 9 covers the Radar tab. New workflow H (Radar to Jira). Vocabulary, collections (`rjira`),
  capabilities (second watch includes `radar`), verification and orientation updated.
- `tests/check_build.py` also checks `D.radarT` and every ticket's type; path follows `.claude/skills/`.

Data
- CP-3183 "Firecrawl integration" (first Radar ticket) and CP-3182 "RooCode maintenance, Oct 2026"
  (first ticket created from the Maintenance tab by a teammate).

## 2.1.0 (2026-10-08)

Page
- "What the labels mean" legend on the Maintenance tab, hover explanations on every label (`TIP`),
  a live worked score example and a per-asset "How this score was calculated" table.
- "Create in Jira" pop-up: drafts the ticket from the asset's template (editable), creates it with
  the viewer's Atlassian connector (new capability tool `createJiraIssue`), and handles each error code.
  Viewers without the connector keep "Approve for Jira" ("Approved, not in Jira yet").
- Jira checklists: tickets get `- [ ]` checkboxes grouped by stage (To do, In progress, In review,
  Before closing). The page reads them live (second watch, ADF), shows "Checklist d of n" and flags
  "Checklist behind" when the status is ahead of the checklist.
- Team proposals hide themselves once a labelled ticket with the same title exists for the asset;
  otherwise they note the open ticket.
- Fallback when `D.maint` is missing; legend cadence texts read from the data.

Skill
- New golden rule 9: every label on the Maintenance tab has a plain-language explanation.
- Scripts moved out of SKILL.md into `scripts/` (SKILL.md 732 to 188 lines).
- `build.py`: `MAINT_TEMPLATES`, `MAINT_STAGES`, `TPL_OF_KIND`, `tpl` per asset, checklist parsing
  from descriptions (`parse_chk`), term-llm linked to CP-3181.
- Workflow G2 (create tickets) and G4 updated, new G6 (change a template); verification checklist
  covers templates, rule 9 and stubbed connector tests.

Data
- CP-3181 "term-llm maintenance, Oct 2026" created from the upstream template; 14 labelled tickets.

## 2.0.0 (2026-10-06)

- Maintenance tab: KPI tiles, queue (Jira tickets labelled `maintenance` plus proposals),
  inferred asset inventory with tiers, cadences (critical 2, high 3, medium 6, low 12 months),
  score (criticality 40, exposure 30, urgency 30), six-month schedule.
- `D.maint` data block, ticket fields `labels`, `itype`, `ownerOff`, collections `mprop` and `mexp`.
- Live Jira overlay adds tickets missing from the snapshot.
- Maintenance identified only by the Jira label `maintenance` (13 tickets labelled on 2026-10-06).
- Workflow G (maintenance). Renamed to `integration-backlog-monitor-v2`; v1 disabled.

## 1.x

- Original skill by Gilvan Magalhaes: Overview, Board, Timeline, Catalog, Stack rank, Radar,
  How it works; full refresh pipeline (extract, trending, build, gaps, inject).
