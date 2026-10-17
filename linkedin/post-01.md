A successful ETL run is only half the story. What happens on retry?

The local retail reference now has tests for repeated batches, corrections, cancellations and failed processing. An identical replay leaves the current sales total unchanged.

The key distinction is event identity versus business identity: an event records a change, while an order represents current business state.

This is a Python/SQL reference using synthetic data. Fabric deployment remains a separate milestone.

What failure case do you test first when reviewing an incremental pipeline?

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/01-replay-safe-etl.md

#DataEngineering #MicrosoftFabric #ETL
