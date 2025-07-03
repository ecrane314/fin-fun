#bootstrap

# Create this in a config.sh file and source it. 
# export POLYGON_API_KEY="projects/<PROJ NUM>/secrets/polygon/versions/1"
# export REQUESTS_SUBSCRIPTION="projects/<PROJ NUM>/subscriptions/<SUB>"
# export definition_file="./option_contract_pubsub_schema.json"
# export PAYLOAD_SCHEMA="gcp pubsub schema name"
# export REQUESTS_TOPIC="polygon_requested_ticker_chain"
# export PAYLOAD_TOPIC="polygon_payload_json"
# export BIGQUERY_DEST="bq table name URI here"

source ./config.sh

gcloud auth application-default login

gcloud pubsub topics create $REQUESTS_TOPIC

gcloud pubsub schemas create $PAYLOAD_SCHEMA \
    --type=avro \
    --definition-file= $definition_file

gcloud pubsub topics create $PAYLOAD_TOPIC --schema=option_contract_schema

bq mk -t $BIGQUERY_DEST_TABLE

gcloud pubsub subscriptions create $REQUESTS_SUBSCRIPTION --topic= $REQUESTS_TOPIC \
  --bigquery-table=$BIGQUERY_DEST_TABLE use destination table
