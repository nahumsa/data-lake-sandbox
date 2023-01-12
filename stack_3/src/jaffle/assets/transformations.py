import pandas as pd
from typing import Dict

def rename_column(df: pd.DataFrame, column_dict: Dict[str, str]) -> pd.DataFrame:
    _df = df.copy()
    return _df.rename(columns=column_dict)