# Design limitations

The local transformation runs a complete in-memory batch and has no scheduler, persistent watermark or connector. Schema errors fail fast. Conflicting duplicate accepted keys raise before the CLI writes output. Rejections count invalid source rows; exact duplicates are collapsed, not labeled rejects. There is no FX conversion. Decimal validation preserves cents without rounding fractional cents.

In native IDMC configure equivalent rules and failure branches, validate runtime behavior and export sanitized mapping assets. The mapping specification is not a JSON/XML import package. Performance, pushdown and runtime sizing remain unmeasured.
