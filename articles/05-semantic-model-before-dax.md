# Before optimizing DAX, verify what one row means

*Technical tutorial draft. DAX examples are authored; Power BI runtime validation is pending.*

A slow measure attracts attention. An incorrect grain can be more damaging because the report may look plausible while aggregating the wrong business concept.

The retail reference makes its grain explicit: one current order with one product. It is intentionally not an order-line model. If multi-line orders are introduced later, the fact key and measures must change deliberately.

## Start with relationships and types

The exported model has fact orders and date, product and region dimensions. Each dimension key should be unique, and filters should propagate from a dimension to its fact through a clear relationship. Check duplicate keys before trying to repair a doubled total with increasingly complicated DAX.

Money arrives as integer cents. Keep that representation in the fact table and convert through a measure:

```dax
Revenue = DIVIDE(SUM(fact_orders[revenue_cents]), 100)
Order Count = DISTINCTCOUNT(fact_orders[order_id])
Average Order Value = DIVIDE([Revenue], [Order Count])
```

These measures are supplied as a starter, not as an executed Power BI benchmark. Their expected fixture total is $165 across five active orders. The SQL evidence gives a comparison point when the model is built.

## Totals need a definition

Average order value should divide total revenue by distinct orders in the current filter context. Averaging regional averages instead can give a different result when regions contain different order counts. Decide what the metric means before selecting an expression.

The example date dimension contains only observed dates. It is sufficient for this tiny fixture, but it is not a complete calendar suitable for a time-intelligence demonstration. Expanding it is a prerequisite for a meaningful YTD exercise.

## Test security separately

A proposed first exercise applies an East-only role to the region dimension. The expected local fixture result is $95 across three orders. View-as testing in Desktop is a useful check; it does not replace service testing with the intended viewer identities and underlying data permissions.

## Then measure performance

Hold data, model version and query constant. Record cold and warm conditions separately, repeat runs and compare medians alongside result equality. Change one factor at a time: a relationship, unused columns, a measure, or storage strategy. Report the actual environment and input size with any improvement.

No performance percentage is claimed here. The first deliverable is a correct, explainable model whose SQL and DAX totals agree. Optimization begins from that baseline.

Project: https://github.com/RLolita-hub/fabric-platform-operations/tree/main/github/enterprise-fabric-platform/powerbi

Reference: Microsoft Power BI star-schema guidance, https://learn.microsoft.com/en-us/power-bi/guidance/star-schema. The specific retail grain and fixture expectations are project design choices and local results.
