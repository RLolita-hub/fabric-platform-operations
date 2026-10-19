# Design limitations

The demo assumes a globally unique order ID and monotonically increasing source version per order. Multiple source systems require a composite source/order key. Tombstones prevent older updates resurrecting deletes. A higher version may intentionally recreate a record. Conflicting stale versions older than current are ignored; retain an immutable event ledger if historical conflict detection is required.

Snowflake MERGE SQL is a native starter, not executed evidence. Diagnostic SELECT gates must be wired into an orchestration step that aborts on nonempty results. Do not rely on declared uniqueness constraints or ERROR_ON_NONDETERMINISTIC_MERGE to prevent duplicate inserts. Check target uniqueness before production runs and restrict concurrent writers.

Versioned UPSERT is not source CDC capture: source logs, offsets, checkpoint persistence, schema evolution and end-to-end exactly-once guarantees are outside this demo.
