Quarantine is a data contract, not just an error folder.

The local reference preserves invalid events with reasons. It advances past them only because quarantine is durably committed with the checkpoint. Corrections arrive under new event IDs, leaving the original evidence intact.

That is an explicit tolerate-and-alert policy. A critical financial dataset may instead need the whole batch to stop.

Which behavior applies should be a business decision recorded in the contract.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/github/enterprise-fabric-platform/docs/architecture.md

#DataEngineering #MicrosoftFabric #ETL
