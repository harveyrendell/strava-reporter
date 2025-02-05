from events.activity.raw_activity import RawActivity
from events.activity.run import RunActivity
from events.webhook import get_base_embed


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
    run = RunActivity(RawActivity(activity))
    run.get_activity_fields()
    embed = get_base_embed(activity, athlete)

    for key, value in run.get_activity_fields().items():
        embed.add_field(name=key, value=value, inline=True)

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
    run = RunActivity(RawActivity(activity))
    run.get_activity_fields()
    embed = get_base_embed(activity, athlete)

    for key, value in run.get_activity_fields().items():
        embed.add_field(name=key, value=value, inline=True)

    assert embed.title == "Morning Run"
    assert embed.url == "https://strava.com/activities/123456"
    assert embed.colour.value == 0xFC4800  # orange
    assert embed.fields[0].name == "Description"
    assert embed.fields[0].value == "A nice morning run"
    assert embed.fields[0].inline == True
    assert len(embed.fields) == 1