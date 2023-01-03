import pandas as pd
from dagster import asset

from jaffle.duckpond import SQL


@asset
def population() -> SQL:
    """Create population asset"""
    pop_df = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
    )[0]

    pop_df.columns = [
        "country",
        "continent",
        "subregion",
        "population_2018",
        "population_2019",
        "pop_change",
    ]

    pop_df["pop_change"] = [
        float(str(row).rstrip("%").replace("\u2212", "-"))
        for row in pop_df["pop_change"]
    ]
    return SQL("select * from $df", df=pop_df)


@asset
def continent_population(population: SQL) -> SQL:
    """Create continent average population from population"""
    return SQL(
        "select continent, avg(pop_change) as avg_pop_change from $population group by 1 order by 2 desc",
        population=population,
    )
