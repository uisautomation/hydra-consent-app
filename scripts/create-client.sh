#!/usr/bin/env bash
#
# Use Hydra command line client to create a test client application with id
# "consent" capable of accessing hydra consent requests.
#
set -xe
docker-compose exec hydra hydra clients create \
    --id consent --secret secret \
    --grant-types client_credentials \
    --response-types token \
    --allowed-scopes hydra.consent
