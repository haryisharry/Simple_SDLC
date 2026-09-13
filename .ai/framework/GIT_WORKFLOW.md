# Git checkpoints and review branches

Both applications share a checkout. Stop the previous writer before a branch change; switching branches changes the files visible to both applications. Git commands do not override the Manager's `.ai` write boundary: the human or assigned worker performs staging, commits, checkout/branch operations, pushes and merges involving application files. The Manager may inspect Git state and propose exact commands.

## Submission checkpoint

1. Inspect `git status --short`, `git branch --show-current` and `git rev-parse HEAD`. Preserve pre-existing user changes and distinguish application changes from planning/evidence records.
2. Prefer a committed application/test snapshot for review. Record the full submitted commit, branch and relevant test evidence. A branch name alone is not code identity. If the tree is dirty, capture relevant diffs and untracked file hashes as required by TESTING.md; never stash/reset/discard work merely to simplify a handoff.
3. Record the tested application snapshot in the report and handoff. Later commits containing only `.ai` reports may refer to that earlier tested commit; the Manager must verify that application/test inputs did not change. Rerun affected checks if they did.

## New review branch or conversation

A review branch is optional. To use one, create it from the submitted implementation commit or a descendant containing only the subsequent coordination records, after reconciling a clean working tree. Never start from an older default branch that lacks the work. Use the repository's naming convention (for example, `codex/review-TASK-001-attempt-01`).

Record the submission commit, review branch starting commit and current HEAD. If `.ai` records differ between these commits, ensure the current handoff, reports and revisions remain available. With authorized human/worker execution, `git switch -c <review-branch> <verified-start-commit>` creates the branch; replace placeholders with inspected values. No branch creation is needed merely because the Manager starts a new chat.

The Manager compares actual application code with the submitted/tested snapshot and records the comparison basis, findings and verification method. Do not label a worker-reported test as independently rerun.

## Corrections and integration

Continue on the review branch for corrections when practical: the Manager writes the updated contract and handoff there, then the worker resumes on that same branch. If another implementation branch is required, the human/worker transfers the reviewed planning changes using the project's Git workflow and checks task/handoff revisions before editing. Do not leave the worker using stale instructions on another branch.

After acceptance, integrate through the project's normal merge/release process. Compare the resulting application snapshot and rerun affected verification after merges, conflict resolution or additional changes. No acceptance or passing evidence authorizes a push, merge or deployment beyond existing user instructions.

## Independent version identifiers

| Identifier | Changes when |
| --- | --- |
| Framework version | Reusable SimpleSDLC instructions/templates/tools change |
| Master plan revision | Approved scope or sequencing changes |
| Task contract revision | Criteria, touchpoints, exclusions or dependencies change |
| Test plan revision | Planned procedure, fixtures or expected observations change |
| Attempt number | The worker submits another execution/report, even under the same contract |
| Product release version | The product's release policy assigns a release |

Preserve prior contracts, procedures, reports and reviews. A correction cycle need not create a product release or a framework upgrade.
