from events.activity.activity_colour import ActivityColour
from events.activity.raw_activity import RawActivity


class SwimActivity:
    colour = ActivityColour.Swim
    raw_activity = None

    def __init__(self, raw_activity: RawActivity):
        self.raw_activity = raw_activity

    def get_activity_fields(self):
        fields = {
           # Main fields
            "Distance": self.raw_activity.get_distance_m(),
            "Moving Time": self.raw_activity.get_moving_time(),
            "Pace": self.raw_activity.get_pace_100m(),
            # Additional fields
            "Avg Heart Rate": self.raw_activity.get_avg_heartrate(),
        }
        return {k: v for k, v in fields.items() if v is not None and v != ""}
