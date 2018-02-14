#!/usr/bin/env python3
from common.config import config
from common.colourprint import Printer
from warrant import Cognito

props = config()

cognito = Cognito(props['USER_POOL_ID'], props['CLIENT_ID'], user_pool_region='eu-west-1', username=props['USERNAME'])

print('Requesting a password reset for {}'.format(props['USERNAME']))
cognito.initiate_forgot_password()

Printer.success()
