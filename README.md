Moved to https://gitlab.developers.cam.ac.uk/uis/devops/raven/hydra-consent-app

# Hydra Consent App for the University of Cambridge

[![Build Status](https://travis-ci.org/uisautomation/hydra-consent-app.svg?branch=master)](https://travis-ci.org/uisautomation/hydra-consent-app)
[![codecov](https://codecov.io/gh/uisautomation/hydra-consent-app/branch/master/graph/badge.svg)](https://codecov.io/gh/uisautomation/hydra-consent-app)

This repository contains a "consent app" implementation for the
[Hydra](https://github.com/ory/hydra) OAuth2 server which integrates
[Raven](https://raven.cam.ac.uk) SSO.

See the [documentation](https://uisautomation.github.io/hydra-consent-app/) for
information about how to get a developer instance running.

## Quick test

As a quick test, you can spin up the consent app and try issuing a token with
the following:

```console
$ ./compose.sh development up -d
```

Then, in another terminal:

```console
$ ./scripts/create-token.sh
```

## Running tests

The test suite may be run using the ``tox.sh`` wrapper script.
