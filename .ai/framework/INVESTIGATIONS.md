# Resolve risky assumptions before committing to a design

Use an investigation only when a material design decision needs evidence that repository inspection or an existing authoritative source cannot supply. Examples include integration behavior, target-environment access, historical data compatibility, or a performance limit. Record known facts, assumptions and open questions in discovery; do not require a prototype for every task.

## Manager prepares a bounded task

Use the existing `tasks/TASK-NNN.md` contract, matrix, state and handoff protocol. Add the sections from `templates/investigation.md` to the task body. There is no additional task type, actor, schema or lifecycle stage: use the relevant existing stage such as discovery, design or planning while investigating, and verification during review.

Define the question, decision it informs, inspected inputs, affected touchpoints, experiment method, measurable decision threshold, allowed environments/files, evidence and stop condition. Include a time or attempt bound and the report due when it is reached. Scope prototype writes explicitly to a project location owned by the worker. The Manager continues to write only inside `.ai`.

The task's acceptance criteria must judge whether the investigation was conducted correctly and produced the required observations, not demand a favorable feasibility result. A valid result can disprove the proposed design. Express the matrix check's expected observation accordingly; use its existing result statuses without adding a new status.

Uncertainty about the experiment's answer is allowed. Uncertainty about its scope, method, required access or permitted effects must be resolved before dispatch. Dependencies can reference this task; downstream design/implementation remains DRAFT until the Manager records the resulting decision and resolves material unknowns. The master plan records the dependency and the decision it blocks.

## Worker executes and returns evidence

Perform the existing preflight and proceed when aligned. Capture exact commands, inputs, environment, code/prototype identity, raw observations, limitations and cleanup. Separate observed facts from interpretations. Report a material discrepancy with evidence and a proposed resolution; do not change criteria silently.

Use the normal numbered worker report. State the finding as supported, disproved or inconclusive, separately from the execution check status. A check may PASS when a correctly measured result disproves feasibility. Missing access or an unexecuted required experiment remains BLOCKED/NOT_RUN; an inconclusive result does not authorize downstream implementation. Return control at the stop condition without automatically expanding the prototype.

## Manager decides what follows

Inspect the evidence and accept the investigation only if its contract is satisfied. Record the design consequence in decisions.md, revise requirements/design/master plan where needed, and take business tradeoffs to the product owner. For example, accepting a completed latency measurement does not accept the measured latency for production.

Preserve investigation reports and relevant evidence even when choosing a different approach. Decide whether to discard, retain as a reference, or deliberately harden prototype code through a separate implementation contract with tests, security, integration and release gates. Prototype success is never automatic production acceptance. Follow existing authorization for cleanup; do not delete unrelated work.

## Example: establish whether an integration meets a latency target

- Question: Does the agreed synthetic workload meet the business target of p95 <= 500 ms in the intended test environment?
- Task check: Run the specified workload with the agreed sample count, record all timings and errors, compute p95, and compare it with 500 ms using the recorded method. A complete, valid measurement and comparison is the expected task result.
- Observed result: p95 is 820 ms. The investigation check can PASS, while the finding is DISPROVED and the performance requirement remains unmet.
- Next step: The Manager reviews evidence and considers an architectural change or another bounded experiment. A relaxed business target requires the product owner's decision; it cannot be changed merely to obtain PASS.

This is an illustrative procedure, not evidence that a real integration was tested. The helper checks ordinary contract structure; it cannot establish the scientific validity of an experiment or enforce its consequences.
