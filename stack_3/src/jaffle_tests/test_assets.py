import pandas as pd

from jaffle.assets.transformations import rename_column
from .utils import FunctionalTestTransform

class TestAssetsTransformations:
    def test_rename_column(self):
        test_df = pd.DataFrame([
            {"id": 0, "value": 1},
            {"id": 1, "value": 2},
            {"id": 2, "value": 10},
            {"id": 3, "value": 11},
        ])

        true_df = pd.DataFrame([
            {"new_id": 0, "value": 1},
            {"new_id": 1, "value": 2},
            {"new_id": 2, "value": 10},
            {"new_id": 3, "value": 11},
        ])

        func_test = FunctionalTestTransform(test_df=test_df, true_df=true_df)
        func_test(rename_column, column_dict={"id": "new_id"})