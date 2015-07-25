import os
import sys
sys.path.append(os.path.dirname(__file__) + '/..')

import uuid

from fcc4d.exceptions import (
    ApiNotFoundException,
    ApiPermissionException,
    ApiValueError,
)
from fcc4d.resources import (
    Endpoint,
)

from base import FCC4DUserTestCase


class EndpointTest(FCC4DUserTestCase):
    def setUp(self):
        super().setUp()

        for o in self.c.endpoints.list(filter='name eq "unittest test endpoint"'):
            if o.name == "unittest test endpoint":
                o.delete()

    def _get_endpoint(self):
        o = self.c.endpoints.get(self.user_endpoint_sid)
        self.assertIsInstance(o, Endpoint)
        self.assertEqual(o.endpointSid, self.user_endpoint_sid)
        return o

    def test_create_bad(self):
        # this request caused an error condition during development
        # keep this test to watch for regressions

        args = {
            'name': "unittest test endpoint",
            'typeId': Endpoint.TYPE_OTHER,
            'addresses': [{"tag": "unittest test endpoint tag", "ip": "10.250.250.250:5061"}],
        }
        _fail = lambda: self.c.endpoints.create(**args)
        self.assertRaises(ApiValueError, _fail)

    def test_create(self):
        result = self.c.endpoints.create(
            name="unittest test endpoint",
            typeId=Endpoint.TYPE_OTHER,
            addresses=[{"tag": "unittest test endpoint tag", "ip": "10.250.250.250"}],
        )
        verify = self.c.endpoints.get(result.endpointSid)
        self.assertEqual(repr(result), repr(verify))

        result = self.c.endpoints.create(
            name="unittest test endpoint",
            typeId=Endpoint.TYPE_OTHER,
            addresses=[{"tag": "unittest test endpoint tag", "ip": "10.251.251.251", "port": "5061"}],
        )
        verify = self.c.endpoints.get(result.endpointSid)
        self.assertEqual(repr(result), repr(verify))

    def test_update(self):
        value = uuid.uuid4().hex

        o = self._get_endpoint()
        self.assertNotEqual(o.name, value)

        o.update(name=value, typeId=Endpoint.TYPE_OTHER)
        o = self._get_endpoint()
        self.assertEqual(o.name, value)
        self.assertEqual(o.typeId, Endpoint.TYPE_OTHER)

        o.update(typeId=Endpoint.TYPE_LYNC)
        o = self._get_endpoint()
        self.assertEqual(o.name, value)
        self.assertEqual(o.typeId, Endpoint.TYPE_LYNC)

    def test_update_other(self):
        o = self._get_endpoint()
        o.endpointSid = self.other_endpoint_sid
        _fail = lambda: o.update(typeId=Endpoint.TYPE_LYNC)

        self.assertRaises(ApiPermissionException, _fail)

    def test_delete(self):
        created = self.c.endpoints.create(
            name="unittest test endpoint",
            typeId=Endpoint.TYPE_OTHER,
            addresses=[{"tag": "unittest test endpoint tag", "ip": "10.254.254.254"}],
        )
        verify = self.c.endpoints.get(created.endpointSid)
        self.assertEqual(repr(created), repr(verify))

        created.delete()
        _fail = lambda: self.c.endpoints.get(created.endpointSid)
        self.assertRaises(ApiNotFoundException, _fail)

    def test_delete_other(self):
        o = self._get_endpoint()
        o.endpointSid = self.other_endpoint_sid
        _fail = lambda: o.delete()
        self.assertRaises(ApiPermissionException, _fail)

    def test_get(self):
        o = self._get_endpoint()
        self.assertIsInstance(o, Endpoint)
        self.assertEqual(o.endpointSid, self.user_endpoint_sid)

    def test_list_all(self):
        wanted = self._get_endpoint()

        rs = self.c.endpoints.list()
        self.assertGreaterEqual(len(rs), 1)
        self.assertIsInstance(rs[0], Endpoint)
        self.assertEqual(repr(rs[0]), repr(wanted))

    def test_list_filter(self):
        wanted = self._get_endpoint()

        rs = self.c.endpoints.list(filter='endpointSid eq "{0}"'.format(self.user_endpoint_sid))
        self.assertEqual(len(rs), 1)
        self.assertIsInstance(rs[0], Endpoint)
        self.assertEqual(repr(rs[0]), repr(wanted))

    def test_list_filter_other(self):
        rs = self.c.endpoints.list(filter='endpointSid eq "{0}"'.format(self.other_endpoint_sid))
        self.assertEqual(len(rs), 0)

    def test_getattr(self):
        o = Endpoint.from_dict({
            'addresses': [],
            'attributes': [
                {
                    'key': 'test1',
                    'value': 'test2',
                },
                {
                    'key': 'test3',
                    'value': 'test4',
                },
            ]
        })
        self.assertEqual(o.getattr('test1'), 'test2')
        self.assertEqual(o.getattr('test3'), 'test4')
        self.assertEqual(o.getattr('none'), None)
        self.assertEqual(o.getattr('none', 'test5'), 'test5')
                    
