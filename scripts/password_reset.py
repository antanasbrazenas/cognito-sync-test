#!/usr/bin/env python3
from common.config import config
from common.colourprint import Printer
from warrant import Cognito

props = config()

cognito = Cognito(props['USER_POOL_ID'], props['CLIENT_ID'], user_pool_region='eu-west-1', username=props['USERNAME'])

print('Resetting password for {}'.format(props['USERNAME']))
cognito.confirm_forgot_password(
    confirmation_code=props['VERIFICATION_CODE'],
    password=props['PASSWORD']
)

Printer.success()
