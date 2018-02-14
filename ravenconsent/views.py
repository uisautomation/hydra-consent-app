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

    # Otherwise, delegate response to a view which requires login
    return _consent_requiring_login(request)


@login_required
def _consent_requiring_login(request):
    """Handle parts of the consent flow which require a user be logged in."""
    # Get consent from request
    unverified_consent_id = request.GET.get('consent')

    # If not present, report error
    if unverified_consent_id is None:
        return render_error(request, 'missing_consent', 'No consent id was provided')

    # If consent looks strange, early out
    if '/' in unverified_consent_id:
        return render_error(request, 'bad_consent', 'A bad consent id was provided')

    # Retrieve and verify the consent
    try:
        consent = hydra.retrieve_and_verify_consent(unverified_consent_id)
    except Exception as e:
        return render_error(request, 'cannot_verify_consent', str(e))

    # Implicitly grant it
    return hydra.resolve_request(
        request, consent, hydra.Decision.ACCEPT, grant_scopes=consent['requestedScopes'])


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
