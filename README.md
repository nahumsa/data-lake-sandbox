<h1 align="center">Data Lake Sandbox</h1>
<p align="center">
<a href="https://github.com/nahumsa/data-lake-sandbox/actions"><img alt="Actions Status" src="https://github.com/nahumsa/data-lake-sandbox/workflows/stack-2/badge.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort/"><img alt="Imports: isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>
<a href="https://github.com/PyCQA/pylint"><img alt="pylint" src="https://img.shields.io/badge/linting-pylint-yellowgreen"></a>

</p>

The main goal of this project is to create a sandbox in order to understand more about how to create and manage data lakes.
I will focus on some tutorials to build a data lake from scratch which will be in the [references](https://github.com/nahumsa/data-lake-sandbox#References) section.


# Stacks

## Stack 1 (Incomplete)
<a href="https://dagster.io/">dagster</a> + <a href="https://min.io/">MinIO</a> + <a href="https://www.docker.com/">Docker</a> + <a href="https://trino.io/">trino</a>

## Stack 2
[dagster]("https://dagster.io/") + [duckdb](https://duckdb.org/) + [S3](https://aws.amazon.com/en/s3/) + [terraform](https://www.terraform.io/) + [localstack](https://localstack.cloud/)

Simple example following the article [Build a poor man’s data lake from scratch with DuckDB](https://dagster.io/blog/duckdb-data-lake). It is a good entry point for learning more about dagster. I added a docker-compose file for running localstack which adds the option to create a "persistent" s3 bucket if it is needed. I also added terraform in order to create all resources that are needed for the AWS implementation.

# References

- [How to build a data lake from scratch — Part 1: The setup](https://towardsdatascience.com/how-to-build-a-data-lake-from-scratch-part-1-the-setup-34ea1665a06e)
- [How to build a data lake from scratch — Part 2: Connecting the components](https://medium.com/towards-data-science/how-to-build-a-data-lake-from-scratch-part-2-connecting-the-components-1bc659cb3f4f)
- [How to Build a Modern Data Lake with MinIO](https://medium.com/codex/how-to-build-a-modern-data-lake-with-minio-db0455eec053)
- [Build a poor man’s data lake from scratch with DuckDB](https://dagster.io/blog/duckdb-data-lake)