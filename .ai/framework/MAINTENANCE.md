# Reuse, configuration, and upgrades

## Model replacement

Edit `project/config.json` role labels to assign a different manager or worker. Then select that model manually in the corresponding application. No provider names occur in task contracts, and the helper never invokes a model. Model abilities still need to match the assigned role. Record a material role change in decisions and give the replacement model the same startup prompt.

## Clean project reuse

Keep an untouched distribution of `.ai`, or run `python .ai/tools/sdlc.py export PATH/TO/NEXT/PROJECT/.ai`. Export excludes `project/`, Python caches, and Git internals. It refuses existing destinations and symbolic links. Review customized framework files before sharing them; anything outside `project/` is part of the reusable distribution.

For a previously initialized target, do not overwrite `.ai`. Review that project's state and either resume it or make a deliberate, backed-up migration. Version 1 does not merge installations or reset project histories.

## Framework upgrades

`framework/VERSION` identifies the reusable framework. Project config/state have their own schema version. Read release changes, back up/version current records, compare framework files, and migrate schemas deliberately. Do not replace project records with fresh templates during an upgrade. Project-specific deviations belong in `project/decisions.md`; reusable rule changes belong in an explicit framework maintenance task.

Read CHANGELOG.md before upgrading. Plan/contract revisions, execution attempts and product releases are separate identifiers described in GIT_WORKFLOW.md.

## Limitations

This is a manual protocol with optional local validation, not an autonomous orchestrator. It does not enforce agent permissions, detect running sessions, select models, synchronize applications, prove review independence, or validate implementation correctness. `check` detects structural and selected state errors; agents and the human must still inspect content and evidence. Moving the same project requires intentionally rebinding its absolute root in configuration after checking identity.

## Upgrade 1.0.0 project records to 1.1.0

Back up/version existing records first. Add task-matrix.json from the new empty template; create one inspected entry per existing task using TASK_DESIGN.md. Add matching Contract metadata to each task and the current handoff (none when no task is active). Existing acceptance must be revalidated against its task rows; do not synthesize PASS results to migrate it. Preserve actual evidence/reviews and mark unsupported closure for manager review. Set config framework_version to 1.1.0 after reconciling these records. Config/state schema_version remains 1. Run check and check --ready. There is no automatic migration or history reset.

## Upgrade 1.1.0 project records to 1.2.0

1. Stop the other writer and version/back up the installation and records. Compare and update reusable `framework/`, entry points, README, tools and tests, preserving reviewed project customizations. Never overwrite `project/` or rerun init.
2. Add `project/implementation-plan.md` from its new template if absent. Populate it from existing scope, tasks, dependencies and release gates; link existing plans instead of duplicating them. Preserve any existing document with that name and reconcile its structure manually.
3. Extend the existing `project/testing/plan.md` with procedure IDs/revisions, scenarios and report links. Existing adequate procedures may be linked in place. Create individual procedures/reports only as needed; retain original evidence and identify legacy reports with their original code/contract context. Do not fabricate historical per-plan execution reports or reset accepted tasks merely for formatting changes.
4. Record adopted Git review and delivery rules in decisions. Add missing packaging work as a task for the next relevant release. If review reveals genuinely missing required coverage, revise the affected contracts and invalidate affected results under TASK_DESIGN.md.
5. Keep config/state/task-matrix `schema_version: 1`. Set only config `framework_version` to `1.2.0` after reconciliation. Run `check` and `check --ready`; investigate failures without resetting history. Check the new documents' content and links manually: helper validation only requires the master plan's presence, not its quality, procedure coverage or revision history.

For a 1.0.0 installation, perform the 1.1.0 record reconciliation above first, then these steps and final checks against 1.2.0. The pristine distribution stays uninitialized. `export` remains a clean framework copy for a new project, not a migration or an application packaging command.

## Upgrade 1.2.0 project records to 1.3.0

1. Stop the other writer and back up/version the installation. Compare and update reusable framework files, entry points, README, tools and tests, preserving project customizations. Do not rerun init or replace project records with fresh templates.
2. Reconcile brief/discovery/master-plan content with the product owner's smallest useful release, measurable outcome targets, known assumptions and next complete increment. Reuse existing answers, evidence and plans. If a material assumption needs investigation, create an ordinary bounded task under INVESTIGATIONS.md; do not fabricate a historical experiment or reset acceptance solely for a format change.
3. Use the expanded review template for future reviews, explicitly checking the plan against the original business outcome. Preserve historical reviews. If an actual overlooked requirement invalidates prior acceptance, record a new review and revise affected contracts/evidence through TASK_DESIGN.md.
4. Before the next relevant release, create operations.md from the on-demand template or link an adequate existing runbook. Record actual owners, applicable recovery/monitoring work and outcome-review timing. Add genuinely missing work through existing tasks; do not invent past deployment results or human signoff. Neither new template is a mandatory initialized document.
5. Change config `framework_version` to `1.3.0` after reconciliation. Config/state/task-matrix schemas remain 1, with the same task states, stages and actors. Run `check` and `check --ready`; manually review the content and links because the helper does not enforce business outcomes, investigation validity or operations readiness.

For older installations, apply the earlier record reconciliations in order, then set the final framework version to the installed version and run its checks. Intermediate version-mismatch errors during a multi-version migration are not grounds to reset records. No automatic migration, provider connection or background monitoring is introduced.
