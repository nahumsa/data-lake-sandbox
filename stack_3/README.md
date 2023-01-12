# Dagster + DuckDB + S3 + Terraform

Simple example following the article [Build a poor man’s data lake from scratch with DuckDB](https://dagster.io/blog/duckdb-data-lake). It is a good entry point for learning more about dagster. I added a docker-compose file for running localstack which adds the option to create a "persistent" s3 bucket if it is needed. I also added terraform in order to create all resources that are needed for the AWS implementation.

## Requirements

- Python 3.7
- [`pipenv`](https://pipenv.pypa.io/en/latest/) installed
- `Docker`
- `docker-compose`
- `terraform`

## Creating in a hurry using Makefile

I chose to use a Makefile to abstract every command and make it easier to create everything with simple syntax.Thus, in order to setup the data lake and dagster you need to use the following commands:

```bash
make setup
```

```bash
make start_localstack
```

```bash
make apply_terraform
```

```bash
make start_dagster
```

## Creating the data lake in depth
To install all packages that are used for development, you need to have python 3.7 and [`pipenv`](https://pipenv.pypa.io/en/latest/) installed, then you can install everything using:

```bash
pipenv install --dev
```

In order to create the s3 bucket that is used for the data lake, you need to start local stack using `docker-compose up -d` (this will run the docker-compose file detached, thus you need to use `docker-compose down` after). After starting localstack you must create the bucket using terraform, so you change to the `terraform` folder and run the following commands:

```bash
tflocal init
tflocal plan
tflocal apply -auto-approve
```

After creating the bucket, you can run dagster using `dagit` on the `src` folder and materialize all Software-Defined Assets.

Since this is a "begginer" tutorial there aren't data lake management policies and tiers for the data assets, so the data lake will be folders containing parquet files on S3. Every table will be represented by a Parquet file and will be backed by a Dagster Software-Defined Asset.

# TODO

- [ ] Add EC2 for dagster

# References

- [Build a poor man’s data lake from scratch with DuckDB](https://dagster.io/blog/duckdb-data-lake)
- [How Pipenv and setup.py work together](https://gist.github.com/dpboard/887b74f242605c3a409b90f0cf706531)