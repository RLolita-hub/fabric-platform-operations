# Fabric Platform Operations — engineering and technical publications

This repository contains a tested local pipeline and accompanying technical writing. **Cloud deployment, Power BI service validation and future project implementations remain pending.** All data is synthetic.

## Run the project

```sh
cd github/enterprise-fabric-platform
python -m unittest discover -s tests -v
python src/pipeline.py load data/batch_001.jsonl
python src/pipeline.py load data/batch_002.jsonl
python src/pipeline.py load data/batch_003_corrections.jsonl
python src/pipeline.py export
```

[Project README](github/enterprise-fabric-platform/README.md) • [Test evidence](github/enterprise-fabric-platform/evidence/test-results.txt) • [Architecture](github/enterprise-fabric-platform/docs/architecture.md)

## Publications

- articles/: eight complete technical article drafts. The first covers the executed local implementation; later articles explicitly distinguish design proposals and examples from deployed work.
- papers/: two technical manuscripts: an empirical local case study and a design/evaluation proposal. Neither is peer-reviewed, submitted, or claimed as novel research.
- linkedin/: complete post drafts and the 60-day calendar.
- Personal profile/contact drafts are excluded from this public repository.

Draft author attribution requires the author's review. Technical writing was prepared with AI assistance; code examples and claims should be personally reproduced before publication under an author's name. No client data or proprietary code is included.

## New: separate projects and combined Customer 360

[Browse all four projects](projects/README.md): Snowflake Incremental Orders, Informatica IDMC Order Quality, Informatica MDM Customer Mastering, and the combined IDMC + MDM + Snowflake + Fabric + Power BI platform. Each includes independent local code, tests and native deployment guidance. Local contract tests are verified; licensed cloud execution remains pending.
