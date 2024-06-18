import duckdb
import os

URL = "s3://projet-ape/log_files/dashboard/**/*.parquet"

con = duckdb.connect(database=':memory:')

# Setting up S3 connection
con.execute(f"""
SET s3_endpoint='{os.getenv("AWS_S3_ENDPOINT")}';
SET s3_access_key_id='projet-ape-sa';
SET s3_secret_access_key='0obEe7LB59g1Zj65nueDa84OQvrlyfPH';
SET s3_session_token='';

COPY(
SELECT
    *,
    CASE
        WHEN "Response.IC" > 1 THEN 1
        ELSE "Response.IC"
    END AS "Response.IC"
FROM
    read_parquet('{URL}', hive_partitioning=1)
) TO STDOUT (FORMAT 'parquet', COMPRESSION 'gzip');
""")


con.close()
