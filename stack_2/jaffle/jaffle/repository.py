from src.duckpond import DuckDB, DuckPondIOManager
from dagster import resource, io_manager, Definitions, load_assets_from_package_module
import assets

@resource(config_schema={"vars": str})
def duckdb(init_context):
    return DuckDB(init_context.resource_config["vars"])


@io_manager(required_resource_keys={"duckdb"})
def duckpond_io_manager(init_context):
    return DuckPondIOManager("datalake", init_context.resources.duckdb)

duckdb_localstack = duckdb.configured(
    {
        "vars": """
        set s3_access_key_id='test';
        set s3_secret_access_key='test';
        set s3_endpoint='localhost:4566';
        set s3_use_ssl='false';
        set s3_url_style='path';
        """
    }
)

defs = Definitions(
    assets=load_assets_from_package_module(assets),
    resources={
        "io_manager": DuckPondIOManager("datalake", DuckDB(duckdb_localstack))
    }
)