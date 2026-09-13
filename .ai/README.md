# SimpleSDLC

A portable, file-based development workflow for a human coordinating a manager model and a worker model. Version 1.3.0.

Copy this entire pristine `.ai` folder into the root of any new or existing project. Open that project in both agent applications. Start the manager, then manually alternate agents using the handoff prompts below. Only one agent writes at a time.

## Start here

Read [the operating workflow](framework/WORKFLOW.md) for discovery through release and operation. The Developer role is called `worker` in the protocol and project records. The [human product owner](framework/roles/PRODUCT_OWNER.md) sets business priorities and acceptance authority.

Paste this into your manager session:

> Read `.ai/START_MANAGER.md` and follow it. Inspect this project first. Help me clarify its business needs and initialize SimpleSDLC if needed. Work as the manager; write only inside `.ai`. Ask me about decisions you cannot establish from the project. Prepare the next actionable handoff when ready.

When the manager prepares work, stop that session and paste this into your worker session:

> Read `.ai/START_WORKER.md` and follow the current handoff. Implement and verify the assigned task. Record evidence and blockers, then prepare the return handoff and stop.

When the worker finishes, stop that session and return to the manager:

> Read `.ai/START_MANAGER.md` and review the current worker submission. Inspect the actual implementation and evidence against the task's acceptance criteria. Accept it or issue concrete corrections, update the project records, and prepare the next handoff.

These prompts work in fresh conversations. Neither application is assumed to automatically discover `.ai` instructions. The framework does not connect to providers, launch models, enforce filesystem permissions, or transfer messages.

## Contents

| Path | Purpose |
| --- | --- |
| `START_MANAGER.md`, `START_WORKER.md` | Entry points for each session |
| `framework/` | Reusable operating rules and document templates |
| `tools/sdlc.py` | Optional Python 3.10+ helper; standard library only |
| `tests/` | Regression tests for the helper |
| `project/` | Project-specific records, created during initialization |

`project/implementation-plan.md` maps modules/phases to detailed tasks, dependencies, test plans and completion gates. `project/testing/plan.md` indexes verification; substantial plans use individual procedures and execution reports. See [Git review workflow](framework/GIT_WORKFLOW.md) for submission snapshots and optional review branches, and [delivery rules](framework/DELIVERY.md) for excluding `.ai` from shipped applications.

Use [investigations](framework/INVESTIGATIONS.md) when an uncertain design needs experimental evidence. Plan a complete next increment, then implement, verify and review both the implementation and the plan against the business goal. Prepare [operations and feedback](framework/OPERATIONS.md) before release at the depth the product needs. Investigation task sections and operations records are created on demand; the existing task states, schemas and single-writer handoffs remain unchanged.

The manager owns planning and acceptance. The worker owns implementation and execution reports. Both can read the whole repository. The manager may run approved, non-destructive checks, but changes to application code, tests, dependencies, or generated project artifacts belong to the worker. Business acceptance and release authorization belong to the human.

The manager plans down to detailed tasks using `project/task-matrix.json`: affected touchpoints, dependencies, contract revision, expected checks, worker evidence and manager review. Each touchpoint needs a check. Read `framework/TASK_DESIGN.md` for this central handoff contract and the rule for diagnosing repeated correction loops. A real brownfield example is in `framework/examples/WORKDAY_LESSONS.md`.

## Local commands

Run from the target project's root. Use `py` instead of `python` on Windows if appropriate.

```text
python .ai/tools/sdlc.py init --name "My Project" --mode greenfield
python .ai/tools/sdlc.py init --name "Existing Product" --mode brownfield
python .ai/tools/sdlc.py check
python .ai/tools/sdlc.py check --ready
python .ai/tools/sdlc.py export ../next-project/.ai
python .ai/tools/sdlc.py check-delivery path/to/product.zip
python -m unittest discover -s .ai/tests -v
```

Choose only one initialization command. Initialization never overwrites existing project records. `check` validates structure, task-matrix coverage, contract revisions and selected closure rules. `--ready` additionally checks dependencies before worker dispatch and unfinished task/handoff placeholders. Evidence references must be concrete, present and nonempty; accepted rows must have manager review and consistent code identity. These checks cannot prove evidence authenticity, software correctness, exhaustive scope or document quality.

The export destination must be a new folder named `.ai`. Export copies the reusable framework and excludes all project records. If copying a folder from a previously active project by hand, copy everything **except `project/`**. Do not delete records from the original project. A root binding check detects accidental reuse of another project's initialized records. For an intentional move of the same project, review its identity and update `project/config.json`'s `project_root` to the new absolute root.

Python is optional for the document workflow: the manager can follow `framework/BOOTSTRAP.md` to create records from templates manually. No API keys are needed. Keep `.ai` in version control with the project when appropriate; never put credentials, private production payloads, or access tokens in it.

Read `framework/PROTOCOL.md` for ownership and handoff rules, `framework/LIFECYCLE.md` for the development stages, and `framework/MAINTENANCE.md` for model changes and framework upgrades. Version changes are listed in `framework/CHANGELOG.md`. The delivery command checks directory or ZIP/TAR entry names/types; it does not validate nested archives, container images or application completeness.

`framework/VALIDATION.md` records the helper's test coverage and the remaining real-agent pilot qualification.
