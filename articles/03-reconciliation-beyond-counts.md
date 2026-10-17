# Equal row counts do not mean equal data

*Technical article draft. Uses the tested local reference and clearly identified SQL examples.*

Suppose a source contains orders 101, 102 and 103. The target contains 101, 102 and 104. Both have three rows. A count-only reconciliation passes even though one order is missing and another is unexpected.

Amounts create another failure mode: the same keys may exist with different prices. A useful reconciliation therefore separates cardinality, key coverage, business values and state semantics.

## Events and current state answer different questions

The supplied change batch receives six rows but has five unique new events. Three are accepted and two are quarantined. Its accepted changes include an update and a cancellation, so three accepted events do not imply three additional orders.

The implemented event invariant is:

`new bronze events = accepted events + quarantined events`

That proves every new event has a disposition. It does not prove the resulting business state is correct. Separate fixture assertions verify the active-order total and amount.

## A practical comparison sequence

Start with unique grain. A duplicated business key can inflate aggregates and make later comparisons confusing. Compare source-only and target-only keys next, then matched values. Finally compare aggregates at meaningful business dimensions such as region and currency.

```sql
-- Example for independent expected_state and actual_state tables.
SELECT e.order_id
FROM expected_state e
LEFT JOIN actual_state a ON a.order_id = e.order_id
WHERE a.order_id IS NULL;

SELECT e.order_id, e.revenue_cents, a.revenue_cents
FROM expected_state e
JOIN actual_state a ON a.order_id = e.order_id
WHERE e.revenue_cents <> a.revenue_cents;
```

These are illustrative comparison queries; the provided repository does not yet contain a generalized expected-state reconstruction engine. For nullable fields, define whether two nulls are equal and explicitly detect one-sided nulls rather than relying on ordinary inequality.

## Money and tolerances

The local fixture uses integer cents and a single currency. Exact equality is appropriate for this contract. Floating-point or converted monetary values need documented precision and rounding rules. A tolerance should come from the business calculation, not be increased until a failing test passes.

A checksum can accelerate comparisons, but its input must be canonical: stable key ordering, type representation, null encoding and delimiters. An input-file SHA-256 verifies the input bytes; it is not source-to-target business reconciliation.

## Make the result actionable

A failed check should record its rule ID, source interval, severity, expected and actual values, mismatch sample and owner. For large datasets, retain bounded examples rather than dumping sensitive rows into logs. Publication policy must say which failures block release and which generate visible exceptions.

The first useful test for a quality framework is simple: deliberately create equal counts with unequal values. If it still reports success, it is measuring activity rather than correctness.

Project and executed evidence: https://github.com/RLolita-hub/fabric-platform-operations/tree/main/github/enterprise-fabric-platform
