# Operating guide: from discovery to operation

The human product owner coordinates two roles in the same project folder: Manager plans and reviews; Developer (called `worker` in records) implements and runs tests. Model and application names are configurable labels. No API connection, cost tracking, or automatic dispatch is required. Stop one writing session before starting the other. See roles/PRODUCT_OWNER.md for business decisions and acceptance responsibilities.

## 1. Create and open the repository

For a new project, create the GitHub repository in your browser, then clone it to your Windows laptop using your normal Git tool. For brownfield work, reuse the existing repository where practical or import the source while preserving its history where available; inspect credentials and ignored files before committing. Establish current behavior, existing failures, user changes, compatibility and upgrade needs before planning changes. Open the same local folder in both agent applications.

Copy the pristine `.ai` distribution into the project, or export it from an existing installation using `python .ai/tools/sdlc.py export PATH/TO/PROJECT/.ai`. Export excludes project records and refuses existing destinations. If `.ai/project` already exists, resume it or follow MAINTENANCE.md; do not initialize over it.

## 2. Discover and define requirements with the Manager

Paste the manager startup prompt from `.ai/README.md`. The Manager inspects the repository and initializes records through BOOTSTRAP.md. Establish the business goal, stakeholders and roles, scope, constraints, risks, rough estimates and assumptions. For brownfield work, capture current behavior, compatibility requirements and baseline gaps.

Write stories, functional/nonfunctional requirements, observable acceptance criteria and integration needs in `.ai/project`. Record unresolved business decisions explicitly. Save the agreed planning checkpoint to Git and push through the human's normal workflow. The Manager writes only inside `.ai` and can read the whole repository.

Agree with the product owner on the smallest useful release and measurable outcomes, including baseline, target and review timing. Seek early user workflow/prototype feedback where useful and record actual sources. Reuse existing decisions; routine technical choices do not require another approval round.

## 3. Validate assumptions, design and prepare the implementation plan

Identify material assumptions needing experimental evidence before committing to a design. Follow INVESTIGATIONS.md to assign a bounded investigation through the ordinary task/matrix/handoff system. The method must be actionable even though its answer is unknown. Accepting valid investigation evidence does not imply a feasible design or production-ready prototype.

With the Manager, settle architecture, data and API contracts, UX/UI states, security, technology choices, deployment and migration needs. Use `project/implementation-plan.md` to map modules/phases to requirements, detailed tasks, dependencies and completion gates.

The master plan is an index and sequencing record. Detailed procedures belong in `tasks/TASK-NNN.md`; checkable coverage belongs in `task-matrix.json`. Plan the overall delivery before dispatch, and fully specify the current task before marking it READY. Future tasks may remain DRAFT with explicit open decisions. Include final assembled feature and release verification work.

Prefer a complete user outcome across relevant UI, backend and persistence boundaries for each increment; sequence necessary foundational tasks explicitly. Do not require every future module to be fully specified before the first increment. The central loop is: plan the next complete increment -> implement -> verify -> review against the business goal -> adjust -> continue.

## 4. Plan verification before implementation

Use `project/testing/plan.md` as the test index. For substantial work, create individual `testing/plans/TESTPLAN-NNN.md` files from `templates/test-procedure.md`. Define fixtures, setup, ordered actions, expected observations, evidence and cleanup before execution. Map each scenario to requirements and task checks.

Cover applicable integration, functional/feature, regression, performance, security and full role-based journeys, plus unit/build checks. Explain exclusions. Prepare human UAT scripts and acceptance authority. See TESTING.md for test-plan revisions and evidence rules.

## 5. Dispatch to the Developer

The Manager prepares the current task's handoff and updates state using PROTOCOL.md. Stop the Manager session and paste the worker startup prompt. The Developer reads the agreed plan, performs its preflight, implements the assigned task and executes its planned checks. It produces an implementation report and a linked report for each assigned test plan.

The Developer applies technical judgment and challenges material contradictions with evidence and a proposed resolution. When aligned, proceed without an extra approval round. Test during implementation and perform the deliberate verification pass before returning the task.

Return to the Manager at the task's review boundary. Continue through the plan with one active task at a time; the whole project plan does not authorize the Developer to skip intermediate acceptance gates. Run the broader assembled-feature and release checks at their planned gates. Blocked checks retain their actual status.

## 6. Review, revise and repeat

Stop the Developer and resume the Manager, in the same or a fresh conversation. Use GIT_WORKFLOW.md when creating a review branch: it must contain the submitted implementation. Inspect the exact code and evidence, record root causes, accept the task or issue concrete corrections. Update the master plan, affected contracts and test procedures when findings change them; preserve prior attempts and invalidate affected evidence.

Review the plan itself against the original business outcome: could the design and tests agree while missing a required real-user behavior? Inspect relevant omitted journeys, assumptions and evidence limitations. A fresh conversation does not itself establish independent verification. Distinguish rerun checks, inspected artifacts and worker-reported results; take changed business scope to the product owner.

Repeat until technical verification and target-environment qualification are complete. Human UAT and release authorization remain explicit gates. Follow DELIVERY.md to exclude `.ai` from application delivery artifacts. A correction attempt increments an attempt number; changed specifications increment plan/contract revisions; product versions follow the product's release policy. None of these automatically changes the SimpleSDLC framework version.

## 7. Qualify and release

Use the release template to record explicit requirement/journey, technical verification, target environment, human UAT, delivery, recovery and authorization gates. Resolve defects or record their appropriate accepted dispositions. Before the release decision, prepare the applicable configuration, secrets provisioning references, migration, backup/restore, deployment and rollback procedures with verified evidence under OPERATIONS.md. Missing required qualification remains NOT_RUN/BLOCKED.

After actual authorized deployment, record the deployed artifact, environment and execution results, including smoke checks. Keep readiness, release authorization and deployment success separate. Do not infer production execution from a completed plan.

## 8. Operate and learn

Assign monitoring, incidents, troubleshooting, maintenance and rollback responsibilities. Follow OPERATIONS.md to record outcome review timing, user feedback and operational observations. Compare actual outcomes with the brief's targets, then route actionable findings into decisions and bounded tasks in the existing master plan. The product owner decides changed priorities; no background monitoring is automatically created by this framework.

## Resume in a fresh conversation

Use the appropriate README startup prompt. The current state, handoff, master plan, task and linked reports are the shared memory. Verify project identity, writer ownership, branch and code snapshot first. Reconcile interrupted updates from evidence before continuing; conversation history alone is not an authoritative contract.
