from events.activity.raw_activity import RawActivity
from events.activity.activity_colour import ActivityColour


class DefaultActivity:
    colour = ActivityColour.Default
    activity = None

    def __init__(self, activity: RawActivity):
        self.activity = activity

    def get_colour(self):
        return self.colour

    def get_activity_fields(self):
        fields = {
            "Moving Time": self.activity.get_moving_time(),
            "Heart Rate": self.activity.get_avg_heartrate(),
        }
        return {k: v for k, v in fields.items() if v is not None}
