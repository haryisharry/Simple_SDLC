# Keep project memory bounded

Project history can grow indefinitely; the material loaded into an agent session must not. Use small current records, deterministic paths, partitioned working documents and paged access to historical evidence. Do not shrink context by deleting requirements, dropping checks, hiding failures or resetting acceptance.

## Storage and enforced limits

| Record | Layout and limit |
| --- | --- |
| Root project records and current handoff | At most 8,192 bytes AND 120 lines per file; current summaries/routes only |
| Task matrices | One object per `task-matrices/TASK-NNN.json`; at most 49,152 bytes AND 600 lines |
| Other working records, including custom files | At most 49,152 bytes AND 600 lines per file; root limits apply at project root |
| Cold history | `history/`, `contracts/`, `handoffs/history/`, and the exact migration backup `task-matrices/legacy-v1.json`; retained, never read in full by default |
| Raw evidence | `evidence/`; retained at its natural size, retrieved by exact locator or bounded pages; binary artifacts use appropriate inspection tools |

Both `check` and `check --ready` reject oversized working files before structural validation, covering all file extensions. `memory-check` performs the size scan alone. These fixed limits are guardrails, not token estimates. Do not minify JSON or compress narrative to evade them. Partition before a limit is reached. Diagnostics print at most 30 entries per run, each capped at 400 characters; fix those and rerun to see the remainder.

`task-matrix.json` is now a constant-size storage descriptor:

```json
{"schema_version": 2, "storage": "task-matrices"}
```

It contains no growing list of tasks. Each shard contains the original task object (id, revision, dependencies, touchpoints, checks and results) without a wrapper. Copy `templates/task-matrix-entry.json` when adding a task. The filename must match its ID. Keep task status in `tasks/TASK-NNN.md` and active state in state.json as before. Never combine all shards into an agent prompt. Full machine validation still audits cross-task dependencies, revisions and evidence; its work scales with history, but the agent receives bounded diagnostics.

## Start and retrieve only what is needed

```text
python .ai/tools/sdlc.py context
python .ai/tools/sdlc.py read-record state.json
python .ai/tools/sdlc.py read-record handoffs/current.md
python .ai/tools/sdlc.py read-record task-matrices/TASK-001.json
python .ai/tools/sdlc.py tasks --limit 20
python .ai/tools/sdlc.py tasks --after TASK-020 --limit 20
python .ai/tools/sdlc.py memory-check
```

`context` returns paths for the active task, not historical contents. It does not replace `check` or verify that a handoff is trustworthy. `tasks` lists IDs in lexical order with a continuation cursor; use the returned cursor exactly (IDs of different numeric widths need not sort numerically). It prints at most 50 IDs, default 20, without creating a saved global catalog.

`read-record` reads at most 12,000 bytes of one project-relative file and prints the next byte offset and whether more remains. Continue only when the task requires it: `read-record PATH --offset RETURNED_OFFSET`. It never silently treats the first page as the complete document. A page boundary can split a UTF-8 character, rendered as a replacement character; use a small overlap to inspect it. Binary files need their normal tools. Without Python, use bounded reads/search with explicit limits and manually apply these budgets; never dump whole directories or cumulative logs.

Startup context should ordinarily fit within 24,000 bytes of project-record excerpts before implementation-specific source inspection. This aggregate reading budget is a protocol rule, not automatically enforced across tools or messages. Stop and follow a narrower task-specific link when more is needed; do not concatenate every individually small file. Apply the same selective reading to application source and large framework examples/tests.

## Partition every accumulating record

| Growing content | Keep current | Move detail to |
| --- | --- | --- |
| Decisions | Active global constraints and relevant decision IDs/links in decisions.md | One decision per `decisions/DEC-NNN.md`; unchanged old snapshots in history |
| Traceability | Current feature routes, unresolved release gates and links | `traceability/FEATURE-ID/PAGE-NNN.md`, with bounded criterion/task rows |
| Master implementation plan | Current release, next increment, unresolved blockers, stable links | `plans/RELEASE-ID/PHASE-ID.md` and bounded page files |
| Requirements/design | Current entry points and relevant assumptions | Per feature/module files and bounded subdocuments |
| Test index/procedures/UAT | Current gate and scenario routes; actual acceptance summary | Per-plan/scenario/role files and numbered execution reports; raw results in evidence |
| Reports/reviews | One task attempt and concise observations/links | Additional numbered parts for large attempts; raw logs in evidence |
| Operations/feedback | Current owners, runbook routes, open incidents and next review | Per release/incident/outcome records with linked evidence |
| Handoffs/state | Only the current actor, task, summary and next inputs | Numbered handoff history; never append prior conversations to state |
| Any new custom record/index | Current scope and direct routes | Partition by stable domain ID, then numbered pages if necessary |

Indexes themselves must not become growing lists of every historical item. Use deterministic paths, bounded parent/next-page links, targeted search and paginated task listing. Keep unfinished required work discoverable through the current release/feature routes; moving it to another file does not complete or defer it. Preserve global constraints and the consequences of old decisions in the active routes even when their full rationale is cold.

When a task shard itself grows too large, first remove repeated narrative by linking precise design and procedure sections. If it still cannot fit, the Manager decomposes independently reviewable outcomes, retains shared invariants and a final integration gate, and revises contracts/dependencies explicitly. Never drop matrix rows merely to pass the budget check.

## Rotate safely before handoff

The owning role checks sizes during work and before transfer. Preserve the original document in an immutable history path before restructuring it; create bounded detail files and replace the former entry point with a concise current summary and routes. Update incoming links and exact evidence locators affected by the move. Prefer keeping old evidence at its original path when acceptance references it; additional historical indexing need not move it.

Review the restructure for lost constraints, unresolved tasks and evidence. Storage-only changes do not invent results or reset accepted tasks. If meaning changes, follow normal contract revision and evidence invalidation rules. Run `check --ready` after restructuring. No generic tool automatically summarizes arbitrary requirements: an automatic cut could discard the very rule needed for correct implementation.

## Legacy matrix migration

Stop the other writer, version/back up the project, then run `python .ai/tools/sdlc.py migrate-matrix`. The command preserves every task field, writes one shard per ID, retains the exact original bytes at `task-matrices/legacy-v1.json`, and replaces the descriptor last. It does not modify task documents, status, config, results or evidence. Duplicate IDs, unexpected top-level fields and conflicting existing shard directories are refused instead of being discarded.

If interruption occurs after shards are published but before descriptor replacement, rerun the command: it resumes only when the original backup and every shard match the still-current legacy matrix. If records differ, preserve both and reconcile manually. Repeated invocation after completion is a no-op. Oversized individual shards remain intact after migration and must be partitioned before handoff. Migration restructures storage; it does not approve existing contracts.

Small v1 matrices remain readable by the full checker during upgrade; active context routing requires v2 storage. No framework can prevent an agent from bypassing instructions and reading an entire file with another tool, or stop an external writer from creating a huge file. These changes detect excessive working-record growth, cap helper retrieval/output and remove the need for cumulative startup reads; they do not promise constant-time full-project audits or universal model compliance.
