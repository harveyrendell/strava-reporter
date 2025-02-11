from events.webhook import build_webhook_message


def test_ebikeride_all_fields():
    activity = {
        "id": 123789,
        "name": "Morning EBike Ride",
        "type": "EBikeRide",
        "start_date": "2023-10-01T07:30:00Z",
        "distance": 25000,
        "moving_time": 3600,
        "average_speed": 6.94,
        "total_elevation_gain": 300,
        "average_heartrate": 150,
        "average_cadence": 80,
        "segment_efforts": [],
        "best_efforts": [],
    }
    athlete = {
        "id": 987654321,
        "firstname": "John",
        "lastname": "Doe",
        "profile_medium": "https://example.com/profile.jpg",
    }

    embed = build_webhook_message(activity, athlete)

    assert embed.title == "Morning EBike Ride"
    assert embed.url == "https://strava.com/activities/123789"
    assert embed.colour.value == 0xFFE811  # yellow
    assert embed.fields[0].name == "Distance"
    assert embed.fields[0].value == "25.00 km"
    assert embed.fields[1].name == "Average Speed"
    assert embed.fields[1].value == "25.0 km/h"
    assert embed.fields[2].name == "Elevation"
    assert embed.fields[2].value == "300 m"
    assert embed.fields[3].name == "Moving Time"
    assert embed.fields[3].value == "1:00:00"
    assert embed.fields[4].name == "Avg Heart Rate"
    assert embed.fields[4].value == "150 bpm"
    assert embed.fields[5].name == "Avg Cadence"
    assert embed.fields[5].value == "80 rpm"

def test_empty_ride():
    activity = {
        "id": 123456,
        "name": "Morning EBike Ride",
        "type": "EBikeRide",
        "start_date": "2023-10-01T07:30:00Z",
        "segment_efforts": [],
        "best_efforts": [],
    }
    athlete = {
        "id": 78910,
        "firstname": "John",
        "lastname": "Doe",
        "profile_medium": "https://example.com/profile.jpg",
    }

    embed = build_webhook_message(activity, athlete)

    assert embed.title == ("Morning EBike Ride")
    assert embed.url == "https://strava.com/activities/123456"
    assert embed.colour.value == 0xFFE811  # yellow
    assert len(embed.fields) == 0
