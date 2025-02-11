from events.map import get_activity_map_url


def test_get_activity_map_url(monkeypatch):
    activity = {
        "map": {
            "summary_polyline": "encoded_polyline"
        }
    }
    monkeypatch.setattr("events.map.MAPBOX_ACCESS_TOKEN", "test_token")
    result = get_activity_map_url(activity)
    expected_url = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/path-3+FC4800-1(encoded_polyline)/auto/544x281?access_token=test_token"
    assert result == expected_url

def test_get_activity_map_url_no_map():
    activity = {}
    result = get_activity_map_url(activity)
    assert result is None

def test_get_activity_map_url_long_url(monkeypatch):
    activity = {
        "map": {
            "summary_polyline": "a" * 2049
        }
    }
    monkeypatch.setattr("events.map.MAPBOX_ACCESS_TOKEN", "test_token")
    result = get_activity_map_url(activity)
    assert result is None