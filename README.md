# Hydra Consent App for the University of Cambridge

This repository contains a "consent app" implementation for the
[Hydra](https://github.com/ory/hydra) OAuth2 server which integrates
[Raven](https://raven.cam.ac.uk) SSO.

See the [documentation](https://uisautomation.github.io/hydra-consent-app/) for
information about how to get a developer instance running.

## Quick test

As a quick test, you can spin up the consent app and try issuing a token with
the following:

```console
$ docker-compose up devserver
```

Then, in another terminal:

```console
$ ./scripts/create-token.sh
```
