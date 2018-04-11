#!/usr/bin/env bash
#
# Use Hydra command line client to create a test client applications:
#
# - consent: a client which can request hydra.consent scope
#
# - application: a client which can request the "example" and "prompt:none"
#   scopes
#
set -xe

# A convenient alias for calling hydra
function hydra() {
    docker-compose exec hydra hydra $@
}

# Delete any existing clients. It is OK for these calls to fail if the
# corresponding clients did not exist
hydra clients delete consent || echo "-- client 'consent' not deleted"
hydra clients delete application || echo "-- client 'application' not deleted"

# Create clients
hydra clients create \
    --id consent --secret secret \
    --grant-types client_credentials \
    --response-types token \
    --allowed-scopes hydra.consent

hydra clients create \
    --id application --secret secret \
    --grant-types authorization_code \
    --response-types token,code \
    --allowed-scopes example,prompt:none \
    --callbacks http://localhost:4445/callback
