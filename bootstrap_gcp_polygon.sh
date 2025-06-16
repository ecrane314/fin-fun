#bootstrap

source ./config.sh

gcloud auth application-default login

gcloud pubsub schemas create option_contract_schema \
    --type=JSON \
    --definition-file= $definition-file

gcloud pubsub topic create -- use schema $REQUESTS_TOPIC

gcloud pubsub subscriptions create $REQUESTS_SUBSCRIPTION --topic= $REQUESTS_TOPIC --bigquery type use destination table