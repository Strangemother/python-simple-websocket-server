import unittest
from unittest import mock

import factory

port = 8004
ip = '127.0.0.1'


class TestServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name(self):
        name = 'dave'
        expected = "Strangemother/BroadcastServerFactory::{}/0.01".format(name)
        url = 'ws://localhost:10919'
        fact = factory.BroadcastServerFactory(url, server=name)
        assert fact.server == expected

