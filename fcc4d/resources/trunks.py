from fcc4d.resources.base import ItemResource, ListResource


class Trunk(ItemResource):
    PROTOCOL_UDP = 1
    PROTOCOL_TCP = 2
    IN_CAPACITY_UNLIMITED = 0
    OUT_CAPACITY_UNLIMITED = 0

    PROTOCOL_MAP = {
        'udp': PROTOCOL_UDP,
        'UDP': PROTOCOL_UDP,
        'tcp': PROTOCOL_TCP,
        'TCP': PROTOCOL_TCP,
    }
    PROTOCOL_ID_MAP = {
        PROTOCOL_UDP: 'udp',
        PROTOCOL_TCP: 'tcp',
    }

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

    @property
    def protocol(self):
        return Trunk.PROTOCOL_ID_MAP.get(self.protocolId, None)

class Trunks(ListResource):
    endpoint_path = 'trunks'
    item_resource = Trunk
