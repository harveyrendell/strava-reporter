from events.webhook import build_webhook_message


def test_run_no_description():
    activity = {
        "id": 123456,
        "name": "Morning Run",
        "type": "Run",
        "start_date": "2023-10-01T07:30:00Z",
        "moving_time": 3600,
        "distance": 10000,
        "average_speed": 2.78,
        "total_elevation_gain": 50,
        "segment_efforts": [],
        "best_efforts": [],
        "average_heartrate": 150,
        "average_cadence": 80,
    }
    athlete = {
        "id": 78910,
        "firstname": "John",
        "lastname": "Doe",
        "profile_medium": "https://example.com/profile.jpg",
    }

    embed = build_webhook_message(activity, athlete)

    assert embed.title == "Morning Run"
    assert embed.url == "https://strava.com/activities/123456"
    assert embed.colour.value == 0xFC4800  # orange
    assert embed.fields[0].name == "Distance"
    assert embed.fields[0].value == "10.0 km"
    assert embed.fields[1].name == "Pace"
    assert embed.fields[1].value == "6:00 /km"
    assert embed.fields[2].name == "Elevation"
    assert embed.fields[2].value == "50 m"
    assert embed.fields[3].name == "Moving Time"
    assert embed.fields[3].value == "1:00:00"
    assert embed.fields[4].name == "Avg Heart Rate"
    assert embed.fields[4].value == "150 bpm"
    assert embed.fields[5].name == "Avg Cadence"
    assert embed.fields[5].value == "160 spm"

def test_empty_run():
    activity = {
        "id": 123456,
        "name": "Morning Run",
        "type": "Run",
        "start_date": "2023-10-01T07:30:00Z",
        "description": "A nice morning run",
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

    assert embed.title == "Morning Run"
    assert embed.url == "https://strava.com/activities/123456"
    assert embed.colour.value == 0xFC4800  # orange
    assert embed.description == "A nice morning run"
    assert len(embed.fields) == 0


def test_run_with_achievements():
    activity = {
        "id": 123456,
        "name": "Morning Run",
        "type": "Run",
        "start_date": "2023-10-01T07:30:00Z",
        "moving_time": 3600,
        "distance": 10000,
        "average_speed": 2.78,
        "total_elevation_gain": 50,
        "segment_efforts": [
            {"is_kom": True},
            {"pr_rank": 1},
            {"pr_rank": 2},
            {"pr_rank": 3},
            {"pr_rank": 4},
        ],
        "best_efforts": [
            {"is_kom": True},
            {"pr_rank": 1},
            {"pr_rank": 2},
            {"pr_rank": 3},
            {"pr_rank": 4},
        ],
        "average_heartrate": 150,
        "average_cadence": 80,
    }
    athlete = {
        "id": 78910,
        "firstname": "John",
        "lastname": "Doe",
        "profile_medium": "https://example.com/profile.jpg",
    }

    embed = build_webhook_message(activity, athlete)

    assert embed.title == "Morning Run"
    assert embed.url == "https://strava.com/activities/123456"
    assert embed.colour.value == 0xFC4800  # orange
    assert embed.fields[0].name == "Distance"
    assert embed.fields[0].value == "10.0 km"
    assert embed.fields[1].name == "Pace"
    assert embed.fields[1].value == "6:00 /km"
    assert embed.fields[2].name == "Elevation"
    assert embed.fields[2].value == "50 m"
    assert embed.fields[3].name == "Moving Time"
    assert embed.fields[3].value == "1:00:00"
    assert embed.fields[4].name == "Avg Heart Rate"
    assert embed.fields[4].value == "150 bpm"
    assert embed.fields[5].name == "Avg Cadence"
    assert embed.fields[5].value == "160 spm"
    assert embed.fields[6].name == "Segment Achievements"
    assert embed.fields[6].value == ":crown::first_place::second_place::third_place:"
    assert embed.fields[7].name == "Best Efforts"
    assert embed.fields[7].value == ":crown::first_place::second_place::third_place:"


def test_run_with_map_url():
    activity = {
        "id": 123456,
        "name": "Morning Run",
        "type": "Run",
        "start_date": "2023-10-01T07:30:00Z",
        "moving_time": 3600,
        "distance": 10000,
        "average_speed": 2.78,
        "total_elevation_gain": 50,
        "segment_efforts": [],
        "best_efforts": [],
        "average_heartrate": 150,
        "average_cadence": 80,
        "map": {"summary_polyline": "encoded_polyline_string"}
    }
    athlete = {
        "id": 78910,
        "firstname": "John",
        "lastname": "Doe",
        "profile_medium": "https://example.com/profile.jpg",
    }

    embed = build_webhook_message(activity, athlete)

    assert embed.title == "Morning Run"
    assert embed.url == "https://strava.com/activities/123456"
    assert embed.image.url == "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/path-3+FC4800-1(encoded_polyline_string)/auto/544x281?access_token=None"
    assert embed.colour.value == 0xFC4800  # orange
    assert embed.fields[0].name == "Distance"
    assert embed.fields[0].value == "10.0 km"
    assert embed.fields[1].name == "Pace"
    assert embed.fields[1].value == "6:00 /km"
    assert embed.fields[2].name == "Elevation"
    assert embed.fields[2].value == "50 m"
    assert embed.fields[3].name == "Moving Time"
    assert embed.fields[3].value == "1:00:00"
    assert embed.fields[4].name == "Avg Heart Rate"
    assert embed.fields[4].value == "150 bpm"
    assert embed.fields[5].name == "Avg Cadence"
    assert embed.fields[5].value == "160 spm"
