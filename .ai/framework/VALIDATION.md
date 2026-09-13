# Version 1 validation record

## Current release: 1.3.0

Date: 2026-09-13. Environment: Windows, Python 3.14.0. Command: `python -B -m unittest discover -s .ai/tests -v` from the distribution root. Result: **39 tests passed**, exit code 0, unittest duration 3.902 seconds. Captured output: [v1.3.0-unittest.txt](evidence/v1.3.0-unittest.txt).

The previous 38 scenarios remain covered; the new scenario simulates 1.2.0 records with an accepted task and evidence. It verifies that changing the framework version preserves every other record byte-for-byte and changes no other configuration field. It also verifies that operations/investigation records are not required merely to initialize or upgrade. The existing 1.1 record reconciliation scenario now targets 1.3.0. These are structural migration simulations, not proof of reconciled business content.

Tested file SHA-256 identities (working tree; no release commit/tag created):

| File | SHA-256 |
| --- | --- |
| tools/sdlc.py | 2C450C7B269F167690D0C06FC21A5B72F4F47315481B56225FF5A56B2C1F8694 |
| tests/test_sdlc.py | 0641469E2D3F6A3EFD83D288A673A60564B830234878AD29907019EAC8A20B3D |

Manual document review mapped the revised source idea to startup paths, role ownership, discovery/master-plan templates, investigation acceptance, business-outcome review, release/operations records and upgrade instructions in ALIGNMENT.md. The helper runtime and schemas are unchanged from 1.2.0. Git whitespace checks passed for `.ai`; the distribution remains uninitialized with no disposable test directories left over.

Limits: no real two-model delivery pilot, feasibility experiment, human UAT, deployment, restore exercise or post-release monitoring was performed for this release. The illustrative investigation in INVESTIGATIONS.md is not executed evidence. Plan quality, experiment validity, actual human authority and operational readiness require content/evidence review; none is proven by the passing helper suite. The earlier 1.2.0 validation limits continue to apply.

## Historical validation

Date: 2026-09-11
Environment: Windows, Python 3.14.

Command from the distribution's project root:

```text
python -B -m unittest discover -s .ai/tests -v
```

Result: 17 tests passed. The suite uses disposable copies; the distribution remains uninitialized.

Covered behavior:

- Greenfield and brownfield initialization; existing application files preserved.
- Reinitialization refusal and cleanup after failed initialization.
- Clean export excluding project-specific history, with fresh project identity on initialization.
- Rejection of existing/nested export destinations and detection of an initialized folder copied into the wrong project.
- Simulated manager-to-worker-to-manager handoffs, correction/resubmission, and task acceptance.
- Missing reports/reviews, task/state and recipient inconsistencies, unfinished worker task placeholders.
- Human-decision state, malformed JSON, task path validation, schema/timestamp checks, configurable model labels.
- Command-line initialization and validation from a different working directory.

The first run encountered Windows access-denied errors caused by Python temporary-directory permissions in this restricted session. Staging now uses uniquely named directories inheriting workspace permissions; the tests passed after that correction.

Not established by this suite: real model adherence, an actual two-application feature delivery, manager review quality, external environment qualification, human UAT, or production readiness. Run a small pilot feature with both configured agents before relying on the workflow for a substantial project. Symbolic-link rejection is implemented but was not exercised in this Windows test run.

## Version 1.1.0 — task-level coordination

Date: 2026-09-11. Same environment and test command. Result: **29 tests passed**, including the original 17 scenarios adapted to the task-matrix contract and 12 new scenarios.

New scenarios verify that the checker rejects:

- Worker execution before manager scope readiness.
- An affected touchpoint without a mapped check.
- Task/handoff contract revisions that disagree with the matrix.
- A passing result from an earlier contract revision.
- A task document missing from the matrix.
- Dependency cycles, unknown dependencies and dispatch before dependency acceptance.
- Empty evidence and evidence references outside project records.
- Task acceptance without every check being reviewed and adequately dispositioned.
- Evidence for a different code snapshot from the manager's accepted snapshot.
- Duplicate check IDs.

The real-case review in examples/WORKDAY_LESSONS.md informed these safeguards. Workday application code/tests were not executed in this review. No measured reduction in correction rounds or real-agent pilot success is claimed. Root-cause review after two rejected submissions, exhaustive impact discovery, role ownership and honest evidence remain instructions for the agents/human, not automatically enforced runtime behavior.

## Version 1.2.0 — workflow, planning and delivery

Date: 2026-09-12. Environment: Windows, Python 3.14. Final command from the distribution root:

```text
python -B -m unittest discover -s .ai/tests -v
```

Final result: **38 tests passed**, exit code 0, 3.286 seconds reported by unittest. This includes the original 29 tests and nine added scenarios; greenfield initialization coverage also now verifies the draft master plan and framework version.

Added coverage:

- Additive 1.1.0-to-1.2.0 record reconciliation preserves active state, task contracts, handoff and the existing test index. Missing master plan/version mismatch are detected before reconciliation. This is a structural simulation, not validation of a populated project's planning content.
- Delivery directory inspection accepts a clean fixture and rejects nested mixed-case `.ai` records without modifying them.
- ZIP/TAR member inspection handles clean and contaminated fixtures; ZIP cases also cover Windows-style separators and parent traversal.
- ZIP symbolic links and TAR symbolic/hard links are rejected without extraction.
- Missing, empty and unsupported/corrupt-format inputs fail inspection.
- The delivery CLI returns success/failure appropriately without requiring project initialization and states its nested-archive limitation.
- Windows staging retries recover from a simulated transient rename error, stop after four failed attempts and refuse a destination created by a competing writer.

Earlier attempts in this session are retained here as failures: the first 36-test run returned exit 1 with 35 passing tests and one `PermissionError: [WinError 5] Access is denied` at `staged.rename(project)` during initialization. An approved run outside the sandbox returned exit 1 with 33 passing tests and three such errors during initialization/export. These failures moved between tests; their OS-level cause was not established. The helper now retries only Windows error codes 5/32/33, up to four rename attempts with 0.1/0.2/0.4-second waits, checks the destination before every attempt and reports persistent failures. The final 38-test run passed in the normal execution environment.

Document review checked startup paths, template/init mappings, module/task/test-plan ownership, revision preservation, branch continuation, additive upgrade steps and release packaging gates. These are protocol instructions, not automatic enforcement. No actual two-model feature-delivery pilot, human UAT, external qualification, application release package or container image was executed/qualified here. Filesystem symlink/junction and hard-link cases were not exercised on this Windows host; archive link cases were tested. Delivery inspection checks names/types only, not payload integrity, nested archive contents or application completeness. The distribution remains uninitialized for reuse.
