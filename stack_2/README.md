# Dagster + DuckDB + S3

1) Run `localstack start` and then `awslocal s3 mb s3://datalake` to create the s3 bucket for the data lake.

The data lake will be folders containing parquet files on S3. Every table will be represented by a Parquet file and will be backed by a Dagster Software-Defined Asset.

# References

- [Build a poor man’s data lake from scratch with DuckDB](https://dagster.io/blog/duckdb-data-lake)