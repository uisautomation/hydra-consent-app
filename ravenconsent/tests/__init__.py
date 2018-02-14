import datetime
import dateutil.tz as tz


def get_valid_consent():
    return {
        'id': 'test-consent',
        'expiresAt': (datetime.datetime.now(tz.tzutc()) + datetime.timedelta(hours=1)).isoformat(),
        'clientId': 'test-client',
        'redirectUrl': 'http://invalid.invalid/',
        'requestedScopes': ['a', 'b']
    }
