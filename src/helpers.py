import os
import re
from typing import List, Optional, Union

import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


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


def read_all_data(path: str, data_name: str) -> None:
    """
    Create a VIEW `data` to be queried with DuckDB containing
    all log data stored on S3.

    Args:
        path (str): Path to log parquet files.
    """
    duckdb.sql(
        f"""
        CREATE OR REPLACE VIEW {data_name} AS
        SELECT
            *,
            CASE
                WHEN "Response.IC" > 1 THEN 1
                ELSE "Response.IC"
            END AS "Response.IC"
        FROM
            read_parquet("{path}", hive_partitioning=1);
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
    show_values: bool = False,
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

    if show_values:
        fig.update_traces(text=data[var_count].round(2), textposition="inside")

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


def calculate_accuracy_levels(
    data: pd.DataFrame, threshold: float, mapping: dict, pct: bool
) -> dict:
    """
    Calculate accuracy levels for each level of the NAF code hierarchy.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data.
        threshold (float): The threshold value for accuracy calculation.
        mapping (dict): A dictionary mapping NAF codes to their corresponding labels.
        pct (bool): A flag indicating whether to return accuracy levels as percentages.

    Returns:
        dict: A dictionary containing the accuracy levels for each level of the NAF code hierarchy.
    """

    naf_names = ["Sous-classe", "Classe", "Groupe", "Division", "Section"]
    accuracy_levels = {}

    # Calculate accuracy levels for each level
    for level in range(5, 1, -1):
        # Calculate accuracy level
        accuracy = np.where(
            data["Response.IC"] > threshold,
            (data["apet_manual"].str[:level] == data["Response.1.code"].str[:level]).astype(int),
            1,
        ).mean()

        # Store accuracy level in dictionary
        accuracy_levels[naf_names[5 - level]] = accuracy

    data = data.copy()
    # Calculate accuracy level for level 1
    data["ground_truth_lvl1"] = data["apet_manual"].str[:2].map(mapping)
    data["pred_lvl1"] = data["Response.1.code"].str[:2].map(mapping)
    accuracy = np.where(
        data["Response.IC"] > threshold,
        (data["ground_truth_lvl1"] == data["pred_lvl1"]).astype(int),
        1,
    ).mean()
    accuracy_levels[naf_names[-1]] = accuracy

    accuracy_levels = pd.DataFrame.from_dict(accuracy_levels, orient="index").reset_index()

    if pct:
        accuracy_levels[0] = accuracy_levels[0] * 100

    return accuracy_levels.rename(columns={"index": "Level", 0: "accuracy"})


def calculate_topk_accuracy(data: pd.DataFrame, threshold: float, pct: bool) -> dict:
    """
    Calculate the top-k accuracy levels for a given DataFrame.

    Args:
        data (pd.DataFrame): The DataFrame containing the data.
        threshold (float): The threshold value for the accuracy calculation.
        pct (bool): Flag indicating whether to return the accuracy as a percentage.

    Returns:
        dict: A dictionary containing the top-k accuracy levels.

    Raises:
        None

    Examples:
        >>> df = pd.DataFrame(...)
        >>> calculate_topk_accuracy(df, 0.5, True)
    """
    accuracy_topk = {}

    # Calculate accuracy levels for each k value
    for k in range(1, 6):
        # Calculate accuracy level
        if k == 1:
            accuracy = np.where(
                data["Response.IC"] > threshold, data["result"].astype(int), 1
            ).mean()
        else:
            past_topk = [data[f"Response.{i}.code"] for i in range(1, k)]
            # Check if any of the top k predicted labels matches the manual label
            matches_manual = pd.concat(
                [data["apet_manual"] == code for code in past_topk], axis=1
            ).any(axis=1)
            accuracy = (
                np.where(
                    data["Response.IC"] > threshold,
                    matches_manual | (data["apet_manual"] == data[f"Response.{k}.code"]),
                    1,
                )
                .astype(int)
                .mean()
            )

        # Store accuracy level in dictionary
        accuracy_topk[f"Top {k}"] = accuracy

    accuracy_topk = pd.DataFrame.from_dict(accuracy_topk, orient="index").reset_index()

    if pct:
        accuracy_topk[0] = accuracy_topk[0] * 100

    return accuracy_topk.rename(columns={"index": "Top k", 0: "accuracy"})


def plot_IC_distrib(
    data: pd.DataFrame,
    var_x: str,
    var_count: str,
    nbins: int,
    vline: Optional[float] = None,
    yaxis_title: Optional[str] = None,
    xaxis_title: Optional[str] = None,
    legend_title: Optional[str] = None,
    color_discrete_sequence: Optional[List[str]] = None,
    range_y: Optional[List[Union[int, float]]] = None,
    barmode: str = "overlay",
):
    fig = px.histogram(
        data,
        x=var_x,
        color=var_count,
        nbins=nbins,
        barmode=barmode,
        color_discrete_sequence=color_discrete_sequence,
    )

    if vline:
        fig.add_vline(x=vline, line=dict(color="black", width=1, dash="dash"))
    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title=legend_title,
        margin=dict(l=0, r=0, b=0, t=0),
    )
    return fig
