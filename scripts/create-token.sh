#!/usr/bin/env bash
#
# Example of manually triggering the consent flow to obtain a token for the
# testclient application. See ./create-client.sh.
#
set -xe
docker-compose exec hydra hydra token user \
    --id hydraroot --secret secret \
    --scopes hydra
