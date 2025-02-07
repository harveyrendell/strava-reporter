from events.activity.raw_activity import RawActivity

def test_get_distance_m_with_valid_distance():
    activity_data = {"distance": 1500}
    raw_activity = RawActivity(activity_data)
    assert raw_activity.get_distance_m() == "1500 m"

def test_get_distance_m_with_decimal_point():
    activity_data = {"distance": 234.5}
    raw_activity = RawActivity(activity_data)
    assert raw_activity.get_distance_m() == "234 m"

def test_get_distance_m_with_zero_distance():
    activity_data = {"distance": 0}
    raw_activity = RawActivity(activity_data)
    assert raw_activity.get_distance_m() is None

def test_get_distance_m_with_no_distance_key():
    activity_data = {}
    raw_activity = RawActivity(activity_data)
    assert raw_activity.get_distance_m() is None

def test_get_distance_m_with_negative_distance():
    activity_data = {"distance": -100}
    raw_activity = RawActivity(activity_data)
    assert raw_activity.get_distance_m() is None