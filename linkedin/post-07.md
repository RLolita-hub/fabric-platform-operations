A local transaction is not a distributed guarantee.

The tested Python/SQLite example commits its data and checkpoint together. The proposed Fabric architecture has multiple independently committed stages.

Its recovery plan needs immutable source windows, replay-safe writes and a publication ledger. A retry must converge without exposing incomplete serving data.

The design note explains those boundaries. Cloud failure injection is still required before claiming the same behavior there.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/02-checkpoints-and-publication.md

#DataEngineering #MicrosoftFabric #ETL
