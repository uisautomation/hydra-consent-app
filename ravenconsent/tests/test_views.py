import unittest.mock as mock

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse

from ravenconsent import hydra
from ravenconsent.tests import get_valid_consent


class HealthzTests(TestCase):
    def test_healthz(self):
        """GET-ing /healthz succeeds."""
        # We hardcode this URL because its location is part of the external API.
        r = self.client.get('/healthz')
        self.assertEqual(r.status_code, 200)


class ConsentParameterTestMixin:
    """
    A mixin class which contains tests for parsing consent parameters. These should pass
    irrespective of whether a user is logged in.

    """
    def test_no_consent(self):
        """If no consent is passed, an error is reported."""
        # missing consent
        r = self.client.get(self.endpoint)
        self.assertEqual(r.status_code, 400)
        self.assertIn(b'missing_consent', r.content)

    def test_slashes_in_consent(self):
        """A consent which looks like it may try to confuse our URL concatenation is provided
        should fail.

        """
        r = self.client.get(self.endpoint + '?consent=foo%2Fbar')
        self.assertEqual(r.status_code, 400)
        self.assertIn(b'bad_consent', r.content)

    def test_invalid_consent(self):
        """An invalid consent id is not accepted."""
        rav_patch = mock.patch('ravenconsent.hydra.retrieve_and_verify_consent')
        consent = get_valid_consent()

        def fail():
            raise RuntimeError("I don't like your auth")

        with rav_patch as retrieve_and_verify_consent:
            retrieve_and_verify_consent.side_effect = fail
            r = self.client.get(self.endpoint + '?consent=' + consent['id'])
            self.assertEqual(r.status_code, 400)


class NoUserConsentTests(TestCase, ConsentParameterTestMixin):
    """Test consent endpoint with no user logged in."""

    def setUp(self):
        self.endpoint = reverse('consent')

    def test_error(self):
        """Error reporting works even if not logged in."""
        r = self.client.get(self.endpoint + '?error=test_error&error_description=test_description')
        self.assertEqual(r.status_code, 400)  # bad request

        # check that error code and message made it into the rendered response
        self.assertIn(b'test_error', r.content)
        self.assertIn(b'test_description', r.content)

    def test_login_required(self):
        """A valid consent requires login."""
        consent = get_valid_consent()
        rav_patch = mock.patch('ravenconsent.hydra.retrieve_and_verify_consent')
        with rav_patch as retrieve_and_verify_consent:
            retrieve_and_verify_consent.side_effect = lambda _: consent
            r = self.client.get(self.endpoint + '?consent=' + consent['id'])
            self.assertEqual(r.status_code, 302)


class UserConsentTests(TestCase, ConsentParameterTestMixin):
    """Test consent endpoint with a user logged in."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test0001')
        self.client.force_login(self.user)
        self.endpoint = reverse('consent')

    def test_successful_flow(self):
        rav_patch = mock.patch('ravenconsent.hydra.retrieve_and_verify_consent')
        rr_patch = mock.patch('ravenconsent.hydra.resolve_request')
        consent = get_valid_consent()
        with rav_patch as retrieve_and_verify_consent, rr_patch as resolve_request:
            retrieve_and_verify_consent.side_effect = lambda _: consent
            resolve_request.return_value = HttpResponseRedirect('http://test.invalid/')
            r = self.client.get(self.endpoint + '?consent=' + consent['id'])

        # Check redirect was passed
        self.assertEqual(r.status_code, 302)

        # Check call to resolve_request was made
        self.assertEqual(len(resolve_request.mock_calls), 1)

        # Check grants and decision
        args, kwargs = resolve_request.call_args
        self.assertEqual(args[2], hydra.Decision.ACCEPT)
        self.assertEqual(kwargs['grant_scopes'], consent['requestedScopes'])
