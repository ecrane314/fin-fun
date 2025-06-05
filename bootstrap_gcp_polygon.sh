#bootstrap

touch config



gcloud auth application-default login

gcloud pubsub schemas create option_contract_schema \
    --type=JSON \
    --definition-file=./option_contract_pubsub_schema.json

gcloud pubsub topic create -- use schema

gcloud pubsub subscriptions create --topic --bigquery type use destination table