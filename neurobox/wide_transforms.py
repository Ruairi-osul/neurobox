import pandas as pd
from typing import Optional, Optional, Callable
from scipy.stats import zmap, zscore
from scipy.ndimage import gaussian_filter1d

def exclude_min_activity_wide(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    # TODO
    ...


def exclude_baseline_wide(
    df: pd.DataFrame,  baseline_before: float = 0,
) -> pd.DataFrame:
    """Exclude data from baseline

    Args:
        df (pd.DataFrame): Input DF
        baseline_before (float, optional): Timepoint at which baseline ends. Defaults to 0.

    Returns:
        pd.DataFrame: DF with baseline excluded
    """
    return df.loc[lambda x: x.index >= baseline_before]


def standardize(
    df: pd.DataFrame, baseline_before: Optional[float] = None
) -> pd.DataFrame:
    """Standardize each column in a dataframe

    Args:
        df (pd.DataFrame): DF in wide format [time, neurons]
        baseline_before (Optional[float], optional): If specified, calculated zscores on values occuring before this point. Defaults to None.

    Returns:
        pd.DataFrame: Standarsized DF
    """

    def _standardize_col(col, baseline_before=None):
        if baseline_before is not None:
            return zmap(col, col.loc[lambda x: x.index < baseline_before])
        else:
            return zscore(col)

    return df.apply(_standardize_col, baseline_before=baseline_before)


def gaussian_smooth(df: pd.DataFrame, sigma: float) -> pd.DataFrame:
    """Apply a gaussian smoothing transformation to each column in a dataframe

    Args:
        df (pd.DataFrame): DF in wide format
        sigma (float): Sigma perameter for gaussian smoothing. Larger values increase kernel width. Returns original DF if sigma is 0.

    Returns:
        pd.DataFrame: DF with smoothed values
    """
    if sigma == 0:
        return df
    return df.apply(gaussian_filter1d, sigma=sigma)

def sort_by_activity_in_range(
    df: pd.DataFrame, t_start: float, t_stop: float, agg_func: Callable,
) -> pd.DataFrame:
    """Sort columns of a DataFrame in wide format by values in a given time range

    Args:
        df (pd.DataFrame): DataFrame in format (time, neurons)
        t_start (float): Start point of window
        t_stop (float): End point of window
        agg_func (Callable): Function to use to aggregate values for sorting (e.g. np.mean)

    Returns:
        pd.DataFrame: Input DataFrame with columns sorted by aggregation (larger to the left)
    """
    idx = (
        df.loc[(df.index <= t_start) & (df.index <= t_stop)]
        .apply(agg_func)
        .sort_values(ascending=False)
        .index.values
    )
    return df[idx]

def resample(
    df: pd.DataFrame,
    new_interval: str,
) -> pd.DataFrame:
    """Resample a dataset. Works best if in long format

    Args:
        df (pd.DataFrame): DataFrame containing the dataset
        new_interval (str): String code for new time interval
        time_col (str, optional): Time column in existing dataset. Defaults to "time".
        grouping_cols (Optional[List[str]], optional): Columns used to group by for resampling. Defaults to None.

    Returns:
        pd.DataFrame: Resampled DF
    """
    df["time"] = pd.to_timedelta(df.index, unit="s")
    df = df.set_index("time")
    return (
        df.resample(new_interval)
        .mean()
        .reset_index()
        .assign(time=lambda x: x["time"].dt.total_seconds())
        .set_index("time")
    )

def exclude_after(df: pd.DataFrame, max_time: float):
    ...