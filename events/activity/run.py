from events.achievements import get_best_effort_achievements, get_segment_achievements
from events.activity.activity_colour import ActivityColour
from events.activity.raw_activity import RawActivity


class RunActivity:
    colour = ActivityColour.Run
    raw_activity = None

    def __init__(self, raw_activity: RawActivity):
        self.raw_activity = raw_activity

    def get_activity_fields(self):
        fields = {
            "Distance": self.raw_activity.get_distance_km(),
            "Pace": self.raw_activity.get_pace(),
            "Elevation": self.raw_activity.get_elevation_gain(),
            "Moving Time": self.raw_activity.get_moving_time(),
            "Avg Heart Rate": self.raw_activity.get_avg_heartrate(),
            "Avg Cadence": self.raw_activity.get_avg_cadence(),
            "Segment Achievements": get_segment_achievements(self.raw_activity.activity),
            "Best Efforts": get_best_effort_achievements(self.raw_activity.activity),
        }
        return {k: v for k, v in fields.items() if v is not None and v != ""}
