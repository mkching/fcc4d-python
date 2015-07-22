from fcc4d.base.rest_client import RestClient, RestConnection
from fcc4d.resources import (
    Accounts,
    Dids,
    DidsInventory,
    Endpoints,
    Trunks,
    Trunkgroups,
    Countries,
    Sms,
    Push,
)


class FCC4DClient(RestClient):
    def __init__(self, username, password, base_url="https://carrierx-api.freeconferencecall.com/api/"):
        super().__init__(RestConnection(username, password, base_url))

        self.accounts = Accounts(self.connection)
        self.dids = Dids(self.connection)
        self.dids_inventory = DidsInventory(self.connection)
        self.endpoints = Endpoints(self.connection)
        self.trunks = Trunks(self.connection)
        self.trunkgroups = Trunkgroups(self.connection)
        self.countries = Countries(self.connection)
        self.sms = Sms(self.connection)
        self.push = Push(self.connection)
