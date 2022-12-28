from typing import Union
import pytest
import pandas as pd

from jaffle.duckpond import sql_to_string, SQL


class TestSQLToString:
    def test_dataframe(self):
        df = pd.DataFrame()
        query = SQL("select * from $df", df=df)
        assert sql_to_string(query) == f"select * from df_{id(df)}"

    def test_sql(self):
        df = pd.DataFrame()
        query = SQL("select * from $test",
                     test=SQL("select * from $df", df=df))

        assert sql_to_string(query) == f"select * from (select * from df_{id(df)})"

    @pytest.mark.parametrize("number", [1, 2, 3, 4, 5, 1.5, 2.5, 3.6])
    def test_int_float(self, number: Union[int, float]):
        query = SQL("select $number from df", number=number)
        assert sql_to_string(query) == f"select {number} from df"

    @pytest.mark.parametrize("boolean", [True, False])
    def test_bool(self, boolean: bool):
        query = SQL("select $boolean from df", boolean=boolean)
        assert sql_to_string(query) == f"select {boolean} from df"

    def test_none(self):
        query = SQL("select $none from df", none=None)
        assert sql_to_string(query) == f"select null from df"

    def test_default(self):
        with pytest.raises(ValueError):
            _ = sql_to_string(SQL("select $none from df", none={}))

