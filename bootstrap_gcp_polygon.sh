#bootstrap

# Create this in a config.sh file and source it. 
# export POLYGON_API_KEY="projects/<PROJ NUM>/secrets/polygon/versions/1"
# export REQUESTS_SUBSCRIPTION="projects/<PROJ NUM>/subscriptions/polygon_requested_ticker_chain"
# export definition_file="./option_contract_pubsub_schema.json"
# export REQUESTS_TOPIC="polygon_requested_ticker_chain"
# export BIGQUERY_DEST="bq table name URI here"

source ./config.sh

gcloud auth application-default login

gcloud pubsub schemas create option_contract_schema \
    --type=avro \
    --definition-file= $definition_file

gcloud pubsub topics create $REQUESTS_TOPIC --schema=option_contract_schema

gcloud pubsub subscriptions create $REQUESTS_SUBSCRIPTION --topic= $REQUESTS_TOPIC \
  --bigquery-table=$BIGQUERY_DEST use destination table