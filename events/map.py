import logging
import os
from urllib import parse as urlparse

MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_activity_map_url(activity):
    # See https://docs.mapbox.com/api/maps/static-images/#path for URL properties

    if not "map" in activity:
        return None

    encoded_polyline = urlparse.quote(activity["map"]["summary_polyline"])
    url = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/path-3+FC4800-1({encoded_polyline})/auto/544x218?access_token={MAPBOX_ACCESS_TOKEN}"
    logger.info(f"Generated map URL: {url}")

    if len(url) > 2048:
        logger.warning(f"Not adding image URL as it exceeds 2048 characters (Maximum allowed by Discord). Actual length: {len(url)}")
        return None
    else:
        return url
