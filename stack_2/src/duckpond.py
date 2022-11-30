import pandas as pd
from string import Template
from duckdb import connect

from sqlescapy import sqlescape

from typing import Mapping

from dagster import IOManager

class SQL:
    def __init__(self, sql: str, **bindings: any):
        self.sql = sql
        self.bindings = bindings

class DuckDB:

    def __init__(self, options: str=""):
        self.options = options

    def query(self, select_statement: SQL) -> pd.DataFrame:
        # Create ephemeral DuckDB
        db = connect(":memory:")
        db.query("install httpfs; load httpfs;")
        db.query(self.options)

        dataframes = collect_dataframes(select_statement)

        for key, value in dataframes.items():
            db.register(key, value)

        result = db.query(sql_to_string(select_statement))

        if result is None:
            return

        return result.df()

def sql_to_string(s: SQL) -> str:
    """Convert SQL statements to SQL strings.

    Args:
        s (SQL): Object to convert to a sql string.

    Raises:
        ValueError: If there's an invalid type for a value

    Returns:
        str: SQL string.
    """
    replacements = {}

    for key, value in s.bindings.items():

        match value:
            case pd.DataFrame():
                replacements[key] = f"df_{id(value)}"
            case SQL():
                replacements[key] = f"({sql_to_string(value)})"
            case str():
                replacements[key] = f"'{sqlescape(value)}'"
            case int() | float() | bool():
                replacements[key] = str(value)
            case None:
                replacements[key] = "null"
            case _:
                raise ValueError(f"Invalid type for {key}")


    return Template(s.sql).safe_substitute(replacements)

def collect_dataframes(s: SQL) -> Mapping[str, pd.DataFrame]:
    dataframes = {}

    for _, value in s.bindings.items():
        if isinstance(value, pd.DataFrame):
            dataframes[f"df_{id(value)}"] = value
        elif isinstance(value, SQL):
            dataframes.update(collect_dataframes(value))

    return dataframes


class DuckPondIOManager(IOManager):
    def __init__(self, bucket_name: str, duckdb: DuckDB, prefix=""):
        self.bucket_name = bucket_name
        self.duckdb = duckdb
        self.prefix = prefix

    def _get_s3_url(self, context) -> str:

        if context.has_asset_key:
            asset_id = context.get_asset_identifier()

        else:
            asset_id = context.get_identifier()

        return f"s3://{self.bucket_name}/{self.prefix}{'/'.join(asset_id)}.parquet"

    def handle_output(self, context, select_statement: SQL):
        if select_statement is None:
            return

        if not isinstance(select_statement, SQL):
            raise ValueError(r"Expected asset to return a SQL, got {select_statement!r}")

        self.duckdb.query(
            SQL(
                "copy $select_statement to $url (format parquet)",
                select_statement=select_statement,
                url=self._get_s3_url(context),
            )
        )