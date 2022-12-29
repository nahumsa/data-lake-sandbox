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
        check_value_instance = lambda x: isinstance(value, x)

        if check_value_instance(pd.DataFrame):
            replacements[key] = f"df_{id(value)}"
        elif check_value_instance(SQL):
            replacements[key] = f"({sql_to_string(value)})"
        elif check_value_instance(str):
            replacements[key] = f"'{sqlescape(value)}'"
        elif check_value_instance(int) or check_value_instance(float) or check_value_instance(bool):
            replacements[key] = str(value)
        elif value is None:
            replacements[key] = "null"
        else:
            raise ValueError(f"Invalid type for {key}")


    return Template(s.sql).safe_substitute(replacements)

def collect_dataframes(s: SQL) -> Mapping[str, pd.DataFrame]:
    dataframes = {}

    for _, value in s.bindings.items():
        check_value_instance = lambda x: isinstance(value, x)
        if check_value_instance(pd.DataFrame):
            dataframes[f"df_{id(value)}"] = value
        elif check_value_instance(SQL):
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
        """Stores software defined assets to the data lake.

        Args:
            context (_type_): _description_
            select_statement (SQL): Statment to store to the data lake.

        Raises:
            ValueError: When receiving a select statement that is not SQL.

        Returns:
            None: None when the select statement is None
        """
        check_select_statement_instance = lambda x: isinstance(select_statement, x)

        if select_statement is None:
            return

        if not check_select_statement_instance(SQL):
            raise ValueError(r"Expected asset to return a SQL, got {select_statement!r}")

        self.duckdb.query(
                            SQL(
                                "copy $select_statement to $url (format parquet)",
                                select_statement=select_statement,
                                url=self._get_s3_url(context),
                            )
                        )


    def load_input(self, context) -> SQL:
        return SQL(
            "select * from read_parquet($url)", url=self._get_s3_url(context)
        )