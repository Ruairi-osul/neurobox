from binit.align import align_around
import pandas as pd
from typing import Dict, List, Optional
from df_grouping_utils import groupby_two_df
import binit


def pivot(
    df: pd.DataFrame,
    neuron_col: str = "neuron_id",
    value_col: str = "value",
    time_col: str = "time",
) -> pd.DataFrame:
    """Pivot a DataFrame to have one neuron per column and one timepoint per row

    Args:
        df (pd.DataFrame): DataFrame
        neuron_col (str, optional): Column containing neuron identifiers. Defaults to "neuron_id".
        value_col (str, optional): Column containing values. Defaults to "value".
        time_col (str, optional): Column containing time identifiers. Defaults to "time".

    Returns:
        pd.DataFrame: DataFrame with one column per neuron and one row per timepoint
    """
    return pd.pivot(df, values=value_col, columns=neuron_col, index=time_col)


def exclude_min_activity_long(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    # TODO
    ...


def exclude_baseline_long(
    df: pd.DataFrame, time_col: str, baseline_before: float = 0,
) -> pd.DataFrame:
    """Exclude data from baseline

    Args:
        df (pd.DataFrame): Input DF
        time_col (str): Column containing time values
        baseline_before (float, optional): Timepoint at which baseline ends. Defaults to 0.

    Returns:
        pd.DataFrame: DF with baseline excluded
    """
    return df.loc[lambda x: x[time_col] >= baseline_before]


def align_to_events(
    df_data: pd.DataFrame,
    df_events: pd.DataFrame,
    time_before_event: Optional[float] = None,
    max_latency: Optional[float] = None,
    df_data_group_colname: str = "group",
    df_events_group_colname: str = "group",
    df_events_timestamp_col: str = "time",
    df_data_time_col: str = "time",
    returned_colname: str = "algined",
) -> pd.DataFrame:
    """Align data to events, by group

    Args:
        df_data (pd.DataFrame): DF containing data to be aligned
        df_events (pd.DataFrame): DF containing events to align to
        time_before_event (Optional[float], optional): If specified, events occuring this latency BEFORE an event will be aligned to that event. Defaults to None.
        max_latency (Optional[float], optional): Data occuring this latency after the last bin are returned as NaN. Defaults to None.
        df_data_group_colname (str, optional): Group col name in df_data. Defaults to "group".
        df_events_group_colname (str, optional): Group col name in df_events. Defaults to "group".
        df_events_timestamp_col (str, optional): Timestamp column in df_events. Defaults to "time".
        df_data_time_col (str, optional): Time column in df_data. Defaults to "time".
        returned_colname (str, optional): Name of the column in df_data which specifies the aligned values. Defaults to "algined".

    Returns:
        pd.DataFrame: df_data with an additional column indicating the rows latency to its closest event.
    """

    def _align_around_one_group(df1, df2):
        df1[returned_colname] = binit.align_around(
            df1[df_data_time_col].values,
            df2[df_events_timestamp_col].values,
            t_before=time_before_event,
            max_latency=max_latency,
        )
        return df1

    return groupby_two_df(
        df1=df_data,
        df2=df_events,
        f=_align_around_one_group,
        df1_group_colname=df_data_group_colname,
        df2_group_colname=df_events_group_colname,
    )


def get_closest_event(
    df_data: pd.DataFrame,
    df_events: pd.DataFrame,
    time_after: Optional[float] = None,
    time_before: Optional[float] = None,
    df_data_group_colname: str = "group",
    df_events_group_colname: str = "group",
    df_events_timestamp_col: str = "time",
    df_data_time_col: str = "time",
    returned_colname: str = "event",
) -> pd.DataFrame:
    """For each row in a DF, get the event it is closest to. Closest refers to most recent previous event (though see time_before)

    Args:
        df_data (pd.DataFrame): DF containing data to be aligned
        df_events (pd.DataFrame): DF containing events to align to
        time_before (Optional[float], optional): If specified, events occuring this latency BEFORE an event will be aligned to that event. Defaults to None.
        time_after (Optional[float], optional): Data occuring this latency after the last bin are returned as NaN. Defaults to None.
        nan_vals_before_first_bin (bool, optional): If True, returns np.nan for values of input timestamps occuring before the after the first bin. Defaults to False.
        df_data_group_colname (str, optional): Group col name in df_data. Defaults to "group".
        df_events_group_colname (str, optional): Group col name in df_events. Defaults to "group".
        df_events_timestamp_col (str, optional): Timestamp column in df_events. Defaults to "time".
        df_data_time_col (str, optional): Time column in df_data. Defaults to "time".
        returned_colname (str, optional): Name of the column in df_data which specifies the aligned values. Defaults to "algined".

    Returns:
        pd.DataFrame: [description]
    """

    def _closest_event_one_group(df1, df2):
        df1[returned_colname] = binit.which_bin(
            arr=df1[df_data_time_col].values,
            bin_edges=df2[df_events_timestamp_col].values,
            time_before=time_before,
            time_after=time_after,
        )
        return df1

    return groupby_two_df(
        df1=df_data,
        df2=df_events,
        f=_closest_event_one_group,
        df1_group_colname=df_data_group_colname,
        df2_group_colname=df_events_group_colname,
    )


def get_closest_event_idx(
    df_data: pd.DataFrame,
    df_events: pd.DataFrame,
    time_before: Optional[float] = None,
    time_after: Optional[float] = None,
    df_data_group_colname: str = "group",
    df_events_group_colname: str = "group",
    df_events_timestamp_col: str = "time",
    df_data_time_col: str = "time",
    returned_colname: str = "event_index",
) -> pd.DataFrame:
    """For each row in a DF, get the event it is closest to. Closest refers to most recent previous event (though see time_before)

    Args:
        df_data (pd.DataFrame): DF containing data to be aligned
        df_events (pd.DataFrame): DF containing events to align to
        time_before (Optional[float], optional): If specified, events occuring this latency BEFORE an event will be aligned to that event. Defaults to None.
        time_after (Optional[float], optional): Data occuring this latency after the last bin are returned as NaN. Defaults to None.
        df_data_group_colname (str, optional): Group col name in df_data. Defaults to "group".
        df_events_group_colname (str, optional): Group col name in df_events. Defaults to "group".
        df_events_timestamp_col (str, optional): Timestamp column in df_events. Defaults to "time".
        df_data_time_col (str, optional): Time column in df_data. Defaults to "time".
        returned_colname (str, optional): Name of the column in df_data which specifies the aligned values. Defaults to "algined".

    Returns:
        pd.DataFrame: [description]
    """

    def _closest_event_one_group(df1, df2):
        df1[returned_colname] = binit.which_bin_idx(
            arr=df1[df_data_time_col].values,
            bin_edges=df2[df_events_timestamp_col].values,
            time_before=time_before,
            time_after=time_after,
        )
        return df1

    return groupby_two_df(
        df1=df_data,
        df2=df_events,
        f=_closest_event_one_group,
        df1_group_colname=df_data_group_colname,
        df2_group_colname=df_events_group_colname,
    )
