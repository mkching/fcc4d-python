import os
import sys
sys.path.append(os.path.dirname(__file__) + '/..')

import json
import unittest

from fcc4d.client import FCC4DClient

import requests
import http.client as http_client
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

config_filename = os.path.dirname(__file__) + '/config.json'
with open(config_filename) as data_file:
    config = json.load(data_file)


class FCC4DAdminTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.c = FCC4DClient(
            username=config['admin_username'],
            password=config['admin_password'],
            base_url=config['endpoint_url'],
        )


class FCC4DUserTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

        # test class expects to be configured with an account that has an object of each of the api endpoints
        # there should also be valid sid for resources which it does have have access to
        for k in ('account', 'did', 'endpoint', 'trunk', 'trunk2', 'trunkgroup'):
            setattr(self, 'user_{0}_sid'.format(k), config['user_{0}_sid'.format(k)])
            setattr(self, 'other_{0}_sid'.format(k), config['other_{0}_sid'.format(k)])

        self.c = FCC4DClient(
            username=config['user_username'],
            password=config['user_password'],
            base_url=config['endpoint_url'],
        )

        self.c = FCC4DClient(
            username=config['user_username'],
            password=config['user_password'],
            base_url=config['endpoint_url'],
        )
