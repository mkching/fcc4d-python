from fcc4d.resources.base import ItemResource, ListResource


class Account(ItemResource):
    endpoint_path = 'accounts'
    create_fields = (
        'name',
        'login',
        'password',
        'role',
    )
    update_fields = (
        'name',
        'login',
        'password',
    )
    retrieve_fields = (
        'accountSid',
        'name',
        'login',
        'levelOfService',
    )
    fields = set(create_fields) | set(retrieve_fields) | set(update_fields)
    sid_field = 'accountSid'


class Accounts(ListResource):
    endpoint_path = 'accounts'
    item_resource = Account
