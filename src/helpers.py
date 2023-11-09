import os

import duckdb
import pandas as pd
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


def make_chart(data: pd.DataFrame, var_name: str, opacity: float = 0.7, color: str = "#040548"):
    """
    Make histogram of variable `var_name` in DataFrame `data`.

    Args:
        data (pd.DataFrame): Data.
        var_name (str): Variable name.
        opacity (float): Opacity.
        color (str): Color hex.
    """
    fig = go.Figure(
        data=[go.Histogram(x=data[var_name], opacity=opacity, marker=dict(color=color))],
    )
    return fig
