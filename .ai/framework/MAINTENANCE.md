# Reuse, configuration, and upgrades

## Model replacement

Edit `project/config.json` role labels to assign a different manager or worker. Then select that model manually in the corresponding application. No provider names occur in task contracts, and the helper never invokes a model. Model abilities still need to match the assigned role. Record a material role change in decisions and give the replacement model the same startup prompt.

## Clean project reuse

Keep an untouched distribution of `.ai`, or run `python .ai/tools/sdlc.py export PATH/TO/NEXT/PROJECT/.ai`. Export excludes `project/`, Python caches, and Git internals. It refuses existing destinations and symbolic links. Review customized framework files before sharing them; anything outside `project/` is part of the reusable distribution.

For a previously initialized target, do not overwrite `.ai`. Review that project's state and either resume it or make a deliberate, backed-up migration. Version 1 does not merge installations or reset project histories.

## Framework upgrades

`framework/VERSION` identifies the reusable framework. Project config/state have their own schema version. Read release changes, back up/version current records, compare framework files, and migrate schemas deliberately. Do not replace project records with fresh templates during an upgrade. Project-specific deviations belong in `project/decisions.md`; reusable rule changes belong in an explicit framework maintenance task.

## Limitations

This is a manual protocol with optional local validation, not an autonomous orchestrator. It does not enforce agent permissions, detect running sessions, select models, synchronize applications, prove review independence, or validate implementation correctness. `check` detects structural and selected state errors; agents and the human must still inspect content and evidence. Moving the same project requires intentionally rebinding its absolute root in configuration after checking identity.

## Upgrade 1.0.0 project records to 1.1.0

Back up/version existing records first. Add task-matrix.json from the new empty template; create one inspected entry per existing task using TASK_DESIGN.md. Add matching Contract metadata to each task and the current handoff (none when no task is active). Existing acceptance must be revalidated against its task rows; do not synthesize PASS results to migrate it. Preserve actual evidence/reviews and mark unsupported closure for manager review. Set config framework_version to 1.1.0 after reconciling these records. Config/state schema_version remains 1. Run check and check --ready. There is no automatic migration or history reset.
