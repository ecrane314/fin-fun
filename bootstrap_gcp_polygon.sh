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
    --type=JSON \
    --definition-file= $definition_file

gcloud pubsub topic create -- use schema $REQUESTS_TOPIC

gcloud pubsub subscriptions create $REQUESTS_SUBSCRIPTION --topic= $REQUESTS_TOPIC --bigquery type use destination table