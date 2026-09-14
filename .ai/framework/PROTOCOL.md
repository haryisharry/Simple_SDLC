# Operating protocol

## Authority and ownership

Human instructions and applicable repository rules constrain this workflow. The human transfers prompts and ensures the previous agent has stopped. `active_role` is a convention, not a process lock. Never run two writing sessions simultaneously, including two manager sessions.

| Records | Owner |
| --- | --- |
| Brief, requirements, design, decisions, traceability, master implementation plan, test index/procedures, acceptance/review | Manager |
| Application implementation, executable tests, implementation/per-plan execution reports, execution evidence | Worker |
| Task execution status and report links | Worker during its turn; manager during review |
| State and current handoff | Outgoing actor, updated together before stopping |
| Human decisions and UAT signoff | Human; manager may transcribe with explicit attribution |
| Business priorities, outcome targets, release/operational authority assignments | Human product owner; manager records attributed decisions |
| Investigation contracts and decisions; operations plans and feedback triage | Manager |
| Experiment evidence and deployment/operational execution reports | Worker or authorized human operator; manager may transcribe with attribution |
| Framework instructions/templates | Maintainer; only change as an explicit framework task |
| Task matrix: scope, dependencies, checks, revision, per-check review | Manager |
| Task matrix: assigned checks' result records | Worker during execution; manager may invalidate stale results with a recorded reason |

Manager writes are limited to `.ai`. Read access includes the entire project. Manager verification must not intentionally modify application source, snapshots, dependencies, or generated application artifacts. Redirect test reports to `.ai/project/evidence/` where supported; delegate checks with intentional writes or external effects. Ordinary ignored runtime caches can occur during read-oriented checks. These rules require agent cooperation; they are not an OS sandbox.

Follow GIT_WORKFLOW.md for optional review branches and application checkpoints. The human/assigned worker performs Git mutations involving application files; the Manager inspects the submitted code and writes its planning/review records inside `.ai`.

The product owner uses the existing `human` actor; no third model is required. Investigations and operations changes use the same task/handoff ownership and acceptance rules. Experimental findings may disprove a design even when the investigation task is accepted. Feedback becomes work through Manager triage and ordinary task preparation, not a second independent queue. See INVESTIGATIONS.md, OPERATIONS.md and roles/PRODUCT_OWNER.md.

## Shared state

`project/state.json` is the machine-readable current position, not a replacement for evidence. `schema_version` is 1. Allowed actors: `manager`, `worker`, `human`. Allowed task states:

| State | Meaning / allowed next step |
| --- | --- |
| `NONE` | Manager discovery; no active task |
| `DRAFT` | Manager preparing a task; may become READY |
| `READY` | Manager-defined work ready for worker; may become IN_PROGRESS |
| `IN_PROGRESS` | Worker executing; may become SUBMITTED or BLOCKED |
| `SUBMITTED` | Returned to manager; may become ACCEPTED, CHANGES_REQUESTED, or BLOCKED |
| `CHANGES_REQUESTED` | Manager review issued; worker may resume IN_PROGRESS |
| `BLOCKED` | Explicit obstacle recorded; manager resolves or asks human before resuming |
| `ACCEPTED` | Manager accepted this task; does not imply project completion or human UAT |

Keep the task's metadata status equal to `task_status`. One active task at a time in v1. Historical tasks remain in `tasks/`; switch `active_task` only after accepting the previous task or recording an explicit deferral in decisions. Acceptance can be revoked by a new review if later evidence invalidates it. Do not erase old reviews.

## Task contract

Use `templates/task.md`. Every task has a unique `TASK-NNN` ID, an objective, allowed scope, relevant inputs, observable acceptance criteria, required checks, and expected deliverables. Manager tasks can cover requirements/design without application coding. Worker execution tasks need an actionable contract, not “build the entire app” with unspecified behavior.

Follow `TASK_DESIGN.md` to prepare the task-level coordination matrix. Every task document has a matching `project/task-matrices/TASK-NNN.json` shard. The root task-matrix.json is a storage descriptor only. The manager inventories integration boundaries before dispatch and owns check-by-check acceptance. Matrix check IDs are unique within each task; cite them as TASK-NNN/CHK-ID.

The first lines of each task are plain metadata used by the helper:

```text
ID: TASK-001
Status: READY
Contract: 1
```

Use only `TASK-` followed by at least three digits. Filename is `TASK-001.md`. Reports/reviews use `TASK-001-attempt-01.md`, incrementing the attempt each time. Preserve prior attempts. Add report/review paths to the task.

## Manual transfer transaction

1. Finish the current action and write its evidence/report/review.
2. Update task status and links. Append decisions and traceability changes where applicable.
3. Copy the outgoing `handoffs/current.md` to `handoffs/history/HANDOFF-NNN.md` using its ID. Never overwrite an existing history file. The initial file uses `HANDOFF-000`.
4. Create the next `current.md` from the handoff template with a new ID, explicit `To: manager`, `worker`, or `human`, and `Task: TASK-NNN` or `none`.
   Include `Contract: <matrix revision>` for a task, or `Contract: none` during discovery without a task. A stale revision cannot be dispatched.
5. Update `state.json` last: actor, task, status, stage, handoff path, summary, and UTC timestamp. Run `check --ready` and resolve inconsistencies before presenting the transfer.
6. Give the human a short next-session prompt and stop. Updating files does not dispatch another agent.

When blocked, always return to manager first. If the manager needs a human decision, record the precise question, options/tradeoffs if useful, and how work resumes; set actor to human. The human's reply in the manager conversation explicitly authorizes that manager to record the answer and restore `active_role: manager`. For a new manager session, include the answer in its startup prompt. Do not infer an answer from elapsed time.

## Interrupted sessions

If a session ends mid-update, do not trust state alone. Compare task metadata, current handoff, latest report/review, and actual working tree. Record the interruption and reconcile the records using evidence. Ask the human if writer ownership is uncertain. Resume an IN_PROGRESS worker task only after confirming the prior worker stopped. Never rerun migrations, deployment, or external writes merely because a report is missing.

## Context and evidence hygiene

MEMORY.md defines mandatory working-record byte/line limits for all project file types, partitioning/rotation rules and bounded retrieval. `check --ready` rejects oversized working records. Only load current routes and task-specific pages; neither a full matrix nor cumulative decision/traceability/plan history belongs in startup context. Preserve cold evidence and original records, with exact locators and links, rather than dropping coverage or accepted results to fit a budget.

Read entry points and current records first, then follow task-specific links. Link large logs rather than pasting them into every handoff. Store raw test artifacts in normal ignored locations or `.ai/project/evidence/`; record stable paths, commands, timestamps, and code identity. Do not store secrets or sensitive real customer data. Summaries do not supersede approved requirements or raw results.
