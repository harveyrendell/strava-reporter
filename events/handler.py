import json
import logging
import os
from datetime import datetime

import boto3
import requests
from botocore.exceptions import ClientError
from opentelemetry import trace

from events.webhook import build_webhook_message, post_webhook, update_or_repost_webhook

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
ACTIVITY_TOPIC_ARN = os.environ.get("ACTIVITY_TOPIC_ARN")
STRAVA_API_BASE = "https://www.strava.com/api/v3"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def subscribe(event, *_):
    """Respond to a Strava subscription validation request.

    Must respond with HTTP 200 and the hub.challenge data
    to complete the subscription validation.

    Docs: https://developers.strava.com/docs/webhooks/
    """
    logger.debug(f"New subscription validation request: {event}")

    try:
        challenge = event["queryStringParameters"]["hub.challenge"]

        logger.info(f"Challenge found in request")
        return {"statusCode": 200, "body": json.dumps({"hub.challenge": challenge})}

    except KeyError:
        logger.warning(f"No challenge found in request", exc_info=True)
        return {"statusCode": 400, "body": "Invalid request"}


def receive_event(event, *_):
    body = json.loads(event["body"])  # Convert body string into a usable object

    logger.info(f"New event received: {body}")

    type = body["object_type"]  # one of 'activity' or 'athlete'

    if type == "activity":
        # post message to SNS to be picked up by webhook
        logger.info(f"New activity received. Publishing to {ACTIVITY_TOPIC_ARN}")

        try:
            sns = boto3.client("sns")
            response = sns.publish(
                TopicArn=ACTIVITY_TOPIC_ARN, Message=json.dumps(body)
            )
        except ClientError as err:
            logger.error(f"Failed to publish to {ACTIVITY_TOPIC_ARN}", exc_info=True)

    else:
        # unsupported object type
        pass

    return {"statusCode": 200, "body": "Success"}


def post_event(event, *_):
    logger.info(f"New event: {event}")

    try:
        if len(event["Records"]) > 1:
            logger.warning(
                f"More than one record returned. Only the first will be processed.\n {event}"
            )

        post_message(json.loads(event["Records"][0]["Sns"]["Message"]))

    except KeyError as err:
        logger.warning(
            f"Failed to unwrap SNS message. Falling back to basic HTTP", exc_info=True
        )
        body = json.loads(event["body"])  # Convert body string into a usable object
        post_message(body)

    return {"statusCode": 200, "body": ""}


def get_token_for_athlete(id):
    logger.info("Getting token")

    dynamodb = boto3.resource("dynamodb")
    users_table = dynamodb.Table(os.environ["USERS_DYNAMODB_TABLE"])
    result = users_table.get_item(Key={"id": id})
    token_expiry = datetime.fromtimestamp(float(result["Item"]["expires_at"]))
    expired = token_expiry < datetime.now()

    if expired:
        logger.info("Token is expired. Refreshing now")
        response = requests.post(
            "https://www.strava.com/oauth/token",
            json={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "refresh_token": result["Item"]["refresh_token"],
                "grant_type": "refresh_token",
            },
        )
        if response.status_code != 200:
            logger.error(f"Error refreshing token: {response}")
            logger.error(response.content)

            return {
                "statusCode": response.status_code,
                "body": "Failed to get updated token for athlete",
            }

        response_body = response.json()
        logger.info(response_body)

        item = result["Item"]
        item["access_token"] = response_body["access_token"]
        item["refresh_token"] = response_body["refresh_token"]
        item["expires_at"] = response_body["expires_at"]
        users_table.put_item(Item=item)

        access_token = response_body["access_token"]
    else:
        access_token = result["Item"]["access_token"]

    logger.info(f"access token is {access_token}")

    return access_token


def post_message(body):
    object_type = body["object_type"]  # one of "activity" or "athlete"
    object_id = body["object_id"]  # id for specified object_type
    aspect_type = body["aspect_type"]  # Always "create," "update," or "delete".
    access_token = get_token_for_athlete(body["owner_id"])

    span = trace.get_current_span()
    span.set_attributes({f"strava.webhook.{key}": value for key, value in body.items()})

    if object_type == "activity":
        if aspect_type in ["create", "update"]:
            activity = requests.get(
                f"{STRAVA_API_BASE}/activities/{object_id}",
                headers={"Authorization": f"Bearer {access_token}"},
            ).json()

            athlete = requests.get(
                f"{STRAVA_API_BASE}/athlete",
                headers={"Authorization": f"Bearer {access_token}"},
            ).json()

            # TODO: check response codes for both requests and fail early if we can't get the data we need

            span.set_attributes({f"strava.activity.{key}": value for key, value in activity.items()})
            span.set_attributes({f"strava.athlete.{key}": value for key, value in athlete.items()})

            if aspect_type == "create":
                embed = build_webhook_message(activity, athlete)
                post_webhook(object_id, embed)
            elif aspect_type == "update":
                embed = build_webhook_message(activity, athlete)
                update_or_repost_webhook(object_id, embed)

    elif object_type == "athlete":
        pass

    return 200
