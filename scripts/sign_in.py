#!/usr/bin/env python3
import boto3
import json

from common.config import config
from common.colourprint import Printer
from warrant.aws_srp import AWSSRP

props = config()

client = boto3.client('cognito-idp')
print('Logging in with user {}'.format(props['USERNAME']))

user = AWSSRP(username=props['USERNAME'], password=props['PASSWORD'], pool_id=props['USER_POOL_ID'],
           client_id=props['CLIENT_ID'], client=client)
tokens = user.authenticate_user()
if tokens:
    print('Authentication Successful')
print(json.dumps(tokens, indent=4))


Printer.success()
