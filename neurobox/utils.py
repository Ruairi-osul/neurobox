import pandas as pd
from typing import Optional

def create_combined_col(
    df: pd.DataFrame, c1: str, c2: str, returned_colname: Optional[str] = None
) -> pd.DataFrame:
    """Create a column which is combination of existing columns

    Args:
        df (pd.DataFrame): Input DF
        c1 (str): Name of first column
        c2 (str): Name of second column
        returned_colname (Optional[str], optional): Name of created column. Defaults to 'c1_c2'.

    Returns:
        pd.DataFrame: Original df with appended column
    """
    if returned_colname is None:
        returned_colname = f"{c1}_{c2}"
    return df.assign(
        **{
            returned_colname: lambda x: x[c1].astype(str).str.cat(x[c2].astype(str), sep="_")
        }
    )