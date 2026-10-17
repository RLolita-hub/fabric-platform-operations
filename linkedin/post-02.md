The checkpoint should describe durable progress.

In the local reference, raw events, quarantine, current-state changes and checkpoint commit together. An injected failure after merge leaves the previous checkpoint intact.

Moving progress forward at extraction time would acknowledge work that might never reach the serving model.

The cloud design needs a separate publication protocol because its stages do not share the local transaction. That extension is proposed, not yet validated.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/02-checkpoints-and-publication.md

#DataEngineering #MicrosoftFabric #ETL
