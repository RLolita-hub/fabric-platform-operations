An approval should authorize the exact correction version.

If a request changes after approval, applying the new payload under the old approval is unsafe workflow behavior.

The planned Power Apps/Power Automate exercise binds approval to a request version and uses an idempotency key when emitting the correction. The original quarantined evidence stays immutable.

This is a learning-project design; an exported and validated app is still to be built.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/08-versioned-data-corrections.md

#DataEngineering #MicrosoftFabric #ETL
