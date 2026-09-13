# Development lifecycle

Use these stages iteratively for features. Work can return to earlier stages when evidence changes the design. Match document depth to risk and scope; record the reason when a stage/check is not applicable. Tiny fixes may use one concise specification, while larger features need separate artifacts.

| Stage | Manager output / gate before progressing |
| --- | --- |
| Discovery | Brief and repository assessment; product owner, smallest useful release, baseline/target outcome measures, users, scope, constraints, unknowns, brownfield baseline |
| Requirements | Stories, business rules, observable acceptance criteria, role matrix, nonfunctional needs, exclusions |
| Design | Material feasibility assumptions investigated where needed; feature behavior, UX journeys, UI states, architecture, contracts, persistence, access rules, migration and rollback where relevant |
| Planning | Master implementation plan by module/phase, test index and detailed procedures, task contracts/matrix, inspected touchpoint inventory, dependencies, measurable checks and bounded first task |
| Implementation | Worker code, tests, execution report; task submitted for review |
| Verification | Manager review of exact code state, evidence and the plan's fitness for the original business outcome; corrections or task acceptance |
| UAT | Human exercises agreed role-based journeys; feedback and explicit signoff recorded |
| Release | Readiness assessment, final delivery artifact inspection excluding `.ai`, known issues, deployment/rollback/runbook, human release decision |
| Maintenance | Named operational owners, monitoring/incident response, measured business outcomes and user feedback, regressions, dependency/schema changes, renewed tasks |

Requirement/design checklist, where applicable:

- Business rules, users/roles, authorization, success and failure criteria.
- Entry points, navigation, loading, empty, validation, error, retry, and success states; accessibility and responsive behavior.
- Domain entities, persistence/restart behavior, validation, concurrency, timestamps/timezones, retention, imports/exports.
- Backend/frontend boundaries, API contracts, external service behavior, authentication and authorization.
- Performance/reliability targets, threat-relevant checks, observability, deployment environment.
- Existing behavior to preserve, schema/data conversion, compatibility, migration safety and rollback.

Require an explicit human answer for unclear business decisions that materially affect implementation. A greenfield project needs an agreed stack and runnable baseline. A brownfield project needs an assessed baseline and change-impact boundaries; it must not be redesigned wholesale by default.

Project completion is broader than task acceptance. Use `templates/release.md` for a readiness record. Keep technical completion, environment qualification, human UAT, and release authorization separately stated. A project can be technically complete while UAT remains pending; do not call that released or fully accepted.

Use `TASK_DESIGN.md` at the planning/implementation/review boundaries. Require a final assembled journey/integration task in addition to component tasks. After two rejected submissions for a task, diagnose the recurring cause and revise the task or verification approach before another patch cycle.

WORKFLOW.md maps these lifecycle gates to the human's process. INVESTIGATIONS.md uses ordinary bounded tasks within existing stages, with investigation acceptance separate from design feasibility. GIT_WORKFLOW.md separates framework versions, plan/contract revisions, attempts and product releases. DELIVERY.md defines application packaging verification; OPERATIONS.md covers readiness, actual deployment results and the feedback loop.
