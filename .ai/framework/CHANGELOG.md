# Framework changes

## 1.3.0 — 2026-09-13

- Aligned the operating guide with discovery through release and post-release operation, preferring the next complete user outcome and learning before detailing future work.
- Added explicit human product-owner responsibilities, smallest useful release, measurable outcome targets and early user feedback in planning records.
- Added bounded investigations through the existing task/matrix/handoff system. Experiment execution, feasibility findings and prototype production readiness remain distinct.
- Expanded Manager reviews to challenge whether the plan and tests satisfy the original business goal, even when planned checks pass.
- Added an operations guide and on-demand record for ownership, recovery, deployment results, monitoring, outcome review and feedback routed to ordinary tasks.
- Added 1.2.0-to-1.3.0 migration guidance and record-preservation regression coverage.

The helper's runtime behavior and config/state/task-matrix schemas are unchanged. New investigation sections and operations records are created on demand. These workflow requirements rely on agents/humans reviewing content; automated structural checks do not prove their quality. See ALIGNMENT.md and VALIDATION.md.

## 1.2.0 — 2026-09-12

- Added the six-step human-operated workflow, including repository setup and fresh conversations.
- Added a master implementation-plan template and initialization mapping for module/phase sequencing, tasks, test plans and release gates.
- Added detailed test-procedure and per-plan execution-report templates with revision and evidence rules.
- Defined submission snapshots, optional review branches, correction routing and independent framework/plan/product versions.
- Added application delivery exclusions and a read-only `check-delivery` command for staged directories and ZIP/TAR files.
- Added bounded retries for Windows staging rename access/share errors during initialization/export; existing destinations are still refused and persistent failures are reported.

Config/state/task-matrix schemas remain version 1; manual dispatch, one active task and role ownership are unchanged. Existing installations require the additive upgrade steps in MAINTENANCE.md. Validation evidence and limits are recorded in VALIDATION.md.

## 1.1.0

Added task-level touchpoint/check coordination, contract revisions, evidence identity checks and recurring-failure diagnosis. See the existing 1.0.0-to-1.1.0 migration in MAINTENANCE.md.
