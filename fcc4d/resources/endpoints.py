from operator import itemgetter

from fcc4d.resources.base import ItemResource, ListResource


class Endpoint(ItemResource):
    TYPE_OTHER = 1
    TYPE_WYDE = 2
    TYPE_LYNC = 4

    endpoint_path = 'endpoints'
    create_fields = (
        'accountSid',
        'name',
        'addresses',
        'typeId',
        'capacity',
        'attributes',
    )
    retrieve_fields = (
        'endpointSid',
        'accountSid',
        'name',
        'addresses',
        'typeId',
        'capacity',
        'attributes',
    )
    update_fields = (
        'accountSid',
        'name',
        'addresses',
        'typeId',
        'capacity',
        'attributes',
    )
    fields = set(create_fields) | set(retrieve_fields) | set(update_fields)
    sid_field = 'endpointSid'

    def clean(self):
        super().clean()
        self.addresses = sorted(self.addresses, key=itemgetter('tag'))

class Endpoints(ListResource):
    endpoint_path = 'endpoints'
    item_resource = Endpoint
