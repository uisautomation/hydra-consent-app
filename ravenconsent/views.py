from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from . import hydra


def healthz(request):
    """Lightweight "readiness" endpoint used to determine when the service is "up"."""
    return JsonResponse({'status': 'ok'})


def consent(request):
    """Handle consent flow from hydra."""
    # If error is passed as GET parameter, report it
    if 'error' in request.GET:
        return render_error_from_request(request)

    # Get consent from request
    unverified_consent_id = request.GET.get('consent')

    # If not present, report error
    if unverified_consent_id is None:
        return render_error(request, 'missing_consent', 'No consent id was provided')

    # If consent looks strange, early out. Recall that the consent id is user-controlled and can be
    # presented directly to the consent app. Later on we use it to build the URL to retrieve the
    # consent request and the accept/reject URL. In all cases the consent id forms part of the URL
    # path. To avoid the chance of an attacker managing to get the consent app to fetch an
    # unexpected URL, disallow slashes in the provided consent id. Otherwise a user could cause the
    # consent app to fetch arbitrary URLs on the hydra app by, e.g., specifying a consent id of
    # "../../some/other/path" or similar.
    if '/' in unverified_consent_id:
        return render_error(request, 'bad_consent', 'A bad consent id was provided')

    # Retrieve and verify the consent
    try:
        consent = hydra.retrieve_and_verify_consent(unverified_consent_id)
    except Exception as e:
        return render_error(request, 'cannot_verify_consent', str(e))

    # With CONSENT_PROMPT_NONE_SCOPE, instead of redirecting to the account login page, simply
    # reject the request out of hand if the current user is not authenticated.
    requested_scopes = consent.get('requestedScopes', [])
    if (settings.CONSENT_PROMPT_NONE_SCOPE in requested_scopes
            and not request.user.is_authenticated):
        return _reject_request(request, consent, 'user not logged in')

    # Otherwise, delegate response to a view which requires login
    return _consent_requiring_login(request, consent)


@login_required
def _consent_requiring_login(request, consent):
    """Handle parts of the consent flow which require a user be logged in."""
    # For the moment we implicitly grant all requested scopes with no further verification or user
    # input. This goes against the grain of OAuth2 in general but, for the moment, the fact we are
    # running an OAuth2 server is an implementation detail and we'd like to preserve a traditional
    # Raven login flow.
    #
    # Should the use of this service become more widespread, we should re-visit this. We shall also
    # need to re-visit this before Hydra v1 since Hydra will start enforcing some sort of scope
    # grant flow. See https://github.com/ory/hydra/issues/772.
    return _grant_request(request, consent)


def _grant_request(request, consent):
    """
    Helper function to unconditionally grant a consent request and all the scopes.

    :returns: redirect back to Hydra server
    :rtype: django.http.response.Response
    """
    return hydra.resolve_request(
        request, consent, hydra.Decision.ACCEPT, grant_scopes=consent['requestedScopes'])


def _reject_request(request, consent, reason):
    """
    Helper function to unconditionally reject a consent request.

    :returns: redirect back to Hydra server
    :rtype: django.http.response.Response
    """
    return hydra.resolve_request(request, consent, hydra.Decision.REJECT, reason=reason)


def render_error_from_request(request):
    """Render error page based on error request."""
    return render(request, 'ravenconsent/error.html', status=400, context={
        'error': request.GET.get('error'),
        'error_description': request.GET.get('error_description'),
    })


def render_error(request, error, error_description):
    """Render error page based on error request."""
    return render(request, 'ravenconsent/error.html', status=400, context={
        'error': error, 'error_description': error_description})
