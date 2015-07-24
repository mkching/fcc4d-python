#!/bin/sh

#export HTTP_TRACE=1

python -munittest accounts
python -munittest accounts_admin
python -munittest dids
python -munittest endpoints
python -munittest trunks
python -munittest trunkgroups
