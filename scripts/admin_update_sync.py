#!/usr/bin/env python3
import boto3
import json

from common.config import config
from common.colourprint import Printer
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


props = config()

client = boto3.client('cognito-idp')
identity_client = boto3.client('cognito-identity')
sync_client = boto3.client('cognito-sync', aws_access_key_id=props['AWS_ACCESS_KEY_ID'], aws_secret_access_key=props['AWS_SECRET_ACCESS_KEY'])

response = client.admin_initiate_auth(
    UserPoolId=props['USER_POOL_ID'],
    ClientId=props['ADMIN_CLIENT_ID'],
    AuthFlow='CUSTOM_AUTH',
    AuthParameters={
        'USERNAME': props['USERNAME']
    }
)

if 'ChallengeName' in response:
    Printer.err("Challenge needs to be completed (Not Implemented)")

if 'AuthenticationResult' in response:
    identity_response = identity_client.get_id(
        AccountId=props['IDENTITY_POOL_ACCOUNT_ID'],
        IdentityPoolId=props['IDENTITY_POOL_ID'],
        Logins={ 'cognito-idp.eu-west-1.amazonaws.com/{}'.format(props['USER_POOL_ID']): response['AuthenticationResult']['IdToken'] })

    identity_id = identity_response['IdentityId']
    print('Identity ID = {}'.format(identity_id))
    print('')
    print('Listing Records')

    # Uncomment below if you want to manage datasets as a Cognito user, rather than an admin
    # credentials_response = identity_client.get_credentials_for_identity(
    #     IdentityId=identity_id,
    #     Logins={ 'cognito-idp.eu-west-1.amazonaws.com/{}'.format(props['USER_POOL_ID']): response['AuthenticationResult']['IdToken'] })
    # credentials = credentials_response['Credentials']
    # sync_client = boto3.client('cognito-sync',
    #                            aws_access_key_id=credentials['AccessKeyId'],
    #                            aws_secret_access_key=credentials['SecretKey'],
    #                            aws_session_token=credentials['SessionToken'])

    datasets = sync_client.list_records(
        IdentityPoolId=props['IDENTITY_POOL_ID'],
        IdentityId=identity_id,
        DatasetName='PermissionService'
    )
    print(json.dumps(datasets, cls=DateTimeEncoder, indent=4))


    print('')
    print('Updating Records')
    update_response = sync_client.update_records(
        IdentityPoolId=props['IDENTITY_POOL_ID'],
        IdentityId=identity_id,
        DatasetName='PermissionService',
        RecordPatches=[
            {
                'Op': 'replace',  # or remove
                'Key': 'last_updated',
                'Value': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now()),
                'SyncCount': datasets.get('DatasetSyncCount', 0)
            }
        ],
        SyncSessionToken=datasets['SyncSessionToken']
    )
    print(json.dumps(update_response, cls=DateTimeEncoder, indent=4))

    Printer.success()

else:
    Printer.err("Failed Authentication")
