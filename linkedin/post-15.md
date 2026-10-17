A retry policy should distinguish rate limits from denied access.

Transient collection errors may justify bounded backoff. An authorization failure usually needs an access decision, not another identical request.

For the planned governance collector, mocked rate limits, denied access and unfinished scans belong in the test suite before real tenant integration.

The important outcome is that a partial collection never quietly becomes a complete-looking dashboard.

Code / technical note: https://github.com/RLolita-hub/fabric-platform-operations/blob/main/articles/04-governance-incomplete-metadata.md

#DataEngineering #MicrosoftFabric #ETL
