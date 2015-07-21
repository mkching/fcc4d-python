from fcc4d.resources.base import ItemResource, ListResource


class Trunk(ItemResource):
    PROTOCOL_UDP = 1
    PROTOCOL_TCP = 2
    IN_CAPACITY_UNLIMITED = 0
    OUT_CAPACITY_UNLIMITED = 0

    endpoint_path = 'trunks'
    create_fields = (
        'name',
        'endpointSid',
        'endpointAddressTag',
        'trunkGroupSid',
        'protocolId',
        'inCapacity',
        'outCapacity',
        'trunkOutAcl',
    )
    retrieve_fields = (
        'trunkSid',
        'name',
        'endpointSid',
        'endpointAddressTag',
        'trunkGroupSid',
        'protocolId',
        'inCapacity',
        'outCapacity',
        'trunkOutAcl',
    )
    update_fields = (
        'name',
        'endpointSid',
        'endpointAddressTag',
        'trunkGroupSid',
        'protocolId',
        'inCapacity',
        'outCapacity',
        'trunkOutAcl',
    )
    fields = set(create_fields) | set(retrieve_fields) | set(update_fields)
    sid_field = 'trunkSid'


class Trunks(ListResource):
    endpoint_path = 'trunks'
    item_resource = Trunk
