# Version 1 validation record

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
