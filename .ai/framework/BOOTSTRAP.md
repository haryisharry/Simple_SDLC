# Initialize a target project

1. Inspect existing files, repository instructions, working tree, build/test commands, CI, documentation, and deployment assumptions. Do not modify the application. Existing files may be valuable even without Git. Record unknowns rather than guessing.
2. Ask the human for the business problem, intended users, desired change, exclusions, constraints, and acceptance authority when they cannot be established. Batch related questions. Do not block unrelated read-only discovery.
3. Select `greenfield` for a new application, `brownfield` for work on an existing application. This choice changes discovery emphasis, not the quality standard.
4. Run `python .ai/tools/sdlc.py init --name "Project name" --mode greenfield` (or brownfield). The helper creates only `.ai/project`, using templates. It is not project implementation. Review its generated records before proceeding.
5. If Python is unavailable, create `project/` with `requirements`, `design`, `tasks`, `reports`, `reviews`, `testing`, `evidence`, and `handoffs/history`. Copy the brief, discovery, decisions, traceability, test-plan, and UAT templates to the paths listed below. Create config/state using their JSON templates, replacing the name, absolute root, UUID project identity, and UTC timestamp. Create `handoffs/current.md` with ID HANDOFF-000, To manager, Task none. Perform checks manually.
6. Update `brief.md` and `discovery.md`. For brownfield, capture current behavior, ownership boundaries, baseline test results or NOT_RUN, existing failing checks, compatibility constraints, data migration and rollback needs, and user changes already present. Delegate baseline execution if manager checks would modify the app or require additional authorization. For greenfield, establish constraints before selecting a stack.
7. Tailor lifecycle depth to scope. Complete required specifications and a test plan before issuing the first implementation task. Unknown material behavior remains an explicit decision, not a hidden assumption.
8. Follow `TASK_DESIGN.md` to decompose the work into task-level contracts. Populate task-matrix.json from an inspected impact inventory before marking a task READY; include a final integration/journey task for each assembled feature.

Initial template mappings:

| Template | Project destination |
| --- | --- |
| `brief.md`, `discovery.md`, `decisions.md`, `traceability.md` | Same filename in project root |
| `test-plan.md` | `testing/plan.md` |
| `uat.md` | `testing/uat.md` |
| `config.json`, `state.json` | Same filename in project root |
| `task-matrix.json` | `task-matrix.json` (initially empty) |

For manual initialization, add `Contract: none` to the initial handoff metadata.

Never copy an existing project's records into a new project as a starting specification. Use the clean export command. Do not overwrite an existing `.ai` installation or existing repository instructions.
