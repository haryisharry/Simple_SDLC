# Test planning and evidence

Define relevant checks before implementation, then record what actually executed. Use the repository's normal test structure and tools; the framework prescribes evidence, not a programming language or test runner.

| Layer | What to establish |
| --- | --- |
| Static/build | Syntax, type checks, lint/build/package checks appropriate to the repository |
| Unit | Business rules and meaningful boundary cases in isolation |
| Function/component | Behavior of a function, service, or UI component with its local dependencies |
| Feature | Acceptance criteria across the full feature behavior |
| Integration | Database/filesystem/service contracts; distinguish local stubs from real environment qualification |
| End-to-end | Complete user journeys through the actual UI/API, including relevant roles and persisted results |
| Regression | Existing supported behavior preserved by the change |
| Nonfunctional | Relevant security, accessibility, performance, recovery, and concurrency requirements |
| Human UAT | Named human execution/acceptance of business journeys in an identified environment |

For each planned check use PASS, FAIL, NOT_RUN, BLOCKED, or NOT_APPLICABLE. NOT_APPLICABLE requires a reason reviewed by the manager. An unavailable browser, VM, credential, or service is NOT_RUN/BLOCKED, never PASS. Automated journey tests do not replace human UAT.

## Procedures before dispatch

The Manager maintains `project/testing/plan.md` as a coverage index linked to the master implementation plan. Use stable `TESTPLAN-NNN` IDs and positive revision numbers. Create `testing/plans/TESTPLAN-NNN.md` from `templates/test-procedure.md` for substantial plans. Each assigned scenario needs requirements/task-check mappings, environment/role/fixture prerequisites, ordered reproducible steps, predetermined expected observations, pass/fail criteria, evidence locations and cleanup. Performance checks specify workload and measurable thresholds; security checks specify threat/permission expectations. Run only authorized environment effects.

Before READY, name procedure paths and revisions in the task and handoff, and map their scenarios to matrix checks. Use exact commands once the stack is established; do not leave execution-critical placeholders for the worker to guess. For tiny changes, a complete inline procedure in the index/task and an identified per-plan section in the worker report is sufficient. Scale documentation to risk without dropping the evidence contract.

## Per-plan execution and revisions

The worker creates `testing/reports/TESTPLAN-NNN-rRRR-TASK-NNN-attempt-NN.md` from `templates/test-report.md` for every assigned plan execution, including failed/blocked attempts. Report all assigned scenarios with actual observations and raw artifact locators; identify partial executions. Link these from the implementation report and matching matrix results. The Manager maintains the index's report links and reviews the results. Human UAT records still require actual human statements in `testing/uat.md`.

Before changing an approved procedure or expected outcome, the Manager archives the previous plan under `project/contracts/TESTPLAN-NNN-rRRR.md`, increments its revision, records the reason and identifies affected task checks. Archive index-only procedure changes as `contracts/test-index-rRRR.md`. Revise affected task contracts and handoffs, then invalidate affected results/reviews to NOT_RUN/PENDING under TASK_DESIGN.md; retain old reports. Adding execution links alone does not revise a plan. The helper does not validate procedure content/revisions or enforce this archival rule; review these explicitly.

## Execution evidence

Minimum execution evidence:

- Requirement/acceptance-criterion IDs and test/check identifiers.
- Exact command or manual steps; working directory; timestamp; environment/tool versions when material.
- Exit status and observed result; artifact path for logs/screenshots where useful.
- Git commit plus dirty-tree status and changed-file/diff identity, or a reproducible file-hash manifest if Git is absent. A commit alone does not identify uncommitted changes.
- Baseline failures, skipped checks, external mocks/stubs, and environment limitations.

For dirty trees record changed/untracked relevant files and preserve a patch or hashes, excluding secrets and generated noise. Reviewers must compare that identity with the actual code being accepted. Changes after a check require the manager to assess and rerun affected verification. Do not rerun unrelated expensive suites without a reason.

Human UAT records need the participant's actual statement/date, role, journey, environment, result, and remaining issues. Models may prepare scripts and transcribe human answers with attribution; they must not invent signatures or approval.
