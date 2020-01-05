import json
import logging
import os
from datetime import datetime

import boto3
from botocore.vendored import requests
from botocore.exceptions import ClientError

import discord


CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
ACTIVITY_TOPIC_ARN = os.environ.get('ACTIVITY_TOPIC_ARN')
STRAVA_API_BASE = 'https://www.strava.com/api/v3'

logger = logging.getLogger(__name__)


def subscribe(event, *_):
    '''Respond to a Strava subscription validation request.

    Must respond with HTTP 200 and the hub.challenge data
    to complete the subscription validation.

    Docs: https://developers.strava.com/docs/webhooks/
    '''
    logger.debug(f'New subscription validation request: {event}')

    try:
        challenge = event['queryStringParameters']['hub.challenge']

        logger.info(f'Challenge found in request')
        return {
            'statusCode': 200,
            'body': json.dumps({'hub.challenge': challenge}),
        }

    except KeyError:
        logger.warning(f'No challenge found in request', exc_info=True)
        return {
            'statusCode': 400,
            'body': 'Invalid request',
        }


def receive_event(event, *_):
    body = json.loads(event['body'])  # Convert body string into a usable object

    logger.info(f'New event received: {body}')
    logger.debug(f'Full event: {event}')

    type = body['object_type']  # one of 'activity' or 'athlete'

    if type == 'activity':
        # post message to SNS to be picked up by webhook
        logger.info(f'New activity received. Publishing to {ACTIVITY_TOPIC_ARN}')

        try:
            sns = boto3.client('sns')
            response = sns.publish(
                TopicArn=ACTIVITY_TOPIC_ARN,
                Message=json.dumps(body),
            )
        except ClientError as err:
            logger.error(f'Failed to publish to {ACTIVITY_TOPIC_ARN}', exc_info=True)

    else:
        # unsupported object type
        pass


    return {
        "statusCode": 200,
        "body": 'Success'
    }


def post_event(event, *_):
    logger.info(f'New event: {event}')

    try:
        if len(event['Records']) > 1:
            logger.warning(f'More than one record returned. Only the first will be processed.\n {event}')

        post_message(json.loads(event['Records'][0]['Sns']['Message']))

    except KeyError as err:
        logger.warning(f'Failed to unwrap SNS message. Falling back to basic HTTP', exc_info=True)
        body = json.loads(event['body'])  # Convert body string into a usable object
        post_message(body)

    return {
        'statusCode': 200,
        'body': '',
    }


def get_token_for_athlete(id):
    logger.info('Getting token')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.get_item(
        Key={'id': id}
    )
    token_expiry = datetime.fromtimestamp(result['Item']['expires_at'])
    expired = token_expiry < datetime.now()

    if expired:
        logger.info('Token is expired. Refreshing now')
        response = requests.post(
            'https://www.strava.com/oauth/token',
            json={
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'refresh_token': result['Item']['refresh_token'],
                'grant_type': 'refresh_token'
            }
        )
        if response.status_code != 200:
            logger.error(f'Error refreshing token: {response}')
            logger.error(response.content)

            return {
                'statusCode': response.status_code,
                'body': 'Failed to get updated token for athlete'
            }

        response_body = response.json()
        logger.info(response_body)

        item = result['Item']
        item['access_token'] = response_body['access_token']
        item['refresh_token'] = response_body['refresh_token']
        item['expires_at'] = response_body['expires_at']
        table.put_item(Item=item)

        access_token = response_body['access_token']
    else:
        access_token = result['Item']['access_token']

    logger.info(f'access token is {access_token}')

    return access_token


def post_message(body):
    # See https://developers.strava.com/docs/reference/#api-models-ActivityType
    activity_colours = {
        'Run': int('fc4c02', 16),  # orange
        'Ride': int('66c2ff', 16),  # pale blue
        'Hike': int('008000', 16),  # forest green
        'RockClimbing': int('ff8000', 16),  # rock colour?
        'default': int('cc0000', 16)  # red
    }
    
    object_type = body['object_type']  # one of 'activity' or 'athlete'
    object_id = body['object_id']  # either athlete id or activity id - based on object_type

    access_token = get_token_for_athlete(body['owner_id'])

    if object_type == 'activity':
        activity_resp = requests.get(
            f'{STRAVA_API_BASE}/activities/{object_id}',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        athlete_resp = requests.get(
            f'{STRAVA_API_BASE}/athlete',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        activity = activity_resp.json()
        athlete = athlete_resp.json()

        # Calculate displayed distance
        activity_distance_km = round(activity['distance'] / 1000, 2)

        # Calculate displayed moving time
        hours, rem = divmod(activity['moving_time'], 3600)
        minutes, seconds = divmod(rem, 60)
        time_array = [hours, "{:02d}".format(minutes), "{:02d}".format(seconds)] if hours else [minutes,
                                                                                                "{:02d}".format(
                                                                                                    seconds)]  # add leading zeroes in time format
        activity_moving_time = ':'.join(str(v) for v in time_array)

        # calculate displayed pace
        activity_minutes = activity['moving_time'] / 60
        raw_pace = activity_minutes / activity_distance_km
        pace_minutes, pace_seconds = divmod(raw_pace, 1)
        pace_seconds = round(pace_seconds * 0.6, 2)  # convert to seconds from decimal
        activity_pace = f'{int(pace_minutes)}:{int(pace_seconds * 100):02d}'

        elevation = activity["total_elevation_gain"]
        activity_type = activity["type"]

        embed = {
            "username": "Strava Webhook",
            "avatar_url": "https://d3nn82uaxijpm6.cloudfront.net/mstile-144x144.png?v=dLlWydWlG8",
            "content": "*A new activity was posted to Strava*",
            "embeds": [
                {
                    "title": activity['name'],
                    "url": f"https://strava.com/activities/{activity['id']}",
                    "color": activity_colours[activity_type] if activity_type in activity_colours else activity_colours['default'],
                    "timestamp": activity['start_date'],
                    "author": {
                        "name": f"{athlete['firstname']} {athlete['lastname']}",
                        "url": f"https://strava.com/athletes/{athlete['id']}",
                        "icon_url": athlete['profile_medium']
                    },
                    "fields": [
                        {
                            "name": "Distance",
                            "value": f"{activity_distance_km} km",
                            "inline": True
                        },
                        {
                            "name": "Moving Time",
                            "value": activity_moving_time,
                            "inline": True
                        },
                        {
                            "name": "Pace",
                            "value": f"{activity_pace} /km",
                            "inline": True
                        },
                        {
                            "name": "Elevation",
                            "value": f"{elevation} m",
                            "inline": True
                        }
                    ],
                    "footer": {
                        "icon_url": "https://d3nn82uaxijpm6.cloudfront.net/apple-touch-icon-144x144.png?v=dLlWydWlG8",
                        "text": "Powered by Strava"
                    }
                }
            ]
        }
    elif object_type == 'athlete':
        pass

    logger.info(embed)

    webhook_response = requests.post(
        DISCORD_WEBHOOK_URL,
        headers={'Content-Type': 'application/json'},
        data=json.dumps(embed)
    )

    logger.info(f'Response from webhook: {webhook_response} - {webhook_response.text}')

    return 200
