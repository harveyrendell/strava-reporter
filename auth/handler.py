import os
import logging

import boto3
from botocore.vendored import requests

dynamodb = boto3.resource('dynamodb')

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

import auth


def authorize(event, context):
    params = event['queryStringParameters']

    if not params:
        logging.error("Callback failed - no query string parameters included")
        raise Exception("Couldn't authorize user.")
        return

    code = params.get('code', '')
    scope = params.get('scope', '')

    response = requests.post(
        'https://www.strava.com/oauth/token',
        json={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
    )

    response_body = response.json()
    print(f'Token request returned: {response.status_code}')
    print(response_body)

    if response.status_code is 200 and response_body.get('token_type', '') == 'Bearer':
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

        item = {
            'id': response_body['athlete']['id'],
            'username': response_body['athlete']['username'],
            'access_token': response_body['access_token'],
            'refresh_token': response_body['refresh_token'],
            'expires_at': response_body['expires_at'],
        }

        table.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': 'Successfully updated user token!'
    }
