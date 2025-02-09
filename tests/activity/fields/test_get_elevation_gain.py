from events.activity.raw_activity import RawActivity

def test_get_elevation_gain_with_valid_elevation():
    activity_data = {"total_elevation_gain": 150}
    raw_activity = RawActivity(activity_data)
    assert raw_activity.get_elevation_gain() == "150 m"

def test_get_elevation_gain_with_decimal_point():
    activity_data = {"total_elevation_gain": 234.5}
    raw_activity = RawActivity(activity_data)
    assert raw_activity.get_elevation_gain() == "234 m"

def test_get_elevation_gain_with_zero_elevation():
    activity_data = {"total_elevation_gain": 0}
    raw_activity = RawActivity(activity_data)
    assert raw_activity.get_elevation_gain()  == "0 m"

def test_get_elevation_gain_with_no_elevation_gain_key():
    activity_data = {}
    raw_activity = RawActivity(activity_data)
    assert raw_activity.get_elevation_gain() is None
