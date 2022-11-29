import pandas as pd
from string import Template
from duckdb import connect

from sqlescapy import sqlescape

from typing import Mapping

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
        # TODO: Change for a match case
        # Convert to a unique identifier
        if isinstance(value, pd.DataFrame):
            replacements[key] = f"df_{id(value)}"
        # Convert recursively to string
        elif isinstance(value, SQL):
            replacements[key] = f"({sql_to_string(value)})"
        # Use sqlescapy to conver safely
        elif isinstance(value, str):
            replacements[key] = f"'{sqlescape(value)}'"
        # Stringify other types
        elif isinstance(value, (int, float, bool)):
            replacements[key] = str(value)
        elif value is None:
            replacements[key] = "null"
        else:
            raise ValueError(f"Invalid type for {key}")

        # match value:
        #     case pd.DataFrame:
        #         replacements[key] = f"df_{id(value)}"
        #     case SQL:
        #         replacements[key] = f"({sql_to_string(value)})"
        #     case str:
        #         replacements[key] = f"'{sqlescape(value)}'"
        #     case (int, float, bool):
        #         replacements[key] = str(value)
        #     case None:
        #         replacements[key] = "null"
        #     case _:
        #         raise ValueError(f"Invalid type for {key}")


    return Template(s.sql).safe_substitute(replacements)

def collect_dataframes(s: SQL) -> Mapping[str, pd.DataFrame]:
    dataframes = {}

    for _, value in s.bindings.items():
        if isinstance(value, pd.DataFrame):
            dataframes[f"df_{id(value)}"] = value
        elif isinstance(value, SQL):
            dataframes.update(collect_dataframes(value))

    return dataframes