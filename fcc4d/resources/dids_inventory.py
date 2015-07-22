from fcc4d.resources.base import ItemResource, ListResource
from fcc4d.resources.dids import Did

class DidsInventory(ListResource):
    LIST_LIMIT = 999

    endpoint_path = 'dids/inventory'
    item_resource = Did
