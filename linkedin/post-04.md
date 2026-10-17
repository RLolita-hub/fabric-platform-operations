A cancelled order should stay cancelled after a replay.

Removing a row without retaining its latest version can leave an opportunity for an old event to recreate it.

The local reference keeps a deletion tombstone and last event ID. Older changes cannot overwrite the newer state.

Retention still matters: a production design must retain enough history for its supported replay horizon. The current fixture demonstrates the behavior without claiming a production retention policy.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/github/enterprise-fabric-platform/src/pipeline.py

#DataEngineering #MicrosoftFabric #ETL
