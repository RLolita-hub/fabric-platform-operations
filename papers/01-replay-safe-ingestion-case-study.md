# Replay-Safe Incremental Ingestion Under Explicit Failure: A Reproducible Local Case Study

**Manuscript type:** engineering case study / technical report draft. Not peer-reviewed or submitted. No methodological novelty is claimed. Author attribution pending the author's review. Prepared with AI assistance, 16 October 2026.

## Abstract

Incremental data pipelines must distinguish source changes from delivery attempts and preserve a recoverable checkpoint when processing fails. This report examines a small Python/SQLite reference implementation using synthetic retail orders. A committed-sequence contract, immutable event ledger, version-guarded current state, durable quarantine and transactional checkpoint publication are evaluated through fifteen automated behavior tests and a deterministic four-step demonstration. The delivered test execution passed all fifteen cases. The demonstration converged to five active orders and 16,500 cents after updates, deletion, replay and correction. These results establish behavior for the specified local cases; they do not establish production scalability, distributed exactly-once execution, or cloud equivalence. The report documents assumptions and proposes the additional experiments required for a Fabric implementation.

**Keywords:** incremental ETL; idempotency; checkpointing; quarantine; reconciliation; failure injection.

## 1. Problem and research questions

A transport retry should not count an order twice. A failed transaction should not advance progress beyond durable business state. A rejected event should remain explainable rather than silently disappearing.

This case study asks:

- RQ1: Does replaying an identical processed batch preserve current business state?
- RQ2: Does an injected failure after local merge preserve the prior committed checkpoint and data?
- RQ3: Can accepted and rejected events be accounted for separately from current-state order totals?

The contribution is a reproducible teaching artifact and explicit boundary analysis. The mechanisms are established engineering techniques, not a new algorithm.

## 2. Model and assumptions

Let E be one ordered source stream. Each event has a unique positive integer sequence s, business key k, operation and payload. The source adapter is assumed to deliver complete committed intervals without sequence gaps. That assumption is stronger than an ordinary identity column and must not be generalized to all source systems.

For each business key, current state retains the highest accepted sequence and deletion flag. A new accepted event replaces state only when its sequence is higher. A deletion leaves a tombstone. Identical repeated events are ignored; conflicting payloads under the same sequence fail the run.

Input business constraints cover required fields, allowed operations and regions, valid dates, positive identifiers, and bounded integer quantities/prices. Money is USD cents. The fact grain is one order with one product. Invalid business records are acknowledged only when their quarantine record is durably committed; corrections require new source sequence IDs.

## 3. Implementation

Python's standard library supplies JSON parsing, hashing, CSV export and SQLite access. The local write transaction contains bronze insertion, quarantine insertion, current-state updates, event reconciliation, checkpoint update and successful audit. A write transaction is begun before the checkpoint read. An exception rolls back this transaction; the application subsequently commits a failed-run audit record separately.

SQLite transaction behavior provides the local mechanism [1]. This study does not test every SQLite crash or storage durability mode. Process termination before error logging is a known telemetry limitation.

## 4. Method

The supplied test harness uses isolated temporary databases. Fifteen tests exercise full-load totals, duplicate replay, updates/deletes/quarantine, injected failure and retry, sequence gaps, conflicting IDs both across and within batches, invalid event IDs, schema drift, new-ID correction, empty input, unsorted delivery, CSV exports, malformed JSON, and bad types/dates.

A separate demonstration loads three initial events, five new changes plus one duplicate delivery, replays the change file, then loads two correction events. Expected monetary totals are directly determined by the tiny fixture rather than estimated from a model. The executed environment is Python 3.12.14 with SQLite; no cloud services or third-party packages are used.

Reproduction:

```sh
cd github/enterprise-fabric-platform
python -m unittest discover -s tests -v
python src/pipeline.py --db build/research.db load data/batch_001.jsonl
python src/pipeline.py --db build/research.db load data/batch_002.jsonl
python src/pipeline.py --db build/research.db load data/batch_002.jsonl
python src/pipeline.py --db build/research.db load data/batch_003_corrections.jsonl
```

Use a fresh database path for an independent initial-load run.

## 5. Observed results

| Demonstration step | Received | New events | Accepted | Rejected | Checkpoint |
|---|---:|---:|---:|---:|---:|
| Initial | 3 | 3 | 3 | 0 | 3 |
| Changes | 6 | 5 | 3 | 2 | 8 |
| Replay | 6 | 0 | 0 | 0 | 8 |
| Corrections | 2 | 2 | 2 | 0 | 10 |

Final active state contains five orders, with regional revenue of 9,500 cents East, 5,000 South and 2,000 West. The original two quarantine records remain as evidence after corrections.

The replay test supports RQ1 for identical fixture deliveries. The injected-failure test supports RQ2 for a Python exception after merge and before commit: checkpoint remains 3, bronze retains three events and the failed transaction's quarantine additions are absent. A subsequent successful retry reaches the expected total. RQ3 is supported by the event-accounting assertion and independent fixture expectations for active state.

The suite reports 15 passing tests. This is a count of selected checks, not a statistical reliability estimate. No throughput, latency improvement or operational cost result was measured.

## 6. Threats to validity

The small deterministic fixture may miss interactions present in larger or adversarial data. Tests and implementation were prepared in the same workflow, so independent review and mutation testing would improve confidence. No concurrent-writer stress test, machine crash, disk failure, network source, or source-retention expiry was exercised. Reading an entire file into memory limits scalability. The source's gap-free committed sequence contract is synthetic. Date dimensions are sparse and product history is not modeled as SCD2.

A current-state assertion on known fixtures is not a generalized reconciliation engine. File SHA-256 identifies bytes and does not prove business equivalence. The results do not support claims about customer deployments or distributed storage behavior.

## 7. Cloud extension and evaluation plan

The proposed Fabric architecture introduces independently committed stages. It must retain immutable source windows, use replay-safe writes and maintain a publication ledger. Delta's table transaction/concurrency model [2] does not by itself establish one atomic transaction across every table and Warehouse stage.

Future experiments should inject failures after bronze, after silver, before Warehouse publication and before reporting refresh; verify no skipped source offsets and no mixed-version serving state; test competing publishers; and compare an independently reconstructed expected state at larger input sizes. These experiments remain unperformed.

## 8. Conclusion

The reference demonstrates replay and rollback behavior under a clearly specified local contract. Its value is reproducibility and explicit limitations. Cloud equivalence and operational readiness require additional implementation and evidence.

## References and artifacts

[1] SQLite, “Transaction,” https://www.sqlite.org/lang_transaction.html, accessed 2026-10-16.

[2] Delta Lake, “Concurrency control,” https://docs.delta.io/concurrency-control/, accessed 2026-10-16.

[A1] Source and tests: https://github.com/RLolita-hub/fabric-platform-operations/tree/main/github/enterprise-fabric-platform

[A2] Executed test log and demo JSON: the evidence/ directory in A1. This manuscript uses those local results; it contains no third-party experimental dataset.
