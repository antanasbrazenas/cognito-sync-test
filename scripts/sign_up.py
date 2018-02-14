#!/usr/bin/env python3

from common.config import config
from common.colourprint import Printer
from warrant import Cognito

props = config()

cognito = Cognito(props['USER_POOL_ID'], props['CLIENT_ID'], user_pool_region='eu-west-1')

print('Registering user {}'.format(props['USERNAME']))
print(cognito.register(props['USERNAME'], props['PASSWORD'],
                       **{
                           'email': props['EMAIL'],
                           'address': props['ADDRESS'],
                           'birthdate': props['DATE_OF_BIRTH'],
                           'family_name': props['FAMILY_NAME'],
                           'given_name': props['GIVEN_NAME'],
                           'locale': props['LOCALE'],
                           'name': props['USERNAME'],
                           'phone_number': props['PHONE_NUMBER'],
                           'preferred_username': props['PREFERRED_USERNAME']
                       }))

Printer.success()
