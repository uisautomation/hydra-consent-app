#!/usr/bin/env bash
#
# Example of manually triggering the consent flow to obtain a token for the
# testclient application. See ./create-client.sh.
#
set -xe

scopes=${1-example}

# Change to this script's directory
cd "$( dirname "${BASH_SOURCE[0]}")"

echo "-- Requesting token with scopes: ${scopes}"

../compose.sh development exec hydra \
    hydra token user \
    --auth-url http://localhost:4444/oauth2/auth \
    --token-url http://hydra:4444/oauth2/token \
    --id application --secret secret \
    --scopes "${scopes}"
