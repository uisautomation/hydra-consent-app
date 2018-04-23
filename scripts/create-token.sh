#!/usr/bin/env bash
#
# Example of manually triggering the consent flow to obtain a token for the
# testclient application. See ./create-client.sh.
#
set -xe

scopes=${1-example}

echo "-- Requesting token with scopes: ${scopes}"
docker-compose exec hydra hydra token user \
    --id application --secret secret \
    --scopes "${scopes}"
