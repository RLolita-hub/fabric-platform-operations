# LinkedIn technical posts — complete drafts

Review before posting under your name. Local results describe the generated reference; design posts explicitly identify planned work. Links target the GitHub publication, not fabricated Medium pages.

## Post 01

A successful ETL run is only half the story. What happens on retry?

The local retail reference now has tests for repeated batches, corrections, cancellations and failed processing. An identical replay leaves the current sales total unchanged.

The key distinction is event identity versus business identity: an event records a change, while an order represents current business state.

This is a Python/SQL reference using synthetic data. Fabric deployment remains a separate milestone.

What failure case do you test first when reviewing an incremental pipeline?

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/01-replay-safe-etl.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 02

The checkpoint should describe durable progress.

In the local reference, raw events, quarantine, current-state changes and checkpoint commit together. An injected failure after merge leaves the previous checkpoint intact.

Moving progress forward at extraction time would acknowledge work that might never reach the serving model.

The cloud design needs a separate publication protocol because its stages do not share the local transaction. That extension is proposed, not yet validated.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/02-checkpoints-and-publication.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 03

Six input rows. Five new events. Three accepted changes.

Those numbers describe the same synthetic batch. One row repeats an identical event, while two unique events fail business validation.

A useful load audit distinguishes received rows, new events, accepted events and quarantined events. Calling all of them “rows processed” hides the behavior that matters.

The repository includes the executed results and tests. These tiny figures validate logic; they are not production-volume claims.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/github/enterprise-fabric-platform/evidence/demo-results.json

#DataEngineering #MicrosoftFabric #ETL

---

## Post 04

A cancelled order should stay cancelled after a replay.

Removing a row without retaining its latest version can leave an opportunity for an old event to recreate it.

The local reference keeps a deletion tombstone and last event ID. Older changes cannot overwrite the newer state.

Retention still matters: a production design must retain enough history for its supported replay horizon. The current fixture demonstrates the behavior without claiming a production retention policy.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/github/enterprise-fabric-platform/src/pipeline.py

#DataEngineering #MicrosoftFabric #ETL

---

## Post 05

Quarantine is a data contract, not just an error folder.

The local reference preserves invalid events with reasons. It advances past them only because quarantine is durably committed with the checkpoint. Corrections arrive under new event IDs, leaving the original evidence intact.

That is an explicit tolerate-and-alert policy. A critical financial dataset may instead need the whole batch to stop.

Which behavior applies should be a business decision recorded in the contract.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/github/enterprise-fabric-platform/docs/architecture.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 06

Accepted events do not equal active orders.

An accepted change might update an existing order or cancel it. Counting those events cannot tell you how many orders should appear in a report.

The example separates event accounting from expected business state. After corrections, the fixture contains five active orders totaling $165.

The amount is a reproducible test expectation, not a business impact metric. That distinction makes the evidence easier to evaluate.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/03-reconciliation-beyond-counts.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 07

A local transaction is not a distributed guarantee.

The tested Python/SQLite example commits its data and checkpoint together. The proposed Fabric architecture has multiple independently committed stages.

Its recovery plan needs immutable source windows, replay-safe writes and a publication ledger. A retry must converge without exposing incomplete serving data.

The design note explains those boundaries. Cloud failure injection is still required before claiming the same behavior there.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/02-checkpoints-and-publication.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 08

Give ADF and Fabric orchestration different jobs.

In the proposed portfolio architecture, ADF handles external ingestion and immutable landing. Fabric orchestrates validation, transformation and downstream publication.

The goal is clear ownership of each stage. Two schedulers independently running the same transformation would make retries and concurrency harder to reason about.

This is a design choice for the lab, not a claim that every organization needs both services.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/github/enterprise-fabric-platform/docs/architecture.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 09

A Lakehouse and a Warehouse need an explicit write path.

The project separates Spark writes to Lakehouse Delta from SQL publication in a Fabric Warehouse. The Lakehouse SQL analytics endpoint is not treated as the write target for Warehouse scripts.

The supplied deployment guide labels those assets as unexecuted starters. Keeping runtime boundaries visible is part of making a portfolio reproducible.

A diagram becomes more useful when it also explains where each operation runs.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/github/enterprise-fabric-platform/docs/deployment.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 10

Equal counts can conceal unequal data.

Three source orders and three target orders may contain different keys. Even matching keys may carry different amounts.

A reconciliation design should check unique grain, missing and unexpected keys, matched values, then business aggregates.

The article uses simple comparison examples and explains the difference between the implemented fixture assertions and a future generalized quality framework. No count-only check is presented as complete reconciliation.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/03-reconciliation-beyond-counts.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 11

Every quality rule needs a consequence.

A warning and a publication-blocking failure are different operational decisions. A useful rule contract should name its severity, owner and remediation path.

The planned framework will separate those decisions from the code that measures the condition. For now, the local project demonstrates explicit quarantine and failure behavior.

A metric without an agreed response is difficult to operate when something breaks.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/03-reconciliation-beyond-counts.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 12

Retries can duplicate notifications too.

A future quality-alert workflow needs an idempotency key just as the data path does. Otherwise a transient failure may produce repeated messages for the same exception.

The proposed approach is a durable notification outbox with delivery status and bounded retries. It is a design extension; no live notification service is claimed.

Reliability work should include the operational side effects, not only the target table.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/06-data-platform-release-gates.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 13

A report inventory is not yet lineage.

An inventory answers what exists. A dependency graph answers what depends on it. Refresh history answers what happened over time.

The governance design keeps those concerns separate and uses stable asset IDs for relationships. Matching names alone is not strong dependency evidence.

The collector is planned, with synthetic fixtures first and authorized API integration later.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/04-governance-incomplete-metadata.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 14

Missing metadata does not always mean a missing owner.

A partial scan, failed page or permission boundary can hide information. A governance dashboard should expose coverage before presenting an organization-wide conclusion.

The proposed catalog retains snapshot completion and collection issues alongside normalized assets. Incomplete collection does not automatically mark an asset deleted.

The article is a design note, not a claim that a tenant-wide scan has been executed.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/04-governance-incomplete-metadata.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 15

A retry policy should distinguish rate limits from denied access.

Transient collection errors may justify bounded backoff. An authorization failure usually needs an access decision, not another identical request.

For the planned governance collector, mocked rate limits, denied access and unfinished scans belong in the test suite before real tenant integration.

The important outcome is that a partial collection never quietly becomes a complete-looking dashboard.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/04-governance-incomplete-metadata.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 16

Names make a catalog readable. IDs make it dependable.

Two workspaces can contain reports with the same name, and an asset can be renamed. Dependency edges should therefore use stable identifiers where the source supports them.

The proposed metadata model also records how an edge was obtained. An inferred relationship should not look identical to a verified one.

That transparency is part of the governance design, which remains a planned implementation.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/04-governance-incomplete-metadata.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 17

Before optimizing DAX, explain what one row means.

The synthetic model has one current order with one product. Introducing multiple order lines would change its grain and require deliberate model changes.

Duplicate dimension keys and ambiguous relationships should be investigated before compensating with a more complicated measure.

The supplied model guide starts with relationships and SQL totals. Power BI runtime validation is the next step.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/05-semantic-model-before-dax.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 18

RLS needs a negative test.

Showing an authorized user the correct rows is only part of the security exercise. An unassigned user and a multi-region user deserve explicit cases too.

The model guide includes a first static role exercise. It also distinguishes Desktop View as testing from service testing and underlying data access.

No service-level RLS validation is claimed yet.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/05-semantic-model-before-dax.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 19

One faster run is not a convincing benchmark.

A performance comparison needs the same input, documented environment and repeated timings. Warm and cold conditions should not be mixed without explanation.

For the planned semantic-model exercise, correctness remains a gate: a faster result is not an improvement if the total changes incorrectly.

No speedup percentage is claimed before those measurements exist.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/05-semantic-model-before-dax.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 20

Code passed CI. Is the data release ready?

Local tests cannot prove that a deployment targets the right workspace, publishes the expected schema or refreshes the report successfully.

The release design separates code checks, environment validation and data acceptance. The current repository provides local tests; cloud release gates remain proposed.

A useful demo will show a bad release being stopped, not only a green badge.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/06-data-platform-release-gates.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 21

Reverting Git does not necessarily restore the data.

A release may already have written data under a new schema or business interpretation. Recovery must account for that state and its dependent semantic model.

The proposed plan retains a last validated publication and source manifest. It avoids simply rewinding a checkpoint while leaving newer target state untouched.

This is a recovery design awaiting cloud rehearsal.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/06-data-platform-release-gates.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 22

Migration sign-off should test meaning, not only movement.

Matching row counts cannot establish that decimal precision, null behavior and metric definitions survived a platform change.

The proposed Synapse-to-Fabric project will compare keys, values and aggregates over the same source window before cutover. If only a simulated legacy workload is available, it will be labeled a compatibility study.

There is no completed migration result claimed in this portfolio release.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/github/enterprise-fabric-platform/docs/architecture.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 23

An AI diagnosis should make its evidence inspectable.

The proposed DataOps assistant separates observations from hypotheses and next checks. A missing-column log supports an observation; an upstream schema change may still be only a hypothesis.

The first design is read-only, using synthetic logs and versioned runbooks. No SQL execution or accuracy benchmark is claimed.

The design paper includes an evaluation protocol for citations, abstention and access boundaries.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/papers/02-evidence-aware-dataops-design.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 24

Logs are evidence, not instructions to the assistant.

Retrieved text may contain malicious instructions. A DataOps assistant should not let those strings expand tool access or override the authorized scope.

The proposed evaluation includes hostile log content, cross-scope requests and seeded secrets. Those are planned test cases, not reported passing results.

A useful assistant must be evaluated on the boundaries it respects as well as the explanations it produces.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/07-ai-dataops-evidence.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 25

An approval should authorize the exact correction version.

If a request changes after approval, applying the new payload under the old approval is unsafe workflow behavior.

The planned Power Apps/Power Automate exercise binds approval to a request version and uses an idempotency key when emitting the correction. The original quarantined evidence stays immutable.

This is a learning-project design; an exported and validated app is still to be built.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/08-versioned-data-corrections.md

#DataEngineering #MicrosoftFabric #ETL

---

## Post 26

A technical portfolio should show its limits as clearly as its results.

This release includes a tested local reference, eight technical article drafts and two manuscripts. The empirical case study reports the actual small-fixture results; the AI paper is an unvalidated design proposal.

Cloud deployment and future projects remain labeled accordingly.

That distinction gives a reviewer something concrete to inspect and a useful starting point for deeper technical questions.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/README.md

#DataEngineering #MicrosoftFabric #ETL

---
