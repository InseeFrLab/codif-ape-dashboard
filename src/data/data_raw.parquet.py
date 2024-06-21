import duckdb
import os

URL = "s3://projet-ape/log_files/dashboard/**/*.parquet"

con = duckdb.connect(database=":memory:")


LIST_VAR = """date, "Response.1.code" """
# Setting up S3 connection
con.execute(f"""
SET s3_endpoint='{os.getenv("AWS_S3_ENDPOINT")}';
SET s3_access_key_id='{os.getenv("AWS_ACCESS_KEY_ID")}';
SET s3_secret_access_key='{os.getenv("AWS_SECRET_ACCESS_KEY")}';
SET s3_session_token='';

COPY(
SELECT
    {LIST_VAR},
    CASE
        WHEN "Response.IC" > 1 THEN 1
        ELSE "Response.IC"
    END AS "Response.IC"
FROM
    read_parquet('{URL}', hive_partitioning=1)
) TO STDOUT (FORMAT 'parquet', COMPRESSION 'gzip');
""")


con.close()
