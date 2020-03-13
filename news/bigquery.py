# from google.cloud import bigquery
#
# client = bigquery.Client()
#
# # Perform a query.
# QUERY = (
#     "SELECT SOURCEURL, DATEADDED FROM `gdelt-bq.full.events` where DATEADDED between 20190601 and 20200101")
# query_job = client.query(QUERY)  # API request
# rows = query_job.result()  # Waits for query to finish
#
# for row in rows:
#     print(row.name)
import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage_v1beta1

# Explicitly create a credentials object. This allows you to use the same
# credentials for both the BigQuery and BigQuery Storage clients, avoiding
# unnecessary API calls to fetch duplicate authentication tokens.
credentials, your_project_id = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Make clients.
bqclient = bigquery.Client(
    credentials=credentials,
    project=your_project_id,
)
bqstorageclient = bigquery_storage_v1beta1.BigQueryStorageClient(
    credentials=credentials
)

table = bigquery_storage_v1beta1.types.TableReference()
table.project_id = "gdelt-bq"
table.dataset_id = "full"
table.table_id = "events"

# Select columns to read with read options. If no read options are
# specified, the whole table is read.
read_options = bigquery_storage_v1beta1.types.TableReadOptions()
read_options.selected_fields.append("SOURCEURL")
read_options.selected_fields.append("DATEADDED")
read_options.row_restriction = 'DATEADDED between 20190601 and 20200101'
parent = "projects/{}".format(your_project_id)
session = bqstorageclient.create_read_session(
    table,
    parent,
    read_options=read_options,
    # This API can also deliver data serialized in Apache Avro format.
    # This example leverages Apache Arrow.
    format_=bigquery_storage_v1beta1.enums.DataFormat.ARROW,
    # We use a LIQUID strategy in this example because we only read from a
    # single stream. Consider BALANCED if you're consuming multiple streams
    # concurrently and want more consistent stream sizes.
    sharding_strategy=(
        bigquery_storage_v1beta1.enums.ShardingStrategy.LIQUID
    ),
)

# This example reads from only a single stream. Read from multiple streams
# to fetch data faster. Note that the session may not contain any streams
# if there are no rows to read.
stream = session.streams[0]
position = bigquery_storage_v1beta1.types.StreamPosition(stream=stream)
reader = bqstorageclient.read_rows(position)

# Parse all Avro blocks and create a dataframe. This call requires a
# session, because the session contains the schema for the row blocks.
dataframe = reader.to_dataframe(session)
dataframe.to_csv("news201906")
print(dataframe.head())