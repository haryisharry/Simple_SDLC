# Initialize a target project

1. Inspect existing files, repository instructions, working tree, build/test commands, CI, documentation, and deployment assumptions. Do not modify the application. Existing files may be valuable even without Git. Record unknowns rather than guessing.
2. Ask the human for the business problem, intended users, desired change, exclusions, constraints, and acceptance authority when they cannot be established. Batch related questions. Do not block unrelated read-only discovery.
   Establish the smallest useful release, baseline/target outcome measures and who reviews them. Use roles/PRODUCT_OWNER.md; do not invent stakeholder feedback or repeat already resolved decisions.
3. Select `greenfield` for a new application, `brownfield` for work on an existing application. This choice changes discovery emphasis, not the quality standard.
4. Run `python .ai/tools/sdlc.py init --name "Project name" --mode greenfield` (or brownfield). The helper creates only `.ai/project`, using templates. It is not project implementation. Review its generated records before proceeding.
5. If Python is unavailable, create `project/` with `requirements`, `design`, `tasks`, `reports`, `reviews`, `testing`, `evidence`, and `handoffs/history`. Copy the brief, discovery, decisions, traceability, implementation-plan, test-plan, UAT and task-matrix templates to the paths listed below. Create config/state using their JSON templates, replacing the name, absolute root, UUID project identity, and UTC timestamp. Create `handoffs/current.md` with ID HANDOFF-000, To manager, Task none. Perform checks manually.
6. Update `brief.md` and `discovery.md`. For brownfield, capture current behavior, ownership boundaries, baseline test results or NOT_RUN, existing failing checks, compatibility constraints, data migration and rollback needs, and user changes already present. Delegate baseline execution if manager checks would modify the app or require additional authorization. For greenfield, establish constraints before selecting a stack.
7. Tailor lifecycle depth to scope. Complete required specifications and a test plan before issuing the first implementation task. Unknown material behavior remains an explicit decision, not a hidden assumption.
   If an unknown needs experimental evidence, prepare an ordinary bounded task using INVESTIGATIONS.md. Settle its method/scope before dispatch; the unknown answer is its purpose. Record the decision before preparing dependent implementation.
8. Follow `TASK_DESIGN.md` to decompose the work into task-level contracts. Create task-matrices/TASK-NNN.json from the entry template and an inspected impact inventory before marking a task READY; include a final integration/journey task for each assembled feature. task-matrix.json remains a fixed v2 descriptor.
9. Maintain `implementation-plan.md` as the module/phase/task index. Fill `testing/plan.md` and create detailed procedures from `test-procedure.md` when needed; create `testing/plans`, `testing/reports` and `contracts` on demand. Include release packaging verification under DELIVERY.md and applicable operations under OPERATIONS.md. WORKFLOW.md explains the sequence from discovery through operation.

Initial template mappings:

| Template | Project destination |
| --- | --- |
| `brief.md`, `discovery.md`, `decisions.md`, `traceability.md` | Same filename in project root |
| `implementation-plan.md` | `implementation-plan.md` |
| `test-plan.md` | `testing/plan.md` |
| `uat.md` | `testing/uat.md` |
| `config.json`, `state.json` | Same filename in project root |
| `task-matrix.json` | `task-matrix.json` (v2 storage descriptor); also create empty `task-matrices/` |

Apply MEMORY.md from the first session: keep root records/current handoff <= 8,192 bytes and 120 lines; partition all other working records before 49,152 bytes or 600 lines. The entry template is copied once per actual task, not during initialization. Legacy projects use migrate-matrix; never overwrite their matrix with the new empty descriptor.

On-demand templates (not required by initialization/check): append `investigation.md` sections to an ordinary task when needed; create `project/operations.md` from `operations.md` before release, or link an adequate existing runbook. Record justified operational exclusions for small projects. Do not initialize pretend experiment, feedback or deployment results.

For manual initialization, add `Contract: none` to the initial handoff metadata.

Never copy an existing project's records into a new project as a starting specification. Use the clean export command. Do not overwrite an existing `.ai` installation or existing repository instructions.
