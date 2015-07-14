import os
import sys
sys.path.append(os.path.dirname(__file__) + '/..')

from fcc4d.resources import (
    Account,
)

from base import FCC4DAdminTestCase


class AccountsTest(FCC4DAdminTestCase):
    def _create_account1(self):
        return self.c.accounts.create(
            login='wv-unittest1',
            password='DVVsJCzoiEf5',
            role=1
        )

    def _create_account2(self):
        return self.c.accounts.create(
            login='wv-unittest2',
            password='TMb9Ywi4sO8o',
            role=1
        )

    def test_create(self):
        a = self._create_account1()
        print(a)

    def test_update(self):
        a = self._create_account1()

        # a.update(
        #     password='9goZ1aB6VuHl',
        # )
        print(a)

    def test_delete(self):
        a = self._create_account1()

        # a.delete()
        print(a)

    def test_get(self):
        a1 = self._create_account1()

        a = self.c.accounts.get(a1.accountSid)
        self.assertEqual(repr(a1), repr(a))

    def test_list_all(self):
        a1 = self._create_account1()
        a2 = self._create_account2()

        rs = self.c.accounts.list()
        self.assertGreaterEqual(len(rs), 2)

        for a in rs:
            self.assertIsInstance(a, Account)

    def test_list_filter(self):
        a1 = self._create_account1()
        a2 = self._create_account2()

        rs = self.c.accounts.list(filter='login eq "wv-unittest1"')
        self.assertEqual(len(rs), 1)

        for a in rs:
            self.assertIsInstance(a, Account)
            self.assertEqual(a.login, 'wv-unittest1')
            self.assertEqual(a.name, 'Unit Test 1')
