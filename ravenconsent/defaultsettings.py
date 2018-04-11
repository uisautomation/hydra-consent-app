"""
Default settings values for the :py:mod:`ravenconsent` application.

"""
# Variables whose names are in upper case and do not start with an underscore from this module are
# used as default settings for the ravenconsent application. See AssetsConfig in .apps for
# how this is achieved. This is a bit mucky but, at the moment, Django does not have a standard way
# to specify default values for settings.  See: https://stackoverflow.com/questions/8428556/

SUBJECT_SCHEME = 'mock'
"""
Scheme used to namespace the identifiers returned by Raven. For production this should be "crsid".
For development/test use "mock".

"""

CONSENT_CLIENT_ID = None
"""
OAuth2 client id which the consent app uses to identify itself to the OAuth2 token introspection
endpoint.

"""

CONSENT_CLIENT_SECRET = None
"""
OAuth2 client secret which the consent app uses to identify itself to the OAuth2 token
introspection endpoint.

"""

HYDRA_TOKEN_ENDPOINT = None
"""
URL of the OAuth2 token endpoint the API server uses to request an authorisation token to perform
OAuth2 token introspection.

"""

HYDRA_CONSENT_REQUESTS_ENDPOINT = None
"""
Endpoint which forms the base URL for consent requests. For example, if hydra is installed at
``http://hydra.invalid/``, this should be ``http://hydra.invalid/oauth2/consent/requests/``.

"""

CONSENT_PROMPT_NONE_SCOPE = 'prompt:none'
"""
Consent requests with this scope are either granted or denied based upon whether the user is
authenticated or not and will not show the Raven login if the user is not currently authenticated.

"""
