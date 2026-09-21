from events.webhook import build_webhook_message


def test_build_webhook_message_no_distance():
    activity = {
        "type": "Run",
        "name": "Morning Run",
        "id": 123456,
        "start_date": "2023-10-01T07:00:00Z",
        "description": "A nice morning run",
        "moving_time": 3600,
        "average_heartrate": 150,
        "average_cadence": 80,
        "segment_efforts": [],
        "best_efforts": [],
    }
    athlete = {
        "firstname": "John",
        "lastname": "Doe",
        "id": 78910,
        "profile_medium": "https://example.com/profile.jpg",
    }
    result = build_webhook_message(activity, athlete)
    assert result.fields[0].name == "Description"
    assert result.fields[0].value == "A nice morning run"

def test_build_webhook_message_with_distance():
    activity = {
        "type": "Ride",
        "name": "Evening Ride",
        "id": 654321,
        "start_date": "2023-10-01T18:00:00Z",
        "distance": 20000,
        "moving_time": 3600,
        "average_speed": 5.5,
        "total_elevation_gain": 300,
        "average_heartrate": 140,
        "average_cadence": 90,
        "segment_efforts": [],
        "best_efforts": [],
    }
    athlete = {
        "firstname": "Jane",
        "lastname": "Smith",
        "id": 112233,
        "profile_medium": "https://example.com/profile.jpg",
    }
    result = build_webhook_message(activity, athlete)
    assert result.fields[0].name == "Distance"
    assert result.fields[0].value == "20.0 km"
    assert result.fields[1].name == "Average Speed"
    assert result.fields[1].value == "19.8 km/h"
    assert result.fields[2].name == "Elevation"
    assert result.fields[2].value == "300 m"

def test_build_webhook_message_no_heartrate():
    activity = {
        "type": "Swim",
        "name": "Afternoon Swim",
        "id": 987654,
        "start_date": "2023-10-01T15:00:00Z",
        "distance": 1000,
        "moving_time": 1800,
        "average_speed": 1.2,
        "total_elevation_gain": 0,
        "average_cadence": 60,
        "segment_efforts": [],
        "best_efforts": [],
    }
    athlete = {
        "firstname": "Alice",
        "lastname": "Johnson",
        "id": 445566,
        "profile_medium": "https://example.com/profile.jpg",
    }
    result = build_webhook_message(activity, athlete)
    assert result.fields[0].name == "Distance"
    assert result.fields[0].value == "1.0 km"
    assert result.fields[1].name == "Pace"
    assert result.fields[1].value == "30:00 /km"
    assert result.fields[2].name == "Elevation"
    assert result.fields[2].value == "0 m"

def test_build_webhook_message_no_cadence():
    activity = {
        "type": "Hike",
        "name": "Mountain Hike",
        "id": 123789,
        "start_date": "2023-10-01T09:00:00Z",
        "distance": 5000,
        "moving_time": 7200,
        "average_speed": 0.7,
        "total_elevation_gain": 500,
        "average_heartrate": 130,
        "segment_efforts": [],
        "best_efforts": [],
    }
    athlete = {
        "firstname": "Bob",
        "lastname": "Brown",
        "id": 778899,
        "profile_medium": "https://example.com/profile.jpg",
    }
    result = build_webhook_message(activity, athlete)
    assert result.fields[0].name == "Distance"
    assert result.fields[0].value == "5.0 km"
    assert result.fields[1].name == "Pace"
    assert result.fields[1].value == "24:00 /km"
    assert result.fields[2].name == "Elevation"
    assert result.fields[2].value == "500 m"