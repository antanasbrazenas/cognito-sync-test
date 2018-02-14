#!/usr/bin/env python3

import boto3
from warrant.aws_srp import AWSSRP

from common.config import config
from common.colourprint import Printer
from warrant import Cognito

props = config()


client = boto3.client('cognito-idp')
aws = AWSSRP(username=props['USERNAME'], password=props['PASSWORD'], pool_id=props['USER_POOL_ID'],
              client_id=props['CLIENT_ID'], client=client)

print('Authenticating user {}...'.format(props['USERNAME']))
tokens = aws.authenticate_user()
print('User {} authenticated! Updating user profiles'.format(props['USERNAME']))

cognito = Cognito(props['USER_POOL_ID'],props['CLIENT_ID'], user_pool_region='eu-west-1',
                  id_token=tokens['AuthenticationResult']['IdToken'],refresh_token=tokens['AuthenticationResult']['RefreshToken'],
                  access_token=tokens['AuthenticationResult']['AccessToken'])
cognito.update_profile({
    'address': props['ADDRESS'],
    'locale': props['LOCALE'],
    'phone_number': props['PHONE_NUMBER'],
    'picture': props['PICTURE'],
    'preferred_username': props['PREFERRED_USERNAME'],
    'custom:certificate_proof': props['PROOF_OF_CERTIFICATES'],
    'custom:partner': props['PARTNER']
    #
    # The following attributes are not mutable
    #
    # 'email': props['EMAIL'],
    # 'birthdate': props['DATE_OF_BIRTH'],
    # 'custom:engineer_ID': props['ENGINEER_ID'],
    # 'family_name': props['FAMILY_NAME'],
    # 'given_name': props['GIVEN_NAME'],
    # 'name': props['USERNAME']
})


Printer.success()