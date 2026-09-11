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

For each planned check use PASS, FAIL, NOT_RUN, BLOCKED, or NOT_APPLICABLE. NOT_APPLICABLE requires a reason reviewed by the manager. A unavailable browser, VM, credential, or service is NOT_RUN/BLOCKED, never PASS. Automated journey tests do not replace human UAT.

Minimum execution evidence:

- Requirement/acceptance-criterion IDs and test/check identifiers.
- Exact command or manual steps; working directory; timestamp; environment/tool versions when material.
- Exit status and observed result; artifact path for logs/screenshots where useful.
- Git commit plus dirty-tree status and changed-file/diff identity, or a reproducible file-hash manifest if Git is absent. A commit alone does not identify uncommitted changes.
- Baseline failures, skipped checks, external mocks/stubs, and environment limitations.

For dirty trees record changed/untracked relevant files and preserve a patch or hashes, excluding secrets and generated noise. Reviewers must compare that identity with the actual code being accepted. Changes after a check require the manager to assess and rerun affected verification. Do not rerun unrelated expensive suites without a reason.

Human UAT records need the participant's actual statement/date, role, journey, environment, result, and remaining issues. Models may prepare scripts and transcribe human answers with attribution; they must not invent signatures or approval.
