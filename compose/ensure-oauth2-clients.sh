#!/usr/bin/env sh
set -xe

# Install bash for wait-for-it.sh
if [ -z "$(which bash)" ]; then
    apk add --no-cache bash
fi

# Change into directory containing clients
cd /tmp/compose/oauth2-clients

# Wait for hydra to come up
/tmp/compose/wait-for-it.sh hydra:4444

# Connect to hydra instance
hydra connect --url http://hydra:4444/ --id hydraroot --secret secret

# Delete and re-create OAuth2 clients
for client_file in /tmp/compose/oauth2-clients/*.json; do
    client_id=$(basename $client_file .json)
    echo "Importing client id: ${client_id}"
    hydra clients delete ${client_id} || echo "-- client not deleted"
    hydra clients import ${client_file}
done

# Delete and re-create the introspect policy
hydra policies delete introspect-policy \
    || echo "-- introspect-policy not deleted"

hydra policies create --actions introspect \
    --description "Allow all clients with hydra.consent to examine consent requests" \
    --actions get,accept,reject \
    --allow \
    --id consent-policy \
    --resources "rn:hydra:oauth2:consent:requests:<.*>" \
    --subjects "<.*>"
