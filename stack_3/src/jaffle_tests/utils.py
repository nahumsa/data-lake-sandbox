import pandas as pd
from typing import Callable, Any

def transform_test(test_df: pd.DataFrame, true_df: pd.DataFrame, transform: Callable[[pd.DataFrame, any], pd.DataFrame], **kwargs) -> None:
    """Tests that transforms are idempotent and are equals to a ground truth.

    Args:
        test_df (pd.DataFrame): Dataframe that you want to test.
        true_df (pd.DataFrame): Ground truth dataframe
        transform (Callable[[pd.DataFrame, ...], pd.DataFrame]): transform to test on the test_df.


    Raises:
        AssertionError: When test_df is not equal to true_df
    """

    df_before_transform = test_df.copy()
    transform_df = transform(test_df, **kwargs)

    # Assert idempotency
    pd.testing.assert_frame_equal(test_df, df_before_transform)
    # Assert tranformation
    pd.testing.assert_frame_equal(transform_df, true_df)

class FunctionalTestTransform:
    def __init__(self, test_df, true_df):
        self._test_df = test_df
        self._true_df = true_df

    def __call__(self, function: Callable[[pd.DataFrame, any], pd.DataFrame], **kwargs) -> Any:
        transform_test(self._test_df, self._true_df, function, **kwargs)
