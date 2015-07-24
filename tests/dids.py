import os
import sys
sys.path.append(os.path.dirname(__file__) + '/..')

from fcc4d.exceptions import (
    ApiNotFoundException,
    ApiPermissionException,
)
from fcc4d.resources import (
    Did,
)

from base import FCC4DUserTestCase


class DidsTest(FCC4DUserTestCase):
    TEST_FILTER = "npa eq 518"

    def _get_did(self):
        o = self.c.dids.get(self.user_did_sid)
        self.assertIsInstance(o, Did)
        self.assertEqual(o.didSid, self.user_did_sid)
        return o

    def test_inventory_list_filter(self):
        rs = self.c.dids_inventory.list(filter=self.TEST_FILTER, limit=5)
        self.assertEqual(len(rs), 5)
        self.assertIsInstance(rs[0], Did)

    def test_create_and_delete(self):
        rs = self.c.dids_inventory.list(filter=self.TEST_FILTER, limit=1)
        wanted = rs[0]
        self.assertIsInstance(wanted, Did)

        created = self.c.dids.create(instance=wanted)
        self.assertIsInstance(created, Did)
        self.assertEqual(wanted.phonenumber, created.phonenumber)

        rs = self.c.dids.list()
        self.assertTrue(any([x.phonenumber == wanted.phonenumber for x in rs]))

        o = self.c.dids.get(created.didSid)
        self.assertIsInstance(o, Did)
        self.assertEqual(o.phonenumber, created.phonenumber)

        o.delete()
        _fail = lambda: self.c.dids.get(created.didSid)
        self.assertRaises(ApiNotFoundException, _fail)

    def test_update(self):
        o = self._get_did()

        o.update(trunkSid=self.user_trunk_sid)
        o = self._get_did()
        self.assertEqual(o.trunkSid, self.user_trunk_sid)

        o.update(trunkSid=self.user_trunk2_sid)
        o = self._get_did()
        self.assertEqual(o.trunkSid, self.user_trunk2_sid)

    def test_update_other(self):
        o = self._get_did()
        o.didSid = self.other_did_sid
        _fail = lambda: o.update(trunkSid=self.user_trunk_sid)
        self.assertRaises(ApiPermissionException, _fail)

    def test_delete_other(self):
        o = self._get_did()
        o.didSid = self.other_did_sid
        _fail = lambda: o.delete()
        self.assertRaises(ApiPermissionException, _fail)

    def test_get(self):
        o = self._get_did()
        self.assertIsInstance(o, Did)
        self.assertEqual(o.didSid, self.user_did_sid)

    def test_list_all(self):
        wanted = self._get_did()

        rs = self.c.dids.list()
        self.assertGreaterEqual(len(rs), 1)
        self.assertTrue(all([isinstance(x, Did) for x in rs]))
        self.assertTrue(any([repr(x) == repr(wanted) for x in rs]))

    def test_list_filter(self):
        wanted = self._get_did()

        rs = self.c.dids.list(filter='didSid eq "{0}"'.format(self.user_did_sid))
        self.assertEqual(len(rs), 1)
        self.assertIsInstance(rs[0], Did)
        self.assertEqual(repr(rs[0]), repr(wanted))

    def test_list_filter_other(self):
        rs = self.c.dids.list(filter='didSid eq "{0}"'.format(self.other_did_sid))
        self.assertEqual(len(rs), 0)
