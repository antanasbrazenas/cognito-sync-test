#!/usr/bin/env python3
import boto3
import json

from common.config import config
from common.colourprint import Printer
from datetime import datetime
from warrant import Cognito


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


props = config()

cognito = Cognito(props['USER_POOL_ID'], props['CLIENT_ID'], user_pool_region='eu-west-1',
                  access_key=props['AWS_ACCESS_KEY_ID'], secret_key=props['AWS_SECRET_ACCESS_KEY'])
client = boto3.client('cognito-idp')
identity_client = boto3.client('cognito-identity')
#sync_client = boto3.client('cognito-sync')

#print('')
#print('Identity ID = {} '.format(props['IDENTITY_ID']))
response = identity_client.describe_identity(IdentityId=props['IDENTITY_ID'])
#print(json.dumps(response, cls=DateTimeEncoder, indent=4))

#print('')
#print('Admin Auth')
response = client.admin_initiate_auth(
    UserPoolId=props['USER_POOL_ID'],
    ClientId=props['ADMIN_CLIENT_ID'],
    AuthFlow='CUSTOM_AUTH',
    AuthParameters={
        'USERNAME': props['USERNAME']
    }
)
print(json.dumps(response, cls=DateTimeEncoder, indent=4))
if 'ChallengeName' in response:
    Printer.err("Challenge needs to be completed (Not Implemented)")

if 'AuthenticationResult' in response:
    #print('')
    identity_response = identity_client.get_id(
        AccountId=props['IDENTITY_POOL_ACCOUNT_ID'],
        IdentityPoolId=props['IDENTITY_POOL_ID'],
        Logins={ 'cognito-idp.eu-west-1.amazonaws.com/{}'.format(props['USER_POOL_ID']): response['AuthenticationResult']['IdToken'] })

    identity_id = identity_response['IdentityId']
    print('Identity ID = {}'.format(identity_id))

    print('')
    print('Listing Records')

    # Uncomment below if you want to manage datasets as a Cognito user, rather than an admin
    credentials_response = identity_client.get_credentials_for_identity(
        IdentityId=identity_id,
        Logins={ 'cognito-idp.eu-west-1.amazonaws.com/{}'.format(props['USER_POOL_ID']): response['AuthenticationResult']['IdToken'] })
    credentials = credentials_response['Credentials']
    sync_client = boto3.client('cognito-sync',
                               aws_access_key_id=credentials['AccessKeyId'],
                               aws_secret_access_key=credentials['SecretKey'],
                               aws_session_token=credentials['SessionToken'])

    datasets = sync_client.list_records(
        IdentityPoolId=props['IDENTITY_POOL_ID'],
        #IdentityId='eu-west-1:742d4a8d-3933-446d-b6b4-bbd3066a24bc',
        IdentityId='eu-west-1:9166cdc2-8972-4330-8bd8-ff79a7793510',
        #IdentityId=props['identity_id']
        DatasetName='PermissionService'
    )
    print(json.dumps(datasets, cls=DateTimeEncoder, indent=4))

    # print('')
    # print('Update Records')
    # update_response = sync_client.update_records(
    #     IdentityPoolId=props['IDENTITY_POOL_ID'],
    #     IdentityId='eu-west-1:742d4a8d-3933-446d-b6b4-bbd3066a24bc',
    #     DatasetName='PermissionService',
    #     RecordPatches=[
    #         {
    #             'Op': 'replace',  # or remove
    #             'Key': 'last_updated',
    #             'Value': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now()),
    #             'SyncCount': 0
    #         }
    #     ],
    #     SyncSessionToken=datasets['SyncSessionToken']
    # )
    # print(json.dumps(update_response, cls=DateTimeEncoder, indent=4))

    Printer.success()

else:
    Printer.err("Failed Authentication")
