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
        self.c = FCC4DClient(
            username=config['admin_username'],
            password=config['admin_password'],
            base_url=config['endpoint_url'],
        )


class FCC4DUserTestCase(unittest.TestCase):
    # represents the sid of the test user
    user_account_sid = config['user_account_sid']
    # another valid sid in the system, but that the test user has no access to
    other_account_sid = config['other_account_sid']

    def setUp(self):
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
