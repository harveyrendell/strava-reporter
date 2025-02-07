from events.webhook import build_webhook_message


def test_swim_no_fields():
    activity = {
        "id": 123456,
        "name": "Morning Swim",
        "type": "Swim",
        "start_date": "2023-10-01T07:30:00Z",
    }
    athlete = {
        "id": 78910,
        "firstname": "John",
        "lastname": "Doe",
        "profile_medium": "https://example.com/profile.jpg",
    }

    embed = build_webhook_message(activity, athlete)

    assert embed.title == "Morning Swim"
    assert embed.url == "https://strava.com/activities/123456"
    assert embed.colour.value == 0x2F63BC
    assert len(embed.fields) == 0


def test_swim_all_fields():
    activity = {
        "id": 123456,
        "name": "Morning Swim",
        "type": "Swim",
        "start_date": "2023-10-01T07:30:00Z",
        "description": "A nice morning swim",
        "distance": 400,
        "moving_time": 536,
        "elapsed_time": 624,
        "average_heartrate": 150,
    }
    athlete = {
        "id": 78910,
        "firstname": "John",
        "lastname": "Doe",
        "profile_medium": "https://example.com/profile.jpg",
    }

    embed = build_webhook_message(activity, athlete)

    assert embed.title == "Morning Swim"
    assert embed.url == "https://strava.com/activities/123456"
    assert embed.colour.value == 0x2F63BC
    assert embed.description == "A nice morning swim"
    assert embed.fields[0].name == "Distance"
    assert embed.fields[0].value == "400 m"
    assert embed.fields[1].name == "Moving Time"
    assert embed.fields[1].value == "8:56"
    assert embed.fields[2].name == "Pace"
    assert embed.fields[2].value == "2:14 /100m"
    assert embed.fields[3].name == "Avg Heart Rate"
    assert embed.fields[3].value == "150 bpm"
