import os
import sys
sys.path.append(os.path.dirname(__file__) + '/..')

import uuid

from fcc4d.exceptions import (
    ApiNotFoundException,
    ApiPermissionException,
)
from fcc4d.resources import (
    Trunkgroup,
)

from base import FCC4DUserTestCase


class TrunkgroupTest(FCC4DUserTestCase):
    def setUp(self):
        super().setUp()

        for o in self.c.trunkgroups.list(filter='name eq "unittest test trunkgroup"'):
            if o.name == "unittest test trunkgroup":
                o.delete()

    def _get_trunkgroup(self):
        o = self.c.trunkgroups.get(self.user_trunkgroup_sid)
        self.assertIsInstance(o, Trunkgroup)
        self.assertEqual(o.trunkGroupSid, self.user_trunkgroup_sid)
        return o

    def test_create(self):
        result = self.c.trunkgroups.create(
            name="unittest test trunkgroup",
            typeId=Trunkgroup.TYPE_FAILOVER,
        )
        verify = self.c.trunkgroups.get(result.trunkGroupSid)
        self.assertEqual(repr(result), repr(verify))

    def test_update(self):
        value = uuid.uuid4().hex

        o = self._get_trunkgroup()
        self.assertNotEqual(o.name, value)

        o.update(name=value, typeId=Trunkgroup.TYPE_FAILOVER)
        o = self._get_trunkgroup()
        self.assertEqual(o.name, value)
        self.assertEqual(o.typeId, Trunkgroup.TYPE_FAILOVER)

        o.update(typeId=Trunkgroup.TYPE_LOADBALANCE)
        o = self._get_trunkgroup()
        self.assertEqual(o.name, value)
        self.assertEqual(o.typeId, Trunkgroup.TYPE_LOADBALANCE)

    def _test_update_other(self):
        o = self._get_trunkgroup()
        o.trunkGroupSid = self.other_trunkgroup_sid
        o.update(typeId=Trunkgroup.TYPE_FAILOVER)

    def test_update_other(self):
        self.assertRaises(ApiPermissionException, self._test_update_other)

    def test_delete(self):
        created = self.c.trunkgroups.create(
            name="unittest test trunkgroup",
            typeId=Trunkgroup.TYPE_FAILOVER,
        )
        verify = self.c.trunkgroups.get(created.trunkGroupSid)
        self.assertEqual(repr(created), repr(verify))

        created.delete()
        _fail = lambda: self.c.trunkgroups.get(created.trunkGroupSid)
        self.assertRaises(ApiNotFoundException, _fail)

    def test_delete_other(self):
        o = self._get_trunkgroup()
        o.trunkGroupSid = self.other_trunkgroup_sid
        _fail = lambda: o.delete()
        self.assertRaises(ApiPermissionException, _fail)

    def test_get(self):
        o = self._get_trunkgroup()
        self.assertIsInstance(o, Trunkgroup)
        self.assertEqual(o.trunkGroupSid, self.user_trunkgroup_sid)

    def test_list_all(self):
        wanted = self._get_trunkgroup()

        rs = self.c.trunkgroups.list()
        self.assertGreaterEqual(len(rs), 1)
        self.assertIsInstance(rs[0], Trunkgroup)
        self.assertEqual(repr(rs[0]), repr(wanted))

    def test_list_filter(self):
        wanted = self._get_trunkgroup()

        rs = self.c.trunkgroups.list(filter='trunkGroupSid eq "{0}"'.format(self.user_trunkgroup_sid))
        self.assertEqual(len(rs), 1)
        self.assertIsInstance(rs[0], Trunkgroup)
        self.assertEqual(repr(rs[0]), repr(wanted))

    def test_list_filter_other(self):
        rs = self.c.trunkgroups.list(filter='trunkGroupSid eq "{0}"'.format(self.other_trunkgroup_sid))
        self.assertEqual(len(rs), 0)
