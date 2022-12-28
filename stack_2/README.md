# Dagster + DuckDB + S3

1) Run `localstack start` and then `awslocal s3 mb s3://datalake` to create the s3 bucket for the data lake.

The data lake will be folders containing parquet files on S3. Every table will be represented by a Parquet file and will be backed by a Dagster Software-Defined Asset.

# Using terraform

First, install `terraform-local`, then you can move to the `terraform` folder, and then use the commands:

```bash
tflocal init
tflocal plan
tflocal apply -auto-approve
```

# References

- [Build a poor man’s data lake from scratch with DuckDB](https://dagster.io/blog/duckdb-data-lake)
- [How Pipenv and setup.py work together](https://gist.github.com/dpboard/887b74f242605c3a409b90f0cf706531)