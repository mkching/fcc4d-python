import os
import sys
sys.path.append(os.path.dirname(__file__) + '/..')

import requests
import uuid

from fcc4d.resources import (
    Account,
)

from base import FCC4DAdminTestCase


class AccountsTest(FCC4DAdminTestCase):
    def setUp(self):
        super().setUp()

        for o in self.c.accounts.list(filter='login like "wv-unittest%"'):
            if o.login.startswith("wv-unittest"):
                o.delete()

    def _create_account(self, username, password, name=None):
        return self.c.accounts.create(
            login=username,
            password=password,
            name=name,
            role=1,
        )

    def _auth_check(self, login, password, status_code=200):
        url = '{0}/{1}'.format(self.c.connection.base_url, 'accounts')
        r = requests.get(url, auth=(login, password))
        self.assertEqual(r.status_code, status_code)

    def test_create(self):
        username = 'wv-unittest1'
        password = uuid.uuid4().hex

        a = self._create_account(
            username,
            password,
        )
        self._auth_check(username, password)
        self.assertEqual(a.login, username)

    def test_update(self):
        username = 'wv-unittest1'
        password = uuid.uuid4().hex
        password2 = uuid.uuid4().hex

        a = self._create_account(
            username,
            password,
        )
        self._auth_check(username, password)

        a.update(
            password=password2,
        )
        self._auth_check(username, password, 401)
        self._auth_check(username, password2)

    def test_delete(self):
        username = 'wv-unittest1'
        password = uuid.uuid4().hex

        a = self._create_account(
            username,
            password,
        )
        self._auth_check(username, password)

        a.delete()
        self._auth_check(username, password, 401)

        rs = self.c.accounts.list(filter='login eq "{0}"'.format(username))
        self.assertEqual(len(rs), 0)

    def test_get(self):
        username = 'wv-unittest1'
        password = uuid.uuid4().hex

        a1 = self._create_account(
            username,
            password,
        )

        a = self.c.accounts.get(a1.accountSid)
        self.assertEqual(repr(a1), repr(a))

    def test_list_all(self):
        username1 = 'wv-unittest1'
        password1 = uuid.uuid4().hex
        username2 = 'wv-unittest2'
        password2 = uuid.uuid4().hex

        self._create_account(
            username1,
            password1,
        )
        self._create_account(
            username2,
            password2,
        )

        rs = self.c.accounts.list()
        self.assertGreaterEqual(len(rs), 2)

        for a in rs:
            self.assertIsInstance(a, Account)

    def test_list_filter(self):
        username1 = 'wv-unittest1'
        password1 = uuid.uuid4().hex
        name1 = uuid.uuid4().hex
        username2 = 'wv-unittest2'
        password2 = uuid.uuid4().hex

        self._create_account(
            username1,
            password1,
            name1,
        )
        self._create_account(
            username2,
            password2,
        )

        rs = self.c.accounts.list(filter='login eq "{0}"'.format(username1))
        self.assertEqual(len(rs), 1)

        for a in rs:
            self.assertIsInstance(a, Account)
            self.assertEqual(a.login, username1)
            self.assertEqual(a.name, name1)
