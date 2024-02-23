import os
import re
from typing import List, Optional, Union

import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def init_duckdb_s3() -> None:
    """
    Set up S3 credentials for DuckDB.
    """
    duckdb.sql(
        f"""
        SET s3_endpoint='{os.getenv("AWS_S3_ENDPOINT")}';
        SET s3_access_key_id='{os.getenv("AWS_ACCESS_KEY_ID")}';
        SET s3_secret_access_key='{os.getenv("AWS_SECRET_ACCESS_KEY")}';
        SET s3_session_token='';
        """
    )


def read_all_data(path: str) -> None:
    """
    Create a VIEW `data` to be queried with DuckDB containing
    all log data stored on S3.

    Args:
        path (str): Path to log parquet files.
    """
    duckdb.sql("ALTER VIEW IF EXISTS test_data RENAME TO data")
    duckdb.sql(
        f"""
        CREATE VIEW test_data
        AS SELECT * FROM read_parquet("{path}", hive_partitioning=1)
        """
    )


def make_histogram(
    data: pd.DataFrame,
    var_name: str,
    yaxis_title: Optional[str] = None,
    xaxis_title: Optional[str] = None,
    opacity: float = 0.7,
    color: str = "#040548",
):
    """
    Make histogram of variable `var_name` in DataFrame `data`.

    Args:
        data (pd.DataFrame): Data.
        var_name (str): Variable name.
        yaxis_title (str): Y axis title.
        xaxis_title (str): X axis title.
        opacity (float): Opacity.
        color (str): Color hex.
    """
    fig = go.Figure(
        data=[go.Histogram(x=data[var_name], opacity=opacity, marker=dict(color=color))],
    )
    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        margin=dict(l=0, r=0, b=0, t=0),
    )
    return fig


def make_barplot(
    data: pd.DataFrame,
    var_x: str,
    var_count: str,
    yaxis_title: Optional[str] = None,
    xaxis_title: Optional[str] = None,
    opacity: float = 0.7,
    color: str = "#040548",
    range_color: Optional[List[Union[int, float]]] = None,
    range_y: Optional[List[Union[int, float]]] = None,
    barmode: str = "relative",
    legend_title: str = "",
):
    """
    Make a barplot for var_x.

    Args:
        data (pd.DataFrame): Data.
        var_x (str): X variable.
        var_y (str): Count variable.
        yaxis_title (Optional[str]): Y axis title.
        xaxis_title (Optional[str]): X axis title.
        opacity (float): Opacity.
        color (str): Color or variable.
        range_color (Optional[List[Union[int, float]]]): Color range.
        range_y (Optional[List[Union[int, float]]]): Y range.
        barmode (str): Bar mode.
        legend_title (str): Legend title.
    """
    if is_valid_hex_color(color):
        fig = px.bar(data, x=var_x, y=var_count, opacity=opacity, range_y=range_y, barmode=barmode)
        fig.update_traces(marker_color=color)
    else:
        fig = px.bar(
            data,
            x=var_x,
            y=var_count,
            opacity=opacity,
            color=color,
            color_continuous_scale="rdylgn",
            range_color=range_color,
            range_y=range_y,
            barmode=barmode,
        )
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=legend_title,
            )
        )

    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        margin=dict(l=0, r=0, b=0, t=0),
    )
    return fig


def is_valid_hex_color(color: str) -> bool:
    """
    Return True if color is a hex code and False otherwise.

    Args:
        hex_code (str): Hex code.

    Returns:
        bool: True or False.
    """
    # Define a regular expression pattern for a valid color hex code.
    hex_color_pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"

    # Use the re.match function to check if the string matches the pattern.
    if re.match(hex_color_pattern, color):
        return True
    else:
        return False
