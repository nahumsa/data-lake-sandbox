# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from jaffle.assets import continent_population, population
from jaffle.duckpond import DuckDB


def test_assets():
    pop_asset = population()
    continent_population_asset = continent_population(pop_asset)

    assert (
        continent_population_asset.sql
        == "select continent, avg(pop_change) as avg_pop_change from $population group by 1 order by 2 desc"
    )
    assert "population" in continent_population_asset.bindings

    continent_population_df = DuckDB().query(continent_population_asset)
    top = continent_population_df.loc[0]

    assert top["continent"] == "Africa"
    assert round(top["avg_pop_change"]) == 2
