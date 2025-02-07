import logging
import os
from datetime import datetime

import boto3
import discord

from events.achievements import get_best_effort_achievements, get_segment_achievements
from events.activity.default import DefaultActivity
from events.activity.raw_activity import RawActivity
from events.activity.run import RunActivity
from events.map import get_activity_map_url

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# See https://developers.strava.com/docs/reference/#api-models-ActivityType
activity_colours = {
    "Run": 0xFC4800,  # orange
    "Ride": 0x3B8544,  # green
    "VirtualRide": 0x3B8544,  # green
    "EBikeRide": 0xFFE811,  # electric yellow
    "Hike": 0x008000,  # forest green
    "RockClimbing": 0xFF8000,  # rock colour?
    "AlpineSki": 0xFEFEFE,  # snow
    "BackcountrySki": 0xFEFEFE,  # snow
    "NordicSki": 0xFEFEFE,  # snow
    "Snowboard": 0xFEFEFE,  # snow
    "Swim": 0x2F63BC,  # blue
    "Workout": 0x00F00F,  # oof ouch owie
    "WeightTraining": 0x91A0A2,  # dumbbell grey
    "default": 0xFC4800,  # also orange
}

# Activity types to use average speed instead of pace
use_speed = ["Ride", "VirtualRide", "EBikeRide"]


def build_webhook_message(activity, athlete):
    activity_type = activity["type"]

    # Use new function for migrated activity types.
    # Add new types here as they are migrated
    if activity_type in ["Run"]:
        return build_webhook_message_new(activity, athlete)

    # Calculate displayed moving time
    activity_moving_time = None
    if "moving_time" in activity:
        hours, rem = divmod(activity["moving_time"], 3600)
        minutes, seconds = divmod(rem, 60)
        time_array = (
            [hours, "{:02d}".format(minutes), "{:02d}".format(seconds)]
            if hours
            else [minutes, "{:02d}".format(seconds)]
        )  # add leading zeroes in time format
        activity_moving_time = ":".join(str(v) for v in time_array)

    # Don't try to calculate distance metrics for workouts
    activity_has_distance = "distance" in activity and activity.get("distance") > 0

    if activity_has_distance:
        # Calculate displayed distance
        activity_distance_km = round(activity["distance"] / 1000, 2)

        # calculate displayed pace
        activity_minutes = activity["moving_time"] / 60
        raw_pace = activity_minutes / activity_distance_km
        pace_minutes, pace_seconds = divmod(raw_pace, 1)
        pace_seconds = round(pace_seconds * 0.6, 2)  # convert to seconds from decimal
        activity_pace = f"{int(pace_minutes)}:{int(pace_seconds * 100):02d}"
        activity_speed_kmh = round(activity["average_speed"] * 3.6, 1)  # convert from m/s

        elevation = activity["total_elevation_gain"]
    else:
        description = activity["description"]

    # `average_heartrate` field is only added if activity has heartrate data
    avg_heartrate = activity.get("average_heartrate")
    avg_heartrate = round(avg_heartrate) if avg_heartrate else avg_heartrate

    # `average_cadence` field is only added if activity has cadence data
    avg_cadence = activity.get("average_cadence")
    avg_cadence = round(avg_cadence) if avg_cadence else avg_cadence

    segment_achievements = get_segment_achievements(activity)
    best_effort_achievements = get_best_effort_achievements(activity)
    activity_map_url = get_activity_map_url(activity)

    # Build new embed
    embed = discord.Embed(
        title=activity["name"],
        url=f"https://strava.com/activities/{activity['id']}",
        colour=activity_colours.get(activity_type, activity_colours["default"]),
    )
    embed.timestamp = datetime.strptime(activity["start_date"], "%Y-%m-%dT%H:%M:%SZ")
    embed.set_author(
        name=f"{athlete['firstname']} {athlete['lastname']}",
        url=f"https://strava.com/athletes/{athlete['id']}",
        icon_url=athlete["profile_medium"],
    )
    embed.set_footer(
        text="Powered by Strava",
        icon_url="https://d3nn82uaxijpm6.cloudfront.net/apple-touch-icon-144x144.png?v=dLlWydWlG8",
    )

    if activity_map_url:
        embed.set_image(url=activity_map_url)

    if activity_has_distance:
        embed.add_field(name="Distance", value=f"{activity_distance_km} km", inline=True)

        if activity_type in use_speed:
            embed.add_field(
                name="Average Speed", value=f"{activity_speed_kmh} km/h", inline=True
            )
        else:
            embed.add_field(name="Pace", value=f"{activity_pace} /km", inline=True)

        embed.add_field(name="Elevation", value=f"{elevation} m", inline=True)
    else:
        embed.add_field(name="Description", value=description, inline=True)

    if activity_moving_time:
        embed.add_field(name="Moving Time", value=activity_moving_time, inline=True)

    if avg_heartrate:
        embed.add_field(name="Avg Heart Rate", value=f"{avg_heartrate} bpm", inline=True)

    if avg_cadence and activity_type in use_speed:  # bike activities
        embed.add_field(name="Avg Cadence", value=avg_cadence, inline=True)
    elif avg_cadence:  # step activities need doubling
        embed.add_field(name="Avg Cadence", value=f"{avg_cadence * 2} spm", inline=True)

    if segment_achievements:
        embed.add_field(name="Segment Achievements", value=segment_achievements)

    if best_effort_achievements:
        embed.add_field(name="Best Efforts", value=best_effort_achievements)

    return embed


def build_webhook_message_new(activity_data, athlete):
    activity_type = activity_data["type"]
    raw = RawActivity(activity_data)

    match activity_type:
        case "Run":
            activity = RunActivity(raw)
        case _:
            activity = DefaultActivity(raw)

    embed = get_base_embed(activity_data, athlete)

    for key, value in activity.get_activity_fields().items():
        embed.add_field(name=key, value=value, inline=True)

    return embed


def get_base_embed(activity, athlete):
    activity_type = activity["type"]
    embed = discord.Embed(
        title=activity["name"],
        url=f"https://strava.com/activities/{activity['id']}",
        colour=activity_colours.get(activity_type, activity_colours["default"]),
    )
    embed.timestamp = datetime.strptime(activity["start_date"], "%Y-%m-%dT%H:%M:%SZ")
    embed.set_author(
        name=f"{athlete['firstname']} {athlete['lastname']}",
        url=f"https://strava.com/athletes/{athlete['id']}",
        icon_url=athlete["profile_medium"],
    )
    embed.set_footer(
        text="Powered by Strava",
        icon_url="https://d3nn82uaxijpm6.cloudfront.net/apple-touch-icon-144x144.png?v=dLlWydWlG8",
    )
    return embed

def post_webhook(activity_id, embed):
    webhook = discord.SyncWebhook.from_url(DISCORD_WEBHOOK_URL)
    webhook_message = webhook.send(
        "*A new activity was posted to Strava*",
        avatar_url="https://d3nn82uaxijpm6.cloudfront.net/mstile-144x144.png?v=dLlWydWlG8",
        username="Strava Webhook",
        embed=embed,
        wait=True,
    )

    dynamodb = boto3.resource("dynamodb")
    messages_table = dynamodb.Table(os.environ["MESSAGES_DYNAMODB_TABLE"])
    messages_table.put_item(
        Item={"activity_id": activity_id, "message_id": webhook_message.id}
    )


def update_or_repost_webhook(activity_id, embed):
    # Should be called when an activity is updated.
    webhook = discord.SyncWebhook.from_url(DISCORD_WEBHOOK_URL)

    dynamodb = boto3.resource("dynamodb")
    messages_table = dynamodb.Table(os.environ["MESSAGES_DYNAMODB_TABLE"])
    result = messages_table.get_item(Key={"activity_id": activity_id})

    # Search for existing entry in messages table or posts a new message.
    if message_id := result.get("Item", {}).get("message_id"):
        webhook.edit_message(message_id=message_id, embed=embed)
    else:
        post_webhook(embed)
