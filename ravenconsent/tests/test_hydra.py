"""
Test hydra consent flow implementation.

"""
import datetime
from unittest import mock

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.test.client import RequestFactory
import dateutil.tz as tz

from ravenconsent import hydra
from ravenconsent.tests import get_valid_consent


class HydraRetrieveTests(TestCase):
    def test_retrieve(self):
        """Passing a consent id to retrieve_consent requests the consent from Hydra."""
        with self.settings(HYDRA_CONSENT_REQUESTS_ENDPOINT='http://hydra.invalid/'), \
                mock.patch('ravenconsent.hydra._request') as request:
            request.return_value.json.return_value = 'yyy'
            self.assertEqual(hydra.retrieve_consent('xxx'), 'yyy')

        # Check request called with values
        _, kwargs = request.call_args

        self.assertEqual(kwargs['url'], 'http://hydra.invalid/xxx')
        self.assertEqual(kwargs['method'], 'GET')


class HydraValidationTests(TestCase):
    def test_good_consent_validates(self):
        """A good consent request will validate without throwing."""
        consent = get_valid_consent()
        hydra.verify_consent(consent, consent['id'])

    def test_mismatched_id(self):
        """A consent request with mismatched id should raise ConsentError"""
        consent = get_valid_consent()
        with self.assertRaises(hydra.ConsentError):
            hydra.verify_consent(consent, consent['id'] + '-with-some-junk')

    def test_expired_consent(self):
        """A consent request which has expired should raise ConsentError"""
        consent = get_valid_consent()
        consent['expiresAt'] = (
            datetime.datetime.now(tz.tzutc()) - datetime.timedelta(hours=1)).isoformat()
        with self.assertRaises(hydra.ConsentError):
            hydra.verify_consent(consent, consent['id'])


class HydraResolveTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(username='test0001')
        self.endpoint = reverse('consent')

    def test_resolve_accept(self):
        request = self.factory.get(self.endpoint)
        request.user = self.user

        consent = get_valid_consent()
        with self.settings(HYDRA_CONSENT_REQUESTS_ENDPOINT='http://hydra.invalid/',
                           SUBJECT_SCHEME='test-scheme'), \
                mock.patch('ravenconsent.hydra._request') as hydra_request:
            hydra.resolve_request(request, consent, hydra.Decision.ACCEPT, ['a', 'b'])

        # The return from _request should have been checked for HTTP failure
        hydra_request.return_value.raise_for_status.assert_called_once_with()

        # Check arguments to _request call
        _, kwargs = hydra_request.call_args

        self.assertEqual(kwargs['method'], 'PATCH')
        self.assertEqual(kwargs['url'], 'http://hydra.invalid/' + consent['id'] + '/accept')
        self.assertEqual(kwargs['json'], {
            'subject': 'test-scheme:test0001', 'grantScopes': ['a', 'b']
        })

    def test_resolve_reject(self):
        request = self.factory.get(self.endpoint)
        request.user = self.user

        consent = get_valid_consent()
        with self.settings(HYDRA_CONSENT_REQUESTS_ENDPOINT='http://hydra.invalid/',
                           SUBJECT_SCHEME='test-scheme'), \
                mock.patch('ravenconsent.hydra._request') as hydra_request:
            hydra.resolve_request(request, consent, hydra.Decision.REJECT, ['a', 'b'])

        # The return from _request should have been checked for HTTP failure
        hydra_request.return_value.raise_for_status.assert_called_once_with()

        # Check arguments to _request call
        _, kwargs = hydra_request.call_args

        self.assertEqual(kwargs['method'], 'PATCH')
        self.assertEqual(kwargs['url'], 'http://hydra.invalid/' + consent['id'] + '/reject')
        self.assertIn('reason', kwargs['json'])

    def test_validate_decision(self):
        """Passing an invalid value for decision raises ValueError."""

        request = self.factory.get(self.endpoint)
        request.user = self.user

        consent = get_valid_consent()
        with self.settings(HYDRA_CONSENT_REQUESTS_ENDPOINT='http://hydra.invalid/',
                           SUBJECT_SCHEME='test-scheme'), \
                mock.patch('ravenconsent.hydra._request'), self.assertRaises(ValueError):
            hydra.resolve_request(request, consent, 'accept', ['a', 'b'])
