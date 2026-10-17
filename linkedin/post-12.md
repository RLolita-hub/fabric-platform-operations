Retries can duplicate notifications too.

A future quality-alert workflow needs an idempotency key just as the data path does. Otherwise a transient failure may produce repeated messages for the same exception.

The proposed approach is a durable notification outbox with delivery status and bounded retries. It is a design extension; no live notification service is claimed.

Reliability work should include the operational side effects, not only the target table.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/06-data-platform-release-gates.md

#DataEngineering #MicrosoftFabric #ETL
