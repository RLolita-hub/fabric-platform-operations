Give ADF and Fabric orchestration different jobs.

In the proposed portfolio architecture, ADF handles external ingestion and immutable landing. Fabric orchestrates validation, transformation and downstream publication.

The goal is clear ownership of each stage. Two schedulers independently running the same transformation would make retries and concurrency harder to reason about.

This is a design choice for the lab, not a claim that every organization needs both services.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/github/enterprise-fabric-platform/docs/architecture.md

#DataEngineering #MicrosoftFabric #ETL
