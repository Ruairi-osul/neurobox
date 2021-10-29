import numpy as np
import pandas as pd
from typing import Optional
from itertools import combinations
from .utils import create_combined_col

def pairwise_correlation(
    df: pd.DataFrame,
    rectify: bool = False,
    zero_diag: bool = True,
    fillna: Optional[float] = None,
) -> pd.DataFrame:
    """Correlate each neuron in a wide df (time, neurons)

    Args:
        df (pd.DataFrame): DF in wide format (time, neurons)
        rectify (bool, optional): Whether to set negative correlations to 0. Defaults to False.
        zero_diag (bool, optional): Whether to set correlations along the diagonal to zero. Defaults to True.
        fillna (Optional[float], optional): If specified, fills NA values with this value prior to calculating correlations. Defaults to None.

    Returns:
        pd.DataFrame: A DF correlation matrix (neurons, neurons)
    """
    if fillna is not None:
        df = df.fillna(fillna)
    res = np.corrcoef(df)
    if rectify:
        res = np.where(res < 0, 0, res)
    if zero_diag:
        np.fill_diagonal(res, 0)
    df = pd.DataFrame(res, columns=df.index.values)
    df.index = df.columns
    return df

def correlation_matrix_to_tidy(df: pd.DataFrame) -> pd.DataFrame:
    """Convert a correlation matrix df to one with one row per neuron combination

    Args:
        df (pd.DataFrame): DF correlation matrix

    Returns:
        pd.DataFrame: DF with one row per neuron combination column for correlation value
    """
    df = (
        df.reset_index()
        .melt(id_vars="index")
        .rename(columns={"index": "neuron_1", "variable": "neuron_2"})
    )
    df = create_combined_col(
        df, c1="neuron_1", c2="neuron_2", returned_colname="neuron_combination"
    )
    # exclude duplicates
    combs = list(combinations(df["neuron_1"].unique(), r=2))
    good_combs = [f"{c1}_{c2}" for c1, c2 in combs if c1 != c2]
    return df[lambda x: x["neuron_combination"].isin(good_combs)]