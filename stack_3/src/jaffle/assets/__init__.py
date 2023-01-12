import pandas as pd
from dagster import asset

from jaffle.duckpond import SQL
from .transformations import rename_column

@asset
def stg_costumers() -> SQL:
    """Create costumer asset"""
    costumers_df = pd.read_csv(
        "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_customers.csv"
    )

    rename_column_dict = {
        "id": "customer_id"
    }
    costumers_df = rename_column(df=costumers_df, column_dict=rename_column_dict)

    return SQL("select * from $df", df=costumers_df)

@asset
def stg_orders() -> SQL:
    """Create orders asset"""
    orders_df = pd.read_csv(
         "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_orders.csv"
    )

    rename_column_dict = {
        "id": "order_id",
        "user_id": "customer_id"
    }

    orders_df = rename_column(df=orders_df, column_dict=rename_column_dict)

    return SQL("select * from $df", df=orders_df)

@asset
def stg_payments() -> SQL:
    """Create payments asset"""
    payments_df = pd.read_csv(
         "https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_payments.csv"
    )

    rename_column_dict = {
        "id": "payment_id",
    }

    payments_df = rename_column(df=payments_df, column_dict=rename_column_dict)

    return SQL("select * from $df", df=payments_df)