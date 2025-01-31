from events.handler import get_activity_map_url


def test_get_activity_map_url(monkeypatch):
    activity = {
        "map": {
            "summary_polyline": "encoded_polyline"
        }
    }
    monkeypatch.setattr("events.handler.MAPBOX_ACCESS_TOKEN", "test_token")
    result = get_activity_map_url(activity)
    expected_url = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/path-3+FC4800-1(encoded_polyline)/auto/544x218?access_token=test_token"
    assert result == expected_url