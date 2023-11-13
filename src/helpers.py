import os
import re
from typing import Optional

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
    duckdb.sql(
        f"""
        CREATE OR REPLACE VIEW data
        AS SELECT * FROM read_parquet("{path}", hive_partitioning=1)
        """
    )


def write_all_data_to_parquet() -> None:
    """
    Write all log data to a single parquet file for
    DuckDB-Wasm (Observable).
    """
    duckdb.sql("SELECT * FROM data").write_parquet("data/data.parquet")


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
    barmode: str = "relative",
):
    """
    Make a barplot for var_x.

    Args:
        data (pd.DataFrame): Data.
        var_x (str): X variable.
        var_y (str): Count variable.
        yaxis_title (str): Y axis title.
        xaxis_title (str): X axis title.
        opacity (float): Opacity.
        color (str): Color or variable.
        barmode (str): Bar mode.
    """
    if is_valid_hex_color(color):
        fig = px.bar(data, x=var_x, y=var_count, opacity=opacity, barmode=barmode)
        fig.update_traces(marker_color=color)
    else:
        fig = px.bar(data, x=var_x, y=var_count, opacity=opacity, color=color, barmode=barmode)
    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
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
