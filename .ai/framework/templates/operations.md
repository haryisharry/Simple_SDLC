# Operations and feedback record

Status: DRAFT

Keep this root record within MEMORY.md limits. Link per-release/incident/outcome pages rather than accumulating all deployment and feedback history here; preserve current owners, open issues and the next review.

## Ownership and authority

| Responsibility | Named owner / source of assignment | Authorized scope / escalation |
| --- | --- | --- |
| Product priorities and outcome review | TODO | TODO |
| Deployment and rollback decision | TODO | TODO |
| Monitoring, incidents and maintenance | TODO | TODO |

## Environment and runbook
TODO — target environment, configuration and secret provisioning references, access prerequisites, version/artifact identity, exact deployment steps and expected results. Link existing runbooks where adequate. Never store secret values.

## Migration, backup, restore and rollback
TODO — data compatibility, backup location/access reference, restore procedure, applicable recovery targets, verification evidence, rollback triggers/authority and irreversible migration constraints. State NOT_RUN or justified exclusions honestly.

## Smoke checks and operational signals

| Check / signal | Method and expected threshold | Environment / timing or cadence | Owner | Evidence / status | Response on failure |
| --- | --- | --- | --- | --- | --- |
| TODO | TODO | TODO | TODO | NOT_RUN | TODO |

## Deployment execution records

| Release / artifact identity | Authorization reference | Environment / executor / time | Deployment and migration result | Smoke / monitoring evidence | Incident / rollback disposition |
| --- | --- | --- | --- | --- | --- |
| TODO | Pending | TODO | NOT_RUN | NOT_RUN | TODO |

Keep prior releases. Before actual authorized deployment, execution results remain NOT_RUN.

## Outcome review and feedback

Next review date / cadence and owner: TODO

| Goal / signal / feedback source and date | Baseline and target | Actual observation / evidence | Decision / owner | Linked task / investigation or deferral reason |
| --- | --- | --- | --- | --- |
| TODO | TODO | NOT_RUN | TODO | TODO |

Link existing incident/feedback systems where used. The master plan and task records remain authoritative for work status. No monitoring or follow-up is automatically scheduled by this document.
