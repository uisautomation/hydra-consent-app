"""
Client for Hydra server.

"""
import datetime
import enum

from django.conf import settings
from django.http import HttpResponseRedirect
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from dateutil import tz
from dateutil.parser import parse as parse_datetime


SCOPES = ['hydra.consent']


class Decision(enum.Enum):
    """Represent a decision on whether to accept or reject a consent request."""
    ACCEPT = 'accept'
    REJECT = 'reject'


class ConsentError(ValueError):
    """Raised when there is an error fetching or validating the consent."""
    pass


def retrieve_consent(consent_id):
    """Retrieve information on consent from hydra."""
    r = _request(
        method='GET', url=settings.HYDRA_CONSENT_REQUESTS_ENDPOINT + consent_id, timeout=5)
    r.raise_for_status()
    return r.json()


def verify_consent(consent, expected_id):
    """Verify the consent from hydra raising ConsentError if it fails."""
    if consent['id'] != expected_id:
        raise ConsentError('Consent ids do not match')
    expires_at = parse_datetime(consent['expiresAt'])
    if expires_at < datetime.datetime.now(tz.tzutc()):
        raise ConsentError('Consent request has expired')
    return consent


def retrieve_and_verify_consent(consent_id):
    """Convenience wrapper around retrieve_consent() and verify_consent()."""
    return verify_consent(retrieve_consent(consent_id), consent_id)


def resolve_request(request, consent, decision, grant_scopes=[], reason=None):
    """
    Resolve a consent request and redirect to location in request.

    If *reason* is omitted, it defaults to "request was rejected".
    """
    reason = reason if reason is not None else 'request was rejected'

    if decision not in [Decision.ACCEPT, Decision.REJECT]:
        raise ValueError('Invalid decision: {}'.format(decision))

    redirect_url = consent['redirectUrl']
    consent_id = consent['id']
    subject = ':'.join((settings.SUBJECT_SCHEME, request.user.username))

    if decision is Decision.ACCEPT:
        response = _request(
            method='PATCH', url=settings.HYDRA_CONSENT_REQUESTS_ENDPOINT + consent_id + '/accept',
            json={'subject': subject, 'grantScopes': grant_scopes})
    else:
        response = _request(
            method='PATCH', url=settings.HYDRA_CONSENT_REQUESTS_ENDPOINT + consent_id + '/reject',
            json={'reason': reason})

    response.raise_for_status()

    # We don't use redirect() here because that also accepts a view name and redirect_url is under
    # the control of a third party who may choose something which matches a view name.
    return HttpResponseRedirect(redirect_url)


def _get_session():
    """
    Get a :py:class:`requests.Session` object which is authenticated with the API application's
    OAuth2 client credentials.
    """
    client = BackendApplicationClient(client_id=settings.CONSENT_CLIENT_ID)
    session = OAuth2Session(client=client)
    session.fetch_token(
        timeout=2, token_url=settings.HYDRA_TOKEN_ENDPOINT,
        client_id=settings.CONSENT_CLIENT_ID,
        client_secret=settings.CONSENT_CLIENT_SECRET,
        scope=SCOPES)
    return session


def _request(*args, **kwargs):
    """
    A version of :py:func:`requests.request` which is authenticated with the OAuth2 token for the
    API server's client credentials. If the token has timed out, it is requested again.
    """
    if getattr(_request, '__session', None) is None:
        _request.__session = _get_session()
    try:
        return _request.__session.request(*args, **kwargs)
    except TokenExpiredError:
        _request.__session = _get_session()
        return _request.__session.request(*args, **kwargs)
