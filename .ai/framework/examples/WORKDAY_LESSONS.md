# Workday brownfield case: reducing repeated remediation

Reviewed 2026-09-11, using documentation in the Workday Integration repository. This is a process analysis of recorded findings, not a fresh audit of the current application. No Workday code, tests, database, external integration or deployment was changed or executed.

## Evidence and interpretation

| Source document | Recorded observation | Framework lesson |
| --- | --- | --- |
| `docs/v2/05_IMPLEMENTATION_PLAN.md`, sections 1 and 3; `09_AGENT_HANDOFF.md`, sections 5–8 | Existing instructions already call for vertical slices, acceptance gates and detailed handbacks. | More prose alone is unlikely to solve this; task-level scope and closure must be operational. |
| `docs/v2/21_ROUND_3_FINAL_CLAIM_INDEPENDENT_REJECTION_AND_REMEDIATION.md`, sections 4.1–4.4 | The review recorded a real worker/schema mismatch, missing migration parity, generated PASS ledgers, and proxy tests substituting for exact cases. | Test the actual entry point and authentic upgrades; link each criterion to its real assertion and result. |
| `docs/v2/22_POST_8C2B7F2_INDEPENDENT_REVIEW_AND_CORRECTIVE_ACTIONS.md`, sections 3–4 | A fix added the relation to fresh DDL/manual upload, while old V3 databases and API/retry/scheduler producers were missed. | Inventory all producers, consumers and upgrade paths before dispatch; close each boundary explicitly. |
| `docs/v2/30_UAT_AND_PRODUCTION_READINESS_IMPLEMENTATION_PLAN.md`, sections 7 and 14 | Shared eligibility must span service, UI, confirmation, nonce and final submission; real browser procedures and case-specific evidence are required. | Shared rules need wiring and consistency checks across every consumer, not isolated service tests. |
| `docs/v2/31_UAT_READINESS_IMPLEMENTATION_REPORT.md`, R3–R6 | CLOSED claims rely on repository filtering or presence of an admin command service; the report also correctly states NOT UAT READY. | Component existence is weaker than the user-visible journey required by the contract. Preserve the distinction between partial progress and closure. |
| `docs/v2/32_POST_A588452_UAT_READINESS_REMEDIATION_REPORT.md` | The file existed but was zero bytes when read on 2026-09-11. | File existence is not evidence content. Empty artifacts cannot support acceptance. |

The documents support the inference that missed integration boundaries, weak proof and broad closure claims contributed to repeated loops. They do not establish model capability as the sole cause, quantify time lost, or prove any listed defect still exists in the current code. The historical phase task breakdowns are explicitly superseded and are not the current Workday contract.

## Example task breakdown: durable job-to-artifact linkage

Illustrative only; the current Workday baseline and decisions must be inspected before issuing these tasks.

| Task | Bounded outcome | Touchpoints and decisive proof | Dependency |
| --- | --- | --- | --- |
| TASK-001 | Publish and migrate the durable relation | Canonical schema + real migration runner + authentic historical variants; preserve data and prove structural parity | None |
| TASK-002 | Manual upload passes exact artifact and metadata | Confirmation -> enqueue -> persisted relation; identical bytes from different candidates remain distinct | TASK-001 |
| TASK-003 | API acquisitions pass exact artifact and selection metadata | Every supported API producer -> queue; fixture acquisition verifies exact ownership and metadata | TASK-001 |
| TASK-004 | Retry retains the correct immutable input | Public retry route -> enqueue -> relation; wrong/missing/superseded input is handled according to contract | TASK-001 |
| TASK-005 | Scheduled acquisition produces one correctly linked job | Persisted occurrence -> acquisition -> queue; concurrency/restart prove idempotency and exact lineage | TASK-001, TASK-003 |
| TASK-006 | Real worker consumes only the declared relation | Actual registered worker -> repository -> parser/persistence; no ambiguous hash fallback, malformed-job isolation | TASK-001 |
| TASK-007 | Assemble and accept the supported journeys | Each supported entry mode/source through the real app/worker, on fresh and upgraded data; reconcile counts, lineage and no-live-call evidence | TASK-002 through TASK-006 |

Each task has detailed substeps and checks. The manager does not need to approve every line or function. A worker can implement and self-correct all agreed substeps within its turn, while the manager reviews one coherent outcome.

## Example shared policy coverage

For eligibility, explicitly map configuration creation -> dependency injection -> record display -> confirmation GET -> nonce POST -> transactional submission. For each required role/state/gate variant, compare visible eligibility, endpoint behavior and side-effect counts. If the gate changes after confirmation, the final boundary must re-evaluate it. A unit test of the evaluator alone cannot close this chain.

## Changes adopted in SimpleSDLC 1.1

- Manager-owned task matrix with touchpoints, dependencies, contract revision and exact check expectations.
- Worker preflight in the existing turn; discrepancies return as precise contract questions.
- Per-check worker results and manager acceptance, with explicit evidence locations and code identity.
- Structural rejection of uncovered touchpoints, stale handoffs, unresolved dependencies and unsupported acceptance.
- Root-cause review after two rejected submissions, and an explicit integration task before feature closure.

These changes are safeguards to validate in a real pilot, not a promise that future delivery will have no gaps.
