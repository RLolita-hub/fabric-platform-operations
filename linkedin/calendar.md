# 60-day technical content and engagement calendar

Use Day 1 as your actual start date. Publish about three technical posts per week; the other days are for engineering, discussion and recruiter follow-up. This is a 60-day action calendar, not a recommendation to write 60 superficial posts.

All links below are **templates**, not live URLs. Replace YOUR_USERNAME only after creating the actual repository. If a gate is unmet, write a design/learning note explicitly in future tense or skip that post. Do not claim completion based on its scheduled date.

## Post briefs

### Post 01 — A successful load is not the same as a safe retry.
- Opening: A successful load is not the same as a safe retry.
- Specific technical point: Identical event deliveries do not create additional current-state orders.
- Explanation/evidence to include: Show the replay test and explain the unique event ledger and business-key upsert.
- Project link template: https://github.com/YOUR_USERNAME/enterprise-fabric-platform/blob/main/tests/test_pipeline.py
- Publication gate: Reproduce the delivered local example yourself and publish the linked file.

### Post 02 — The watermark should move last.
- Opening: The watermark should move last.
- Specific technical point: The local failure-injection test leaves checkpoint 3 intact.
- Explanation/evidence to include: Show BEGIN IMMEDIATE, rollback and the separate failed-run audit. Explain why this boundary is local.
- Project link template: https://github.com/YOUR_USERNAME/enterprise-fabric-platform/blob/main/src/pipeline.py
- Publication gate: Reproduce the delivered local example yourself and publish the linked file.

### Post 03 — Six input rows can legitimately become five new events.
- Opening: Six input rows can legitimately become five new events.
- Specific technical point: Batch 2 contains an identical transport duplicate.
- Explanation/evidence to include: Separate received rows, unique events, accepted events and rejected events before reporting load counts.
- Project link template: https://github.com/YOUR_USERNAME/enterprise-fabric-platform/blob/main/evidence/demo-results.json
- Publication gate: Reproduce the delivered local example yourself and publish the linked file.

### Post 04 — A deleted order should stay deleted after a replay.
- Opening: A deleted order should stay deleted after a replay.
- Specific technical point: The order state retains a tombstone and event version.
- Explanation/evidence to include: Explain how deleting only the target row can allow an older event to recreate it.
- Project link template: https://github.com/YOUR_USERNAME/enterprise-fabric-platform/blob/main/src/pipeline.py
- Publication gate: Reproduce the delivered local example yourself and publish the linked file.

### Post 05 — Bad records need a destination, not silence.
- Opening: Bad records need a destination, not silence.
- Specific technical point: Two synthetic invalid events are durably quarantined.
- Explanation/evidence to include: Explain the acknowledge-and-quarantine policy and why corrections use new sequence IDs.
- Project link template: https://github.com/YOUR_USERNAME/enterprise-fabric-platform/blob/main/docs/runbook.md
- Publication gate: Reproduce the delivered local example yourself and publish the linked file.

### Post 06 — An event count is not a fact-table count.
- Opening: An event count is not a fact-table count.
- Specific technical point: Updates and deletes mean accepted events do not equal active orders.
- Explanation/evidence to include: Use the supplied demo to distinguish event accounting from final-state reconciliation.
- Project link template: https://github.com/YOUR_USERNAME/enterprise-fabric-platform/blob/main/evidence/demo-results.json
- Publication gate: Reproduce the delivered local example yourself and publish the linked file.

### Post 07 — The cloud version needs a different failure boundary.
- Opening: The cloud version needs a different failure boundary.
- Specific technical point: A single SQLite transaction cannot make separate Delta and Warehouse writes atomic.
- Explanation/evidence to include: Show the proposed publication ledger and label cloud recovery as planned until tested.
- Project link template: https://github.com/YOUR_USERNAME/enterprise-fabric-platform/blob/main/docs/architecture.md
- Publication gate: State clearly that this is a design decision, not a completed cloud result.

### Post 08 — ADF and Fabric should have clear responsibilities.
- Opening: ADF and Fabric should have clear responsibilities.
- Specific technical point: The proposed architecture assigns external ingestion to ADF and downstream orchestration to Fabric.
- Explanation/evidence to include: Explain the migration/lab context and why two competing schedules are unnecessary.
- Project link template: https://github.com/YOUR_USERNAME/enterprise-fabric-platform/blob/main/docs/architecture.md
- Publication gate: State clearly that this is a design decision, not a completed cloud result.

### Post 09 — A Lakehouse SQL endpoint is not a Warehouse write target.
- Opening: A Lakehouse SQL endpoint is not a Warehouse write target.
- Specific technical point: Lakehouse Delta writes and Warehouse publication use different paths.
- Explanation/evidence to include: Show the actual deployment path if run; otherwise frame this as an architecture note and link Microsoft documentation.
- Project link template: https://github.com/YOUR_USERNAME/enterprise-fabric-platform/blob/main/docs/deployment.md
- Publication gate: State clearly that this is a design decision, not a completed cloud result.

### Post 10 — A count check can pass while the data is wrong.
- Opening: A count check can pass while the data is wrong.
- Specific technical point: Equal row counts do not imply equal business keys or amounts.
- Explanation/evidence to include: Build a same-count/different-value fixture; show key-level mismatches before claiming the check works.
- Project link template: https://github.com/YOUR_USERNAME/etl-quality-framework/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 11 — Quality rules should say what happens next.
- Opening: Quality rules should say what happens next.
- Specific technical point: Warning and blocking severity imply different publication behavior.
- Explanation/evidence to include: Demonstrate a contract with owner, severity and remediation path.
- Project link template: https://github.com/YOUR_USERNAME/etl-quality-framework/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 12 — A notification can be duplicated just like a data row.
- Opening: A notification can be duplicated just like a data row.
- Specific technical point: Retried notifications need an idempotency key.
- Explanation/evidence to include: Show a persisted outbox and duplicate-delivery test; do not claim alerts were sent if using fixtures.
- Project link template: https://github.com/YOUR_USERNAME/etl-quality-framework/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 13 — A report inventory is not yet a lineage graph.
- Opening: A report inventory is not yet a lineage graph.
- Specific technical point: Asset IDs and dependency edges answer different questions.
- Explanation/evidence to include: Use fictional metadata to compare a flat report list with upstream impact analysis.
- Project link template: https://github.com/YOUR_USERNAME/powerbi-governance-framework/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 14 — Missing metadata can look like missing ownership.
- Opening: Missing metadata can look like missing ownership.
- Specific technical point: Partial API collection must remain visibly incomplete.
- Explanation/evidence to include: Demonstrate permission and scan-completion states; never infer organization-wide coverage from a partial scan.
- Project link template: https://github.com/YOUR_USERNAME/powerbi-governance-framework/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 15 — HTTP 429 should change collection behavior.
- Opening: HTTP 429 should change collection behavior.
- Specific technical point: A collector must honor service retry guidance and bounded backoff.
- Explanation/evidence to include: Show a mocked rate-limit response test, labeling it as a fixture.
- Project link template: https://github.com/YOUR_USERNAME/powerbi-governance-framework/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 16 — Lineage needs stable identities.
- Opening: Lineage needs stable identities.
- Specific technical point: Names can change or collide while asset IDs distinguish objects.
- Explanation/evidence to include: Show duplicate names in different workspaces and resolve edges using IDs.
- Project link template: https://github.com/YOUR_USERNAME/powerbi-governance-framework/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 17 — Correct totals come before faster DAX.
- Opening: Correct totals come before faster DAX.
- Specific technical point: Relationship grain determines whether measures double-count.
- Explanation/evidence to include: Show one duplicate dimension fixture and the corrected one-to-many model.
- Project link template: https://github.com/YOUR_USERNAME/semantic-model-performance/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 18 — RLS deserves a negative test.
- Opening: RLS deserves a negative test.
- Specific technical point: An authorized view is only half of an access-control test.
- Explanation/evidence to include: Test an unassigned user and multiple-region user; distinguish Desktop and service testing.
- Project link template: https://github.com/YOUR_USERNAME/semantic-model-performance/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 19 — One fast refresh is not a benchmark.
- Opening: One fast refresh is not a benchmark.
- Specific technical point: Comparable inputs, cache state and repeated timings are needed.
- Explanation/evidence to include: Publish the actual environment and measurements only after testing; no planned percentage improvement.
- Project link template: https://github.com/YOUR_USERNAME/semantic-model-performance/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 20 — A deployment passed. Did the data?
- Opening: A deployment passed. Did the data?
- Specific technical point: Code deployment and data release validation are separate gates.
- Explanation/evidence to include: Show a failed reconciliation blocking release in a lab environment.
- Project link template: https://github.com/YOUR_USERNAME/data-platform-cicd/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 21 — Rolling back Git does not roll back the data.
- Opening: Rolling back Git does not roll back the data.
- Specific technical point: Stateful migrations require a recovery plan beyond source control.
- Explanation/evidence to include: Walk through a synthetic schema/data rollback rehearsal and limitations.
- Project link template: https://github.com/YOUR_USERNAME/data-platform-cicd/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 22 — A migration is a contract test.
- Opening: A migration is a contract test.
- Specific technical point: Matching row counts alone cannot prove metric compatibility.
- Explanation/evidence to include: Compare decimal precision and null behavior in the actual source/target lab, or label it a compatibility study.
- Project link template: https://github.com/YOUR_USERNAME/synapse-fabric-migration/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 23 — An AI answer should show what it used.
- Opening: An AI answer should show what it used.
- Specific technical point: Retrieval citations allow a reviewer to inspect the basis of a diagnosis.
- Explanation/evidence to include: Demonstrate a cited synthetic log/runbook answer and one unanswered question.
- Project link template: https://github.com/YOUR_USERNAME/dataops-support-agent/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 24 — Logs are evidence, not instructions to the agent.
- Opening: Logs are evidence, not instructions to the agent.
- Specific technical point: Retrieved text can contain malicious instructions.
- Explanation/evidence to include: Show an injection fixture and verify read-only scope and refusal to execute SQL.
- Project link template: https://github.com/YOUR_USERNAME/dataops-support-agent/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 25 — An approval is not yet a validated correction.
- Opening: An approval is not yet a validated correction.
- Specific technical point: The approved request version must match the applied payload.
- Explanation/evidence to include: Demonstrate stale approval rejection and idempotent correction delivery in the learning app.
- Project link template: https://github.com/YOUR_USERNAME/powerapps-data-operations/blob/main/README.md
- Publication gate: Implement and verify this example first; this project is currently planned.

### Post 26 — A useful portfolio explains what is still missing.
- Opening: A useful portfolio explains what is still missing.
- Specific technical point: Evidence status helps readers distinguish code, runtime validation and deployment.
- Explanation/evidence to include: Review actual releases and list unresolved engineering risks with next tests.
- Project link template: https://github.com/YOUR_USERNAME/enterprise-fabric-platform/blob/main/README.md
- Publication gate: Reproduce the delivered local example yourself and publish the linked file.

## Daily schedule

| Day | Action |
|---|---|
| 1 | Publish Post 01 if its evidence gate is satisfied; answer substantive comments. |
| 2 | Implement or debug the next example; save actual output and one trade-off. |
| 3 | Publish Post 02 if its evidence gate is satisfied; answer substantive comments. |
| 4 | Leave two useful technical comments; follow up with relevant C2C contacts. |
| 5 | Publish Post 03 if its evidence gate is satisfied; answer substantive comments. |
| 6 | Record a short walkthrough or refine the next article using actual code. |
| 7 | Review recruiter replies, repository feedback and next week’s evidence; no posting required. |
| 8 | Publish Post 04 if its evidence gate is satisfied; answer substantive comments. |
| 9 | Implement or debug the next example; save actual output and one trade-off. |
| 10 | Publish Post 05 if its evidence gate is satisfied; answer substantive comments. |
| 11 | Leave two useful technical comments; follow up with relevant C2C contacts. |
| 12 | Publish Post 06 if its evidence gate is satisfied; answer substantive comments. |
| 13 | Record a short walkthrough or refine the next article using actual code. |
| 14 | Review recruiter replies, repository feedback and next week’s evidence; no posting required. |
| 15 | Publish Post 07 if its evidence gate is satisfied; answer substantive comments. |
| 16 | Implement or debug the next example; save actual output and one trade-off. |
| 17 | Publish Post 08 if its evidence gate is satisfied; answer substantive comments. |
| 18 | Leave two useful technical comments; follow up with relevant C2C contacts. |
| 19 | Publish Post 09 if its evidence gate is satisfied; answer substantive comments. |
| 20 | Record a short walkthrough or refine the next article using actual code. |
| 21 | Review recruiter replies, repository feedback and next week’s evidence; no posting required. |
| 22 | Publish Post 10 if its evidence gate is satisfied; answer substantive comments. |
| 23 | Implement or debug the next example; save actual output and one trade-off. |
| 24 | Publish Post 11 if its evidence gate is satisfied; answer substantive comments. |
| 25 | Leave two useful technical comments; follow up with relevant C2C contacts. |
| 26 | Publish Post 12 if its evidence gate is satisfied; answer substantive comments. |
| 27 | Record a short walkthrough or refine the next article using actual code. |
| 28 | Review recruiter replies, repository feedback and next week’s evidence; no posting required. |
| 29 | Publish Post 13 if its evidence gate is satisfied; answer substantive comments. |
| 30 | Implement or debug the next example; save actual output and one trade-off. |
| 31 | Publish Post 14 if its evidence gate is satisfied; answer substantive comments. |
| 32 | Leave two useful technical comments; follow up with relevant C2C contacts. |
| 33 | Publish Post 15 if its evidence gate is satisfied; answer substantive comments. |
| 34 | Record a short walkthrough or refine the next article using actual code. |
| 35 | Review recruiter replies, repository feedback and next week’s evidence; no posting required. |
| 36 | Publish Post 16 if its evidence gate is satisfied; answer substantive comments. |
| 37 | Implement or debug the next example; save actual output and one trade-off. |
| 38 | Publish Post 17 if its evidence gate is satisfied; answer substantive comments. |
| 39 | Leave two useful technical comments; follow up with relevant C2C contacts. |
| 40 | Publish Post 18 if its evidence gate is satisfied; answer substantive comments. |
| 41 | Record a short walkthrough or refine the next article using actual code. |
| 42 | Review recruiter replies, repository feedback and next week’s evidence; no posting required. |
| 43 | Publish Post 19 if its evidence gate is satisfied; answer substantive comments. |
| 44 | Implement or debug the next example; save actual output and one trade-off. |
| 45 | Publish Post 20 if its evidence gate is satisfied; answer substantive comments. |
| 46 | Leave two useful technical comments; follow up with relevant C2C contacts. |
| 47 | Publish Post 21 if its evidence gate is satisfied; answer substantive comments. |
| 48 | Record a short walkthrough or refine the next article using actual code. |
| 49 | Review recruiter replies, repository feedback and next week’s evidence; no posting required. |
| 50 | Publish Post 22 if its evidence gate is satisfied; answer substantive comments. |
| 51 | Implement or debug the next example; save actual output and one trade-off. |
| 52 | Publish Post 23 if its evidence gate is satisfied; answer substantive comments. |
| 53 | Leave two useful technical comments; follow up with relevant C2C contacts. |
| 54 | Publish Post 24 if its evidence gate is satisfied; answer substantive comments. |
| 55 | Record a short walkthrough or refine the next article using actual code. |
| 56 | Review recruiter replies, repository feedback and next week’s evidence; no posting required. |
| 57 | Publish Post 25 if its evidence gate is satisfied; answer substantive comments. |
| 58 | Implement or debug the next example; save actual output and one trade-off. |
| 59 | Publish Post 26 if its evidence gate is satisfied; answer substantive comments. |
| 60 | Leave two useful technical comments; follow up with relevant C2C contacts. |

## Medium cadence

Days 12–18: publish the included incremental reliability article after reproducing its tests. Days 25–32: governance collection and incomplete-scan handling, only after P2 works. Days 40–47: semantic model correctness/performance with real benchmark evidence. Days 55–60: one AI-agent evaluation or operations-app lesson only if implemented. These are gates, not claims of completed work.