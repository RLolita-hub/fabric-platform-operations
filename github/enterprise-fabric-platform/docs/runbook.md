# Demonstration, debugging and interview guide

## Five-minute demo

0:00 — business problem and synthetic dataset; show local/cloud status.
0:30 — architecture and the transaction boundary.
1:00 — run batch 1; inspect $100 total.
1:40 — inject failure in batch 2 with `python src/pipeline.py load data/batch_002.jsonl --fail-after-merge`; expected nonzero exit. Check checkpoint remains 3.
2:10 — rerun batch 2 without the flag; $125, two quarantines, one cancelled order.
2:50 — replay batch 2; zero new events, unchanged total.
3:15 — load correction batch; $165 and five active orders.
3:45 — show automated tests and explain one deliberate failure case.
4:20 — explain why cloud cross-table publication needs a different recovery design.

Record your own narration after reproducing results. Screenshot the terminal, actual SQL totals, quarantine and eventual Power BI model/report. Never use an illustrative chart as proof of an implemented report. No screenshot or video has been fabricated in this release.

## Debugging exercises

| Fault | Expected evidence | Repair |
|---|---|---|
| Missing event 4, then submit event 5 | sequence_gap; no checkpoint move | Recover missing event from immutable source |
| Reuse event 1 with another payload | conflicting_event_id | Investigate source integrity; don't overwrite ledger |
| Extra input field | schema_mismatch quarantine | Version contract deliberately; resubmit with new sequence |
| Negative quantity | invalid_amount quarantine | Correct upstream and emit a new event |
| Crash after merge | transaction rollback + FAILED run | Retry same immutable batch |
| Old batch replay after deletion | deleted order stays deleted | Confirm tombstone version beats old event |
| Power BI total differs from SQL | wrong type, relationship or stale CSV | Compare loaded rows and refresh path before changing DAX |

## Interview questions with answers

1. **What makes this incremental?** A committed event sequence checkpoint determines new events; existing event IDs are validated for conflicts. This isn't a live CDC connector.
2. **Why not MAX(order_date)?** Business dates aren't change order. Corrections may affect old dates; hard deletes may disappear entirely. Use a real change feed or explicit reconciliation policy.
3. **Does this guarantee exactly once?** Local data publication is transactional and replay-safe. Cloud steps require idempotent sinks and a publication ledger; don't claim distributed exactly once.
4. **Why keep tombstones?** They retain the latest delete version so a replay cannot resurrect old state.
5. **Why does rejection advance the checkpoint?** The rejected event is durably acknowledged in quarantine. Corrections receive new IDs. For critical finance contracts, fail-the-batch can be preferable.
6. **Do event counts equal fact counts?** No. Updates and deletes change current state; reconcile event accounting separately from key/amount reconciliation.
7. **How do you prevent concurrent writers?** BEGIN IMMEDIATE serializes this local implementation. In cloud, enforce a single publisher and a transactional lease; re-test races.
8. **Where is SCD2?** Not implemented. Current synthetic product labels use Type 1 semantics. Add effective intervals and surrogate keys when historical dimension changes are part of the requirements.
9. **What is still missing for production?** Real source adapter, scale tests, secrets/identity deployment, retention, disaster recovery, multi-table publication, RLS/service validation and operational alert delivery.
10. **How would you benchmark?** Fixed seeded input sizes, documented hardware/runtime, warm/cold runs, medians and p95, identical result checks. No speedup claim before collecting evidence.

## Resume evidence

After personally running and explaining this implementation, a truthful portfolio bullet is:
“Implemented a synthetic retail ETL reference pipeline in Python and SQL with replay-safe incremental loads, deletion tombstones, quarantine, reconciliation and 15 automated behavior tests.”

Do not put this under client employment or describe it as a deployed Azure/Fabric platform. Add a cloud-specific bullet only after completing the cloud acceptance gate and recording actual outputs.
