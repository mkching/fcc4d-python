from fcc4d.resources.base import ItemResource, ListResource


class Did(ItemResource):
    endpoint_path = 'dids'
    create_fields = (
        'phonenumber',
        'trunkSid',
        'trunkGroupSid',
    )
    retrieve_fields = (
        'didSid',
        'accountSid',
        'trunkSid',
        'trunkGroupSid',
        'phonenumber',
        'capabilities',
        'countryId',
        'internationalFormat',
        'inCountryFormat',
        'vendorId',
    )
    update_fields = (
        'trunkSid',
        'trunkGroupSid',
    )
    fields = set(create_fields) | set(retrieve_fields) | set(update_fields)
    sid_field = 'didSid'

class Dids(ListResource):
    endpoint_path = 'dids'
    item_resource = Did
