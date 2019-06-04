import unittest
from unittest import mock

import authenticator as au


class TestAuthenticator(unittest.TestCase):

    def test_gen_16(self):
        """gen_auth_string must return an expecteds formatted string"""
        name = 'foo'
        secret = 'random_string'
        res = au.gen_auth_string(name, secret)
        template = "otpauth://totp/{}?secret={}".format(name, secret)
        assert res == template

    @mock.patch('authenticator.gen_16', return_value='egg')
    def test_gen_16_None(self, gen_16=None):
        """gen_auth_string must return a correctly formatted string with no args"""
        res = au.gen_auth_string(None, None)

        template = "otpauth://totp/authenticator?secret=egg"
        assert res == template, f"Failure for {res}"

    @mock.patch('authenticator.otp.get_totp', return_value='egg')
    def test_gen_time_token(self, get_totp):
        """Ensure the get_totp function is called with the correct args."""
        secret = 'banana'
        res = au.gen_time_token(secret)
        get_totp.assert_called_with(secret)
        assert res == 'egg'

    @mock.patch('authenticator.otp.valid_totp', return_value='sploge')
    def test_validate_time_auth(self, validate_time_auth):
        """Ensure the get_totp function is called with the correct args."""
        secret = 'banana'
        token = 'orange'
        res = au.validate_time_auth(token, secret)

        validate_time_auth.assert_called_with(token=token, secret=secret)
        assert res == 'sploge'

    @mock.patch('pyqrcode.create', return_value='URLO')
    def test_validate_time_auth(self, create):
        """Ensure the get_totp function is called with the correct args."""
        secret = 'banana'
        name = 'fred'
        url = au.create_qr(secret, name)
        #text = url.text(quiet_zone=1)

        create.assert_called_with('otpauth://totp/fred?secret=banana')
        assert 'URLO' == url, url
