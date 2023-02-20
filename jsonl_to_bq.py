#!/usr/bin/env python

"""
Load jsonl file into BigQuery Table
https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-json#python

Preparation
1-- IAM, set service account access for BQ Data Editor to create and write tables
2-- Use this export statement at shell to set your credentials before runtime
export GOOGLE_APPLICATION_CREDENTIALS=/home/MyHomeDir/keys/<SERVICE ACCT PRV KEY>.json

# Read JSONL file and append write to BQ Table
# Upsert needed as duplicates? Unique on the date of the observation
# Need a new table per series? Yes. Run the joins as needed.

BigQuery Python Client Library Documentation
https://cloud.google.com/python/docs/reference/bigquery/latest/index.html
"""

from google.cloud import bigquery

PROJECT= "crane-gcp"
DATASETID = "fred"
BUCKET = "gs://ce-demo2/bq/icoads_core_2005-*.csv"
PREFIX = "/fred/outbound/"


# BigQuery client constructor
bq_client = bigquery.Client()


def load_bq_from_uri(uri, dataset = DATASETID):
    """Load jsonl data from GCS into BigQuery
    respond to GCS obj finalization notifications"""
    #TODO create gcs notifications OR use functions
    #TODO update table naming logic to inherit from uri tail
    # Create table reference
    #TODO this is broken
    table_ref = bigquery.TableReference(project=PROJECT, dataset_id=dataset, table="scratch")

    # Set job config
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig
    job_config = bigquery.LoadJobConfig(
        autodetect = True,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    # Run job
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client
    # https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#jobconfigurationload
    load_job = bq_client.load_table_from_uri(
        uri,
        table_ref,
        location="us-central1",  # Must match the destination dataset location.
        job_config=job_config,
    )

    print(load_job.result)



def load_bq_from_file(series, dataset_id=DATASETID):
    """Submit a BigQuery load job which reads from local jsonl file."""

    # Input filename
    filename = series + ".jsonl.temp"
    table_id = series

    # Pointer to our target dataset
    dataset_ref = bq_client.dataset(dataset_id)

    # Create our load job configuration
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True

    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE


    with open(filename, 'rb') as f01:
        load_job = bq_client.load_table_from_file(
            f01, dataset_ref.table(table_id), job_config=job_config)

    print(f"Starting job {load_job.job_id}")

    # Waits for table load job to complete, inform us.
    load_job.result()
    print("Job finished.")


if __name__=="__main__":
    load_bq_from_uri("")