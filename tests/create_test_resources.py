#!/bin/env python

import os
import sys
sys.path.append(os.path.dirname(__file__) + '/..')

import requests
import uuid

from fcc4d.client import FCC4DClient

api = FCC4DClient(base_url=sys.argv[1], username=sys.argv[2], password=sys.argv[3])
password1 = sys.argv[4]
password2 = sys.argv[5]

if len(api.accounts.list(filter='login eq "wv-test1"')) == 0:
    print("Creating account wv-test1")
    print(api.accounts.create(login="wv-test1", password=password1, name="test user for wv unittest"))
accountSid1 = api.accounts.list(filter='login eq "wv-test1"')[0].accountSid
api1 = FCC4DClient(base_url=sys.argv[1], username='wv-test1', password=password1)

if len(api.accounts.list(filter='login eq "wv-test2"')) == 0:
    print("Creating account wv-test2")
    print(api.accounts.create(login="wv-test2", password=password2, name="test user for wv unittest"))
accountSid2 = api.accounts.list(filter='login eq "wv-test2"')[0].accountSid
api2 = FCC4DClient(base_url=sys.argv[1], username='wv-test2', password=password2)

if len(api1.dids.list()) == 0:
    print("Creating did for account1")
    did = api1.dids_inventory.list(limit=1)[0]
    print(api1.dids.create(instance=did))

if len(api2.dids.list()) == 0:
    print("Creating did for account2")
    did = api2.dids_inventory.list(limit=1)[0]
    print(api2.dids.create(instance=did))

if len(api1.endpoints.list()) == 0:
    print("Creating endpoint for account1")
    print(api1.endpoints.create(addresses=[{"ip":"10.255.255.1", "port": "5060", "tag": "test"}], typeId=4))

if len(api2.endpoints.list()) == 0:
    print("Creating endpoint for account2")
    print(api2.endpoints.create(addresses=[{"ip":"10.255.255.2", "port": "5060", "tag": "test"}], typeId=4))

if len(api1.trunks.list()) < 2:
   print("Creating trunks for account1")
   print(api1.trunks.create(protocolId=1))
   print(api1.trunks.create(protocolId=1))

if len(api2.trunks.list()) < 2:
   print("Creating trunks for account2")
   print(api2.trunks.create(protocolId=1))
   print(api2.trunks.create(protocolId=1))

if len(api1.trunkgroups.list()) == 0:
    print("Creating trunkgroup for account1")
    print(api1.trunkgroups.create(typeId=1))

if len(api2.trunkgroups.list()) == 0:
    print("Creating trunkgroup for account2")
    print(api2.trunkgroups.create(typeId=1))
