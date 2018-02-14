#!/usr/bin/env python3
import boto3

from common.config import config
from common.colourprint import Printer
from warrant import Cognito

props = config()

cognito = Cognito(props['USER_POOL_ID'], props['CLIENT_ID'], user_pool_region='eu-west-1')
client = boto3.client('cognito-idp')

print('Activating user {}'.format(props['USERNAME']))
cognito.confirm_sign_up(props['VERIFICATION_CODE'], username=props['USERNAME'])

Printer.success()
