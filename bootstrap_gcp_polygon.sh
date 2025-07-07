# bootstrap
# Copy these veriables to your config.sh file.

# Exit immediately on error
#set -e

# export PROJECT_ID=
# export POLYGON_API_KEY="projects/<PROJ NUM>/secrets/polygon/versions/1"
# export REQUESTS_TOPIC="polygon_requested_ticker_chain"
# export REQUESTS_SUBSCRIPTION="projects/<PROJ NUM>/subscriptions/<SUB>"
# export PAYLOAD_SCHEMA_DEFINITION="./option_contract_pubsub_schema.json"
# export PAYLOAD_SCHEMA="gcp pubsub schema name"
# export PAYLOAD_TOPIC="polygon_payload_json"
# export BIGQUERY_DEST="fully qualified bq table name here"
# export PAYLOAD_SUBSCRIPTION=

source ./config.sh

# Comment in if app default credentials not set
# gcloud auth application-default login

gcloud pubsub topics create $REQUESTS_TOPIC

gcloud pubsub subscriptions create $REQUESTS_SUBSCRIPTION --topic=\
$REQUESTS_TOPIC

gcloud pubsub schemas create $PAYLOAD_SCHEMA \
    --type=avro \
    --definition-file=$PAYLOAD_SCHEMA_DEFINITION

gcloud pubsub topics create $PAYLOAD_TOPIC --schema=$PAYLOAD_SCHEMA \
    --message-encoding=json

bq mk -t $BIGQUERY_DEST_TABLE

gcloud pubsub subscriptions create $PAYLOAD_SUBSCRIPTION --topic=$PAYLOAD_TOPIC \
  --topic-project=$PROJECT_ID 
  --bigquery-table=$BIGQUERY_DEST_TABLE \
  --use-topic-schema
