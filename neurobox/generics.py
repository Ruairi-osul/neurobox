"""Adaptations of generic pandas methods to allow them to be exposed to the compose interface.
"""

from typing import Callable, Dict, List 
import pandas as pd


def rename(df: pd.DataFrame, **column_mapping: Dict[str, str]):
    """Rename a column of the input DataFrame

    Args:
        df (pd.DataFrame): Input DF

    Returns:
        pd.DataFrame: DataFrame with updated columns
    """
    return df.rename(columns=column_mapping)


def drop_cols(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Drop columns from input DataFrame

    Args:
        df (pd.DataFrame): DF
        cols (List[str]): Columns to drop

    Returns:
        pd.DataFrame: Input DataFrame with provided columns dropped
    """
    return df.drop(cols, axis=1)


def dropna_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with NA values

    Args:
        df (pd.DataFrame): Input DF

    Returns:
        pd.DataFrame: DF without NA rows
    """
    return df.dropna()

def assign_col(df: pd.DataFrame, col_name: str, func: Callable) -> pd.DataFrame:
    return df.assign(**{col_name: func})

def select_cols(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    return df[cols]

def filter_rows(df: pd.DataFrame, condition: Callable) -> pd.DataFrame:
    return df.loc[condition]

def set_index(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return df.set_index(col)