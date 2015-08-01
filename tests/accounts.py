import os
import sys
sys.path.append(os.path.dirname(__file__) + '/..')

import uuid

from fcc4d.exceptions import (
    ApiPermissionException,
)
from fcc4d.resources import (
    Account,
)

from base import FCC4DUserTestCase


class AccountsTest(FCC4DUserTestCase):
    def _get_account(self):
        a = self.c.accounts.get(self.user_account_sid)
        self.assertIsInstance(a, Account)
        self.assertEqual(a.accountSid, self.user_account_sid)
        return a

    def _test_create(self):
        self.c.accounts.create(
            login='wv-unittest1',
            password='DVVsJCzoiEf5',
            role=1
        )

    def test_create(self):
        self.assertRaises(ApiPermissionException, self._test_create)

    def test_update(self):
        value = uuid.uuid4().hex

        a = self._get_account()
        self.assertNotEqual(a.name, value)

        a.update(name=value)

        a = self._get_account()
        self.assertEqual(a.name, value)

    def _test_update_other(self):
        value = uuid.uuid4().hex

        a = self._get_account()
        self.assertNotEqual(a.name, value)

        a.accountSid = self.other_account_sid
        a.update(name=value)

        a = self._get_account()
        self.assertNotEqual(a.name, value)

    def test_update_other(self):
        self.assertRaises(ApiPermissionException, self._test_update_other)

    def test_delete(self):
        pass

    def _test_delete_other(self):
        a = self._get_account()

        a.accountSid = self.other_account_sid
        a.delete()

    def test_delete_other(self):
        self.assertRaises(ApiPermissionException, self._test_delete_other)

    def test_get(self):
        a = self._get_account()
        self.assertIsInstance(a, Account)
        self.assertEqual(a.accountSid, self.user_account_sid)

    def test_exists(self):
        self.assertTrue(self.c.accounts.exists(filter='accountSid eq "{0}"'.format(self.user_account_sid)))
        self.assertFalse(self.c.accounts.exists(filter='accountSid eq "{0}"'.format(self.other_account_sid)))

    def test_list_all(self):
        wanted = self._get_account()

        rs = self.c.accounts.list()
        self.assertEqual(len(rs), 1)
        self.assertIsInstance(rs[0], Account)
        self.assertEqual(repr(rs[0]), repr(wanted))

    def test_list_filter(self):
        wanted = self._get_account()

        rs = self.c.accounts.list(filter='accountSid eq "{0}"'.format(self.user_account_sid))
        self.assertEqual(len(rs), 1)
        self.assertIsInstance(rs[0], Account)
        self.assertEqual(repr(rs[0]), repr(wanted))

    def test_list_filter_other(self):
        rs = self.c.accounts.list(filter='accountSid eq "{0}"'.format(self.other_account_sid))
        self.assertEqual(len(rs), 0)
