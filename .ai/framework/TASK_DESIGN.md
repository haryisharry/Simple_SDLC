# Task-level planning and coordination

The manager and worker coordinate through an explicit task contract and its coverage rows in `project/task-matrix.json`. Feature names and passing test totals are insufficient. The manager is responsible for identifying the work down to this level before dispatch.

## 1. Decompose by an independently verifiable outcome

Use this hierarchy: business outcome -> user journey -> bounded task -> observable checks across affected touchpoints. A touchpoint is a producer, consumer, entry point, storage boundary, configuration source, or deployment path affected by a change. It is not just a source filename.

Split a task when it contains independently acceptable outcomes, unsettled contracts, incompatible prerequisites, or too many scenarios for one focused review. Keep changes that must be consistent together. Several files may belong in one task; one function per task is not the goal. Do not require another manager round trip for each implementation substep.

Sequence foundational contract/migration tasks before their consumers. Reserve a final integration task to join the accepted slices through the actual application entry points. Individual task acceptance does not automatically accept the assembled feature.

## 2. Manager inventory before READY

Prefer a complete user outcome across relevant UI, backend and persistence boundaries when it fits a bounded review. Keep future tasks DRAFT until material decisions are settled; do not over-specify an entire roadmap before learning from the first increment. Use INVESTIGATIONS.md for risky assumptions: the experiment must be specified even when its answer is unknown. Downstream tasks require both accepted investigation evidence and the resulting recorded decision.

Inspect the real repository and record the search/read basis in `inventory_note`. For each changed rule or contract identify:

- All writers/producers: UI, API, import, retry, scheduler, CLI, background worker as applicable.
- All readers/consumers: service, real composition/entry point, UI, export, audit and operations.
- Fresh installation AND supported upgrade paths; real historical fixture provenance, existing data, constraints and rollback policy.
- Configuration creation, injection, consumers and final transactional rechecks.
- Roles, direct endpoint access, state transitions, failure/retry, duplicate/concurrent actions, restart and persistence behavior.
- Existing behavior to preserve and dependencies already accepted.

Record every affected touchpoint as `CHANGE` or `VERIFY_UNCHANGED`, with the reason. Every touchpoint needs a mapped check; “unchanged” is a verification decision, not an omission. The manager must justify excluded variants in the task. Do not blindly create a Cartesian product: enumerate required high-risk combinations, group equivalent cases with a reason, and explicitly cover interactions that can diverge.

In brownfield work, a passing fresh-database test cannot cover an upgrade, and a newly constructed test service graph cannot cover the real registered worker. Inspect those boundaries before implementation.

## 3. Prepare the contract and matrix

Create `tasks/TASK-NNN.md` from the task template and a matching task object in `task-matrix.json`. The task document contains the detailed procedure/substeps. The matrix contains stable IDs and compact, checkable links between scope, criteria, tests and review. Do not duplicate narrative specifications in the matrix.

Link the task from its module/phase in `project/implementation-plan.md`. Name assigned test-plan IDs, paths and revisions in the task and handoff; matrix checks reference the concrete procedure/scenario in `method` without adding schema fields. Follow TESTING.md for per-plan reports and test revision handling.

Each task object contains:

| Field | Meaning |
| --- | --- |
| `id`, `feature`, `revision` | Task identity, parent feature/journey identifier, positive contract revision |
| `depends_on` | Other task IDs that must be ACCEPTED before this task is dispatched |
| `scope_review` | DRAFT or READY; manager approval of the planned task coverage |
| `inventory_note` | Where the manager looked and why the touchpoint inventory is complete for this scope |
| `touchpoints` | Unique IDs, repository-relative paths, surface description, CHANGE/VERIFY_UNCHANGED and rationale |
| `checks` | Unique IDs, requirement criterion, scenario, touched IDs, method, mode and exact expected observation |
| `reviewed_code_identity` | Manager's accepted code snapshot; empty until acceptance |

Each check's `result` holds worker execution status, `contract_revision`, code identity, reason and evidence items (`path` relative to `.ai/project`, plus an exact test node/checkpoint/record in `locator`). Each check's `review` is manager-owned: PENDING, ACCEPTED or CHANGES_REQUESTED. Execution statuses: NOT_RUN, PASS, FAIL, BLOCKED, NOT_APPLICABLE. NOT_APPLICABLE requires a reason and manager acceptance; it must not be used to drop a required business behavior.

See `examples/task-matrix.example.json`. Initialization creates an empty matrix, not pretend tasks or preaccepted results. Task status remains in task metadata; the matrix does not hold a second copy of it. `state.json` mirrors only the active task status.

## 4. Readiness and worker understanding

Before READY, manager confirms: no material unresolved behavior; complete impact inventory; measurable positive and relevant negative checks; prerequisites/environment known; actual entry points and upgrade paths covered; expected evidence named. Set `scope_review: READY`, task `Contract: <revision>`, and the same `Contract` in the handoff.

At the beginning of its existing turn, the worker writes a short preflight note in its report: understood outcome, all touchpoints, intended substeps/checks and any mismatch found in the real code. This is not a mandatory extra manager approval round. If aligned, continue immediately. If a missing caller, contradictory rule or impossible test changes the contract, stop affected work and return the precise discrepancy to the manager.

For a reported defect, reproduce its failure before editing when practical. If reproduction is blocked, say so. Tests must assert the predetermined business/contract result, not copy the implementation's current output. Perform a final self-check of every matrix row before returning work.

## 5. Contract change and evidence invalidation

Only the manager changes criteria, touchpoints, exclusions or dependencies. Preserve the previous contract in `project/contracts/` and increment `revision`. Update task/handoff `Contract` and invalidate affected results/reviews to NOT_RUN/PENDING. When the shared code snapshot changes, assess whether prior checks still apply; do not reuse an earlier PASS merely because its file still exists. Acceptance requires PASS results to identify the same code snapshot as `reviewed_code_identity`.

A new business requirement is a scope change, not automatically a worker defect. A previously required but omitted boundary is a planning/implementation gap. Record which occurred rather than changing the target silently.

When a finding changes module/phase scope or sequence, archive and revise the master implementation plan as well. Keep task/test-plan revisions aligned in dispatch inputs; do not renumber past attempts or overwrite earlier evidence. GIT_WORKFLOW.md describes branch continuity and product versioning.

## 6. Review once across the agreed task scope

The manager reviews every planned check and relevant cross-boundary effects, gathering findings into one actionable review where practical. Distinguish requirement gap, missed touchpoint, implementation defect, inadequate test, invalid evidence, environment block and new scope. Preserve accepted behavior and name affected checks for each correction. Stop early only when an invalid baseline makes remaining review unreliable; state what was not reviewed.

The worker reports exact per-check outcomes; the manager owns per-check acceptance. An ACCEPTED task requires every check to have an accepted PASS or an explicitly approved NOT_APPLICABLE disposition. Missing/broken/empty evidence is not closure. The helper verifies structural links, not the truth of a test, screenshot, or narrative.

After **two rejected submissions for the same task**, or sooner for a repeated symptom, stop the patch-only loop. The manager records a root-cause review and changes the method: reproduce first, rediscover producers/consumers, repair the contract, split the task, add a missing integration check, or resolve a specific environment issue. Do not send the same broad repair prompt again. This threshold triggers diagnosis, not abandonment or forced human approval.

## 7. Feature closure and efficient continuation

Challenge the contract against the original business outcome and actual user journey: identify assumptions shared by the design and tests, missing behavior and contradicting user/operational evidence. Use the review template's business-outcome assessment even when every planned check passes. A material flaw in the agreed outcome prevents full acceptance until resolved through the appropriate contract/decision path. Separate newly requested scope from previously required behavior that was overlooked; do not silently expand the task or weaken expectations. A new conversation alone is not independent verification.

List every required task and the final integration/journey task in traceability. A feature remains incomplete while any required task, integration check, environment qualification or human acceptance gate is pending/blocked. An accepted safe interim behavior does not mean its decision-blocked production variant is complete.

Use targeted checks during implementation and the planned affected regression at handoff. Run the broader suites at the feature/release gates in the project test plan or when impact demands them. Existing project-mandated suites still apply. Preserve the latest accepted evidence and review the delta plus affected boundaries, rather than restarting a whole-project audit after every tiny correction.

No matrix can guarantee zero implementation gaps. Its purpose is to expose omitted boundaries before dispatch, make closure reviewable, and turn recurring failures into a change in the process.
