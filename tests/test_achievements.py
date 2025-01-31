from events.achievements import get_segment_achievements, get_best_effort_achievements


def test_get_segment_achievements():
    activity = {
        "segment_efforts": [
            {"is_kom": True},
            {"pr_rank": 1},
            {"pr_rank": 2},
            {"pr_rank": 3},
            {"pr_rank": 4},
        ]
    }
    result = get_segment_achievements(activity)
    assert result == ":crown::first_place::second_place::third_place:"

def test_get_best_effort_achievements():
    activity = {
        "best_efforts": [
            {"is_kom": True},
            {"pr_rank": 1},
            {"pr_rank": 2},
            {"pr_rank": 3},
            {"pr_rank": 4},
        ]
    }
    result = get_best_effort_achievements(activity)
    assert result == ":crown::first_place::second_place::third_place:"
