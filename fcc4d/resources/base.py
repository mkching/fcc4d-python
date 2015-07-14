import json
import requests

from fcc4d.exceptions import (
    ApiPermissionException,
    ApiServerError,
    ApiValueError,
)
from fcc4d.base.rest_client import RestClient


class ItemResource(RestClient):
    def __init__(self, connection, data=None):
        super().__init__(connection)
        if data:
            for k in self.retrieve_fields:
                setattr(self, k, data[k])

    def __str__(self):
        fields = ['{0}={1!r}'.format(x, getattr(self, x)) for x in self.fields if getattr(self, x, None)]
        buf = '{0}({1})'.format(self.__class__.__name__, ", ".join(fields))
        return buf

    @classmethod
    def from_dict(cls, data):
        o = cls(None)
        for k in cls.fields:
            setattr(o, k, data.get(k))
        return o

    def to_json(self):
        data = {}
        for k in self.fields:
            v = getattr(self, k, None)
            if v:
                data[k] = v
        return json.dumps(data)

    def update(self, **data):
        url = '{0}/{1}/{2}'.format(self.connection.base_url, self.endpoint_path, getattr(self, self.sid_field))

        for k in data.keys():
            if k not in self.update_fields:
                raise ApiValueError("Field {0} not allowed in update, must be in {1}".format(k, self.update_fields))

        r = requests.patch(
            url=url,
            auth=self.connection.auth,
            headers=self.connection.headers,
            data=json.dumps(data),
        )
        if r.status_code == 403:
            raise ApiPermissionException()
        elif r.status_code != 200:
            raise ApiServerError("Unexpected response from server: {0}: {1}".format(r.status_code, r.content))

        return r.content.decode()

    def delete(self):
        url = '{0}/{1}/{2}'.format(self.connection.base_url, self.endpoint_path, getattr(self, self.sid_field))

        r = requests.delete(
            url=url,
            auth=self.connection.auth,
            headers=self.connection.headers,
        )
        if r.status_code == 403:
            raise ApiPermissionException()
        if r.status_code != 200:
            raise ApiServerError("Unexpected response from server: {0}: {1}".format(r.status_code, r.content))

        return r.content.decode()


class ListResource(RestClient):
    LIST_LIMIT = 999999

    def create(self, **data):
        url = '{0}/{1}'.format(self.connection.base_url, self.endpoint_path)

        for k in data.keys():
            if k not in self.item_resource.create_fields:
                raise ApiValueError("Field {0} not allowed in create, must be in {1}".format(
                    k, self.item_resource.create_fields))

        instance = self.item_resource.from_dict(data)

        r = requests.post(
            url=url,
            auth=self.connection.auth,
            headers=self.connection.headers,
            data=instance.to_json(),
        )
        if r.status_code == 403:
            raise ApiPermissionException()
        elif r.status_code != 200:
            raise ApiServerError("Unexpected response from server: {0}: {1}".format(r.status_code, r.content))

        return r.content.decode()

    def get(self, sid):
        url = '{0}/{1}/{2}'.format(self.connection.base_url, self.endpoint_path, sid)

        r = requests.get(
            url=url,
            auth=self.connection.auth,
            headers=self.connection.headers,
        )
        if r.status_code == 403:
            raise ApiPermissionException()
        elif r.status_code != 200:
            raise ApiServerError("Unexpected response from server")

        try:
            data = json.loads(r.content.decode())
        except ValueError:
            raise ApiServerError("Unparseable response from server: {0}: {1}".format(r.status_code, r.content))
        else:
            return self.item_resource(self.connection, data)

    def list(self, filter=None):
        url = '{0}/{1}'.format(self.connection.base_url, self.endpoint_path)

        r = requests.get(
            url=url,
            auth=self.connection.auth,
            headers=self.connection.headers,
            params={
                'limit': self.LIST_LIMIT,
                'filter': filter,
            },
        )
        if r.status_code == 403:
            raise ApiPermissionException()
        elif r.status_code != 200:
            raise ApiServerError("Unexpected response from server")

        try:
            data = json.loads(r.content.decode())["items"]
        except ValueError:
            raise ApiServerError("Unparseable response from server: {0}: {1}".format(r.status_code, r.content))
        else:
            return [self.item_resource(self.connection, x) for x in data]
