from fcc4d.resources.base import ItemResource, ListResource


class Trunkgroup(ItemResource):
    TYPE_FAILOVER = 0
    TYPE_LOADBALANCE = 1

    endpoint_path = 'trunkGroups'
    create_fields = (
        'name',
        'typeId',
    )
    retrieve_fields = (
        'trunkGroupSid',
        'accountSid',
        'name',
        'typeId',
    )
    update_fields = (
        'name',
        'typeId',
    )
    fields = set(create_fields) | set(retrieve_fields) | set(update_fields)
    sid_field = 'trunkGroupSid'


class Trunkgroups(ListResource):
    endpoint_path = 'trunkGroups'
    item_resource = Trunkgroup
