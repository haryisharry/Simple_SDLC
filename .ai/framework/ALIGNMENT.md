# Alignment with the revised working process

Reviewed 2026-09-13 against the SimpleSDLC source repository's `idea.txt`. This is an implementation map for framework 1.3.0, not evidence that agents have delivered a real product with it.

| Process requirement | Existing foundation retained | 1.3.0 completion |
| --- | --- | --- |
| Configurable two-model setup, manual transfer, one writer, Manager writes only `.ai` | Config, protocol, startup prompts | Product owner documented using existing human actor; no provider orchestration or cost tracking |
| Repository setup and brownfield baseline | Bootstrap and discovery | Guide prefers reusing brownfield history, explicitly establishes current behavior/failures/upgrade needs |
| Business discovery and smallest useful release | Brief, requirements, decisions | Product-owner role; baseline/target/outcome-review fields and early user feedback |
| Validate risky assumptions before design | Ordinary bounded task, matrix, evidence and review | INVESTIGATIONS.md and task-body sections; method readiness, disproved findings, downstream decisions and prototype disposition |
| Detail and deliver the next complete increment | Master plan, task dependencies, one active task, integrated journey closure | Explicit preference for complete user outcomes, investigation dependencies, future DRAFT work |
| Predetermined verification and Developer judgment | Test procedures/reports, preflight, evidence identity, human UAT separation | Investigation and operations execution guidance joins existing startup paths |
| Review both implementation and plan correctness | Exact-code review, correction loops, preserved revisions | Business-outcome assessment in role, task design, startup and review template |
| Explicit production gates and actual deployment verification | Release template, delivery inspection, human release authority | Operational ownership/recovery gate and separate post-deployment results |
| Operate, measure and learn | Maintenance stage and ordinary task intake | OPERATIONS.md and on-demand record; review owner/cadence, incidents, outcome targets, feedback to decisions/tasks |
| Shared memory, fresh sessions, separate versions and packaging exclusions | `.ai` records, startup, Git workflow, maintenance, delivery | Existing model and schemas retained; migration reconciles records without history reset |

Review boundaries: investigation acceptance must not imply the hypothesis was supported; accepting a task must not imply human UAT or release; release authorization must not imply deployment success; a scheduled review date in a document does not create an automation. Small projects can link existing adequate records and justify inapplicable operational checks.

Qualification still needed: a real two-application pilot covering an investigation, an implemented user outcome, correction/review, human acceptance and applicable release/feedback work. Regression tests cover helper behavior and record compatibility; they do not establish model adherence, business correctness or production readiness.
