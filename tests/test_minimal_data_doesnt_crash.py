from events.webhook import build_webhook_message


def test_minimal_data_doesnt_crash_building_embed():
    activity = {
        "name": "Some Activity",
        "description": "Some exercise I guess.",
        "start_date": "2024-01-01T00:00:00Z",
        "type": "Some weird type",
        "id": 0,
    }
    athlete = {
        "firstname": "test",
        "lastname": "person",
        "id": 1,
        "profile_medium": "https://strava.com/link-to-profile-pic"
    }
    build_webhook_message(activity, athlete)
