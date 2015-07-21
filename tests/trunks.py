import os
import sys
sys.path.append(os.path.dirname(__file__) + '/..')

import uuid

from fcc4d.exceptions import (
    ApiNotFoundException,
    ApiPermissionException,
)
from fcc4d.resources import (
    Trunk,
)

from base import FCC4DUserTestCase


class TrunkTest(FCC4DUserTestCase):
    def setUp(self):
        super().setUp()

        for o in self.c.trunks.list(filter='name eq "unittest test trunk"'):
            if o.name == "unittest test trunk":
                o.delete()

    def _get_trunk(self):
        o = self.c.trunks.get(self.user_trunk_sid)
        self.assertIsInstance(o, Trunk)
        self.assertEqual(o.trunkSid, self.user_trunk_sid)
        return o

    def test_create(self):
        result = self.c.trunks.create(
            name="unittest test trunk",
            endpointSid=self.user_endpoint_sid,
        )
        verify = self.c.trunks.get(result.trunkSid)
        self.assertEqual(repr(result), repr(verify))

    def test_update(self):
        value = uuid.uuid4().hex

        o = self._get_trunk()
        self.assertNotEqual(o.name, value)

        o.update(name=value, protocolId=Trunk.PROTOCOL_UDP)
        o = self._get_trunk()
        self.assertEqual(o.name, value)
        self.assertEqual(o.protocolId, Trunk.PROTOCOL_UDP)

        o.update(protocolId=Trunk.PROTOCOL_TCP)
        o = self._get_trunk()
        self.assertEqual(o.name, value)
        self.assertEqual(o.protocolId, Trunk.PROTOCOL_TCP)

    def test_update_other(self):
        o = self._get_trunk()
        o.trunkSid = self.other_trunk_sid
        _fail = lambda: o.update(protocolId=Trunk.PROTOCOL_TCP)

        self.assertRaises(ApiPermissionException, _fail)

    def test_delete(self):
        created = self.c.trunks.create(
            name="unittest test trunk",
            endpointSid=self.user_endpoint_sid,
        )
        verify = self.c.trunks.get(created.trunkSid)
        self.assertEqual(repr(created), repr(verify))

        created.delete()
        _fail = lambda: self.c.trunks.get(created.trunkSid)
        self.assertRaises(ApiNotFoundException, _fail)

    def test_delete_other(self):
        o = self._get_trunk()
        o.trunkSid = self.other_trunk_sid
        _fail = lambda: o.delete()
        self.assertRaises(ApiPermissionException, _fail)

    def test_get(self):
        o = self._get_trunk()
        self.assertIsInstance(o, Trunk)
        self.assertEqual(o.trunkSid, self.user_trunk_sid)

    def test_list_all(self):
        wanted = self._get_trunk()

        rs = self.c.trunks.list()
        self.assertGreaterEqual(len(rs), 1)
        self.assertIsInstance(rs[0], Trunk)
        self.assertEqual(repr(rs[0]), repr(wanted))

    def test_list_filter(self):
        wanted = self._get_trunk()

        rs = self.c.trunks.list(filter='trunkSid eq "{0}"'.format(self.user_trunk_sid))
        self.assertEqual(len(rs), 1)
        self.assertIsInstance(rs[0], Trunk)
        self.assertEqual(repr(rs[0]), repr(wanted))

    def test_list_filter_other(self):
        rs = self.c.trunks.list(filter='trunkSid eq "{0}"'.format(self.other_trunkgroup_sid))
        self.assertEqual(len(rs), 0)
