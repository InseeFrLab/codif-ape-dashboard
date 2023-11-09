import os

import duckdb
import pandas as pd
import plotly.graph_objects as go


def read_data(path: str):
    duckdb.sql(
        f"""
        SET s3_endpoint='{os.getenv("AWS_S3_ENDPOINT")}';
        SET s3_access_key_id='{os.getenv("AWS_ACCESS_KEY_ID")}';
        SET s3_secret_access_key='{os.getenv("AWS_SECRET_ACCESS_KEY")}';
        SET s3_session_token='';
        """
    )

    duckdb.sql(
        f"""
        CREATE OR REPLACE VIEW data
        AS SELECT * FROM read_parquet("{path}", hive_partitioning=1)
        """
    )

    test = duckdb.sql(
        """
        SELECT
            COUNT(*) AS TotalRows,
            (COUNT(
                CASE WHEN data."Response.IC" > 0.8 THEN 1 END
                ) * 100.0 / COUNT(*)
            ) AS PercentageHighIC
        FROM data;
        """
    )

    # Write all data to unique parquet file
    duckdb.sql("SELECT * FROM data").write_parquet("data/data.parquet")

    test2 = duckdb.sql(
        """
    SELECT
        data."Query.Auto",
        COUNT(*) AS Occurrences,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM data) AS Percentage
    FROM
        data
    GROUP BY
        data."Query.Auto";
    """
    )

    df = duckdb.sql("SELECT * FROM data").to_df()

    return {"data": df, "values": test.to_df().to_dict(), "values2": test2.to_df()}


def make_chart(data: pd.DataFrame):
    fig = go.Figure(
        data=[go.Histogram(x=data["Response.IC"], opacity=0.7, marker=dict(color="#040548"))],
    )
    return fig
