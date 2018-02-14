#!/usr/bin/env python3
import boto3
import json
import requests

from common.config import config
from common.colourprint import Printer
from requests_aws4auth import AWS4Auth
from warrant import Cognito
from warrant.aws_srp import AWSSRP

props = config()

client = boto3.client('cognito-idp')
user = AWSSRP(username=props['USERNAME'], password=props['PASSWORD'], pool_id=props['USER_POOL_ID'],
              client_id=props['CLIENT_ID'], client=client)
tokens = user.authenticate_user()

ID_TOKEN = tokens['AuthenticationResult']['IdToken']

identity_client = boto3.client('cognito-identity', region_name='eu-west-1')
identity_response = identity_client.get_id(
    AccountId=props['IDENTITY_POOL_ACCOUNT_ID'],
    IdentityPoolId=props['IDENTITY_POOL_ID'],
    Logins={ 'cognito-idp.eu-west-1.amazonaws.com/{}'.format(props['USER_POOL_ID']): ID_TOKEN })

identity_id = identity_response['IdentityId']
print('identity_id:', identity_id)

credentials_response = identity_client.get_credentials_for_identity(
    IdentityId=identity_id,
    Logins={ 'cognito-idp.eu-west-1.amazonaws.com/{}'.format(props['USER_POOL_ID']): ID_TOKEN })


credentials = credentials_response['Credentials']
access_key_id = credentials['AccessKeyId']
secret_key = credentials['SecretKey']
session_token = credentials['SessionToken']
print('access_key_id:', access_key_id)
print('secret_key:', secret_key)
print('session_token:', session_token)

# auth = AWS4Auth(access_key_id, secret_key, 'eu-west-1', 'execute-api', session_token=session_token)
# r = requests.request(props['TARGET_METHOD'], props['TARGET_URL'], auth=auth, headers={
#     'x-api-key': props['TARGET_API_KEY'],
#     'x-idtoken': ID_TOKEN
# },
# params=None,  # params={"include[hubs]": "devices"}
# data=None  # json.dumps({"data":{"id":"::215:8d00:12e:4d99@2029726276851335171","type":"devices","attributes":{"name":"Tuneable Li"}}})
# )
#
# print('\nRESPONSE:')
# if r.status_code == 200:
#     Printer.green('Response code: {}'.format(r.status_code))
#     Printer.green(r.text)
#
# else:
#     Printer.red('Response code: {}'.format(r.status_code))
#     Printer.red(r.text)
#     Printer.red(r.reason)

u = Cognito(props['USER_POOL_ID'], props['CLIENT_ID'],
            id_token=tokens['AuthenticationResult']['IdToken'], refresh_token=tokens['AuthenticationResult']['RefreshToken'],
            access_token=tokens['AuthenticationResult']['AccessToken'])
u.logout()
