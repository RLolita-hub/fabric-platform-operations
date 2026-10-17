A Lakehouse and a Warehouse need an explicit write path.

The project separates Spark writes to Lakehouse Delta from SQL publication in a Fabric Warehouse. The Lakehouse SQL analytics endpoint is not treated as the write target for Warehouse scripts.

The supplied deployment guide labels those assets as unexecuted starters. Keeping runtime boundaries visible is part of making a portfolio reproducible.

A diagram becomes more useful when it also explains where each operation runs.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/github/enterprise-fabric-platform/docs/deployment.md

#DataEngineering #MicrosoftFabric #ETL
