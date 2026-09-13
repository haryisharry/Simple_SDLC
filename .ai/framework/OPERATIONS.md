# Release operation and feedback

Before the release decision, the Manager prepares `project/operations.md` from `templates/operations.md`, or links an existing equivalent runbook from the release record. Scale detail to product risk; record justified exclusions for inapplicable items. This record is created when relevant, not required to initialize an empty project.

## Responsibilities and preparation

The product owner identifies who owns production operation, user feedback, incident response and release/rollback decisions. One person may fill several roles. Record actual assignments and unresolved responsibilities; do not invent an on-call team or human agreement. The Manager organizes the plan and records decisions. The worker implements and verifies application configuration, deployment scripts, monitoring and other operational changes through bounded tasks.

Define applicable environments, configuration and secret provisioning procedures (references only, never secret values), access prerequisites, version/artifact identity, deployment steps, migrations, backup and restore, smoke checks, monitoring and rollback triggers. Include recovery targets where relevant and evidence that recovery procedures were exercised. A backup's existence is not proof of restore capability. A migration may prevent a simple binary rollback; state the recovery approach explicitly.

Link required operational checks to release tasks, test plans and evidence. Missing required recovery/environment verification remains NOT_RUN/BLOCKED and prevents a full readiness claim. Exclusions and accepted limitations need their appropriate decision owner and rationale.

## Release and verification after deployment

Keep release authorization distinct from deployment execution and the subsequent smoke-check result. Record the authorized scope, actual deployed artifact/environment/time, executor, migration result, smoke checks and monitoring observations. Before deployment these execution fields remain NOT_RUN; authorization alone does not populate them.

After an authorized deployment, the worker or authorized operator records actual results. Failures follow the agreed response and rollback authority; passing preparation checks does not authorize additional production effects. There is no scheduler or monitoring service in SimpleSDLC: the assigned human/operator and project tooling perform checks at the recorded cadence.

## Learn and return to planning

Set a review date/cadence and owner for business outcome measures and operational signals. Compare the observed outcomes with the brief's success criteria and baseline. Record user feedback with source/date, incidents, unresolved issues and maintenance needs in the operations record or linked existing system.

The Manager triages each actionable finding into a decision, a bounded task, a further investigation or an explicitly deferred item with an owner/reason. The product owner decides changed priorities or business scope. Update the master plan and affected contracts/tests through the normal revision process. Use the existing maintenance lifecycle stage and current handoff; do not create a second competing task queue inside this document.

Do not reopen all accepted work because feedback arrived. Review the affected behavior and boundaries, preserving unrelated acceptance and historical release evidence. Mark a fixed incident resolved only when its required verification and disposition are recorded.
