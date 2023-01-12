import pandas as pd
from dagster import asset

from jaffle.duckpond import SQL


@asset
def stg_costumers() -> SQL:
    """Create population asset"""
    pop_df = pd.read_csv(
        "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
    )[0]

    return SQL("select * from $df", df=pop_df)


@asset
def continent_population(population: SQL) -> SQL:
    """Create continent average population from population"""
    return SQL(
        "select continent, avg(pop_change) as avg_pop_change from $population group by 1 order by 2 desc",
        population=population,
    )
