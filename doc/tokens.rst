Issuing tokens
==============

If you are running the consent app via docker-compose, you can try out granting
tokens.

Create clients
``````````````

Make sure you've created the appropriate OAuth2 clients via:

.. code-block:: bash

    $ ./scripts/create-clients.sh

This will create two OAuth2 clients:

consent
    An OAuth2 client for the consent app itself which uses client credentials
    for authorisation and can be granted the ``hydra.consent`` scope to perform
    user consent flow.

application
    An example OAuth2 client for obtaining a token. This application is allowed
    to perform the authorisation code flow and can request the ``example`` and
    ``prompt:none`` scopes.

Issue a token
`````````````

The normal flow can be demonstrated via:

.. code-block:: bash

    $ ./scripts/create-token.sh example

This will create an authorisation request for the ``example`` scope. The script
prints a URL which you can paste into the browser (in a private browsing tab).
The demo Raven login page will be shown and you can log in as a test user.

Running the script a second time should issue the token immediately as your
session will be saved in a browser cookie.

The "prompt:none" flow
``````````````````````

As an extension to the usual flow, if you request the ``prompt:none`` scope, you
will never be re-directed to the login page. Request a new token via:

.. code-block:: bash

    $ ./scripts/create-token.sh example,prompt:none

Open a new private browsing tab and visit the URL shown. You should see an
immediate rejection of the request. Requesting a token without ``prompt:none``
should result in the usual login box. After logging in once, further
``prompt:none`` requests should succeed.
