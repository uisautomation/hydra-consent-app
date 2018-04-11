import datetime
import dateutil.tz as tz


def get_valid_consent(scopes=None):
    scopes = scopes if scopes is not None else ['a', 'b']
    return {
        'id': 'test-consent',
        'expiresAt': (datetime.datetime.now(tz.tzutc()) + datetime.timedelta(hours=1)).isoformat(),
        'clientId': 'test-client',
        'redirectUrl': 'http://invalid.invalid/',
        'requestedScopes': scopes,
    }
