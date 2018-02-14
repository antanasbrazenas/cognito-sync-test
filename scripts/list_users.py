#!/usr/bin/env python3
import boto3

from common.config import config
from common.colourprint import Printer
from warrant import Cognito

props = config()

cognito = Cognito(props['USER_POOL_ID'], props['CLIENT_ID'], user_pool_region='eu-west-1',
                  access_key=props['AWS_ACCESS_KEY_ID'], secret_key=props['AWS_SECRET_ACCESS_KEY'])
client = boto3.client('cognito-idp')

users = cognito.get_users()
print('Users (total {}):'.format(len(users)))
for u in users:
    print(' * {}: email={} | email_verified={}'.format(u.username, u.email, u.email_verified))

Printer.success()
