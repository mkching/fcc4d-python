import json
import logging
import requests

from fcc4d.exceptions import (
    ApiNotFoundException,
    ApiPermissionException,
    ApiServerError,
    ApiValueError,
)
from fcc4d.base.rest_client import RestClient


logger = logging.getLogger()


def _validate_status_code(r):
    if r.status_code == 200:
        return
    elif r.status_code == 403:
        raise ApiPermissionException()
    elif r.status_code == 404:
        raise ApiNotFoundException()
    elif r.status_code == 400:
        try:
            errors = json.loads(r.content.decode())['errors']
            raise ApiValueError(errors)
        except (ValueError, KeyError):
            # fall through to default error if error response cannot be parsed
            pass

    raise ApiServerError("Unexpected response from server: {0}: {1}".format(r.status_code, r.content))


class ItemResource(RestClient):
    def __init__(self, connection, data=None):
        super().__init__(connection)
        if data:
            for k in self.fields:
                setattr(self, k, data.get(k))

    def __str__(self):
        fields = ['{0}={1!r}'.format(x, getattr(self, x)) for x in self.fields if getattr(self, x, None) is not None]
        buf = '{0}({1})'.format(self.__class__.__name__, ", ".join(fields))
        return buf

    def __repr__(self):
        return str(self)

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
            if v is not None:
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
        _validate_status_code(r)

        return r.content.decode()

    def delete(self):
        url = '{0}/{1}/{2}'.format(self.connection.base_url, self.endpoint_path, getattr(self, self.sid_field))

        r = requests.delete(
            url=url,
            auth=self.connection.auth,
            headers=self.connection.headers,
        )
        _validate_status_code(r)

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

        logger.debug("POST {0}: {1}: {2!r}".format(url, data, instance))
        r = requests.post(
            url=url,
            auth=self.connection.auth,
            headers=self.connection.headers,
            data=instance.to_json(),
        )
        _validate_status_code(r)

        ser = json.loads(r.content.decode())
        return self.item_resource(self.connection, ser)

    def get(self, sid):
        url = '{0}/{1}/{2}'.format(self.connection.base_url, self.endpoint_path, sid)

        r = requests.get(
            url=url,
            auth=self.connection.auth,
            headers=self.connection.headers,
        )
        _validate_status_code(r)

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
        _validate_status_code(r)

        try:
            data = json.loads(r.content.decode())["items"]
        except ValueError:
            raise ApiServerError("Unparseable response from server: {0}: {1}".format(r.status_code, r.content))
        else:
            return [self.item_resource(self.connection, x) for x in data]
