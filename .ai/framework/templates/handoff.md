ID: HANDOFF-001
To: worker
Task: TASK-001
Contract: 1

# Current handoff

## Action for the next actor
TODO — one unambiguous instruction and stop condition.

## Read these inputs
TODO — task and contract revision, master plan module/phase and revision, assigned test plans/procedures and revisions, relevant design/requirements, latest implementation and per-plan reports/review.

Name the assigned task-matrices/TASK-NNN.json and exact relevant sections/pages. Keep this handoff <= 8,192 bytes and 120 lines under MEMORY.md; link context rather than copying history or full documents.

## Current code and verification state
TODO — submitted/tested commit, current branch/HEAD, dirty-tree identity and gaps without copying large logs. If switching branches, identify the verified starting commit and how the next actor receives the current planning records (GIT_WORKFLOW.md).

## Expected outputs and constraints
TODO

## Prompt for the human to paste
Read `.ai/START_WORKER.md` and carry out the current handoff. Report results and return control to the manager when finished or blocked.
