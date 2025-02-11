from events.activity import RawActivity
from events.activity.activity_colour import ActivityColour


class RideActivity:
    colour = ActivityColour.Ride
    activity = None

    def __init__(self, activity: RawActivity):
        self.activity = activity

    def get_activity_fields(self):
        fields = {
            "Distance": self.activity.get_distance_km(),
            "Average Speed": self.activity.get_avg_speed_kmh(),
            "Elevation": self.activity.get_elevation_gain(),
            "Moving Time": self.activity.get_moving_time(),
            "Avg Heart Rate": self.activity.get_avg_heartrate(),
            "Avg Cadence": self.activity.get_avg_cadence(),
        }
        return {k: v for k, v in fields.items() if v is not None and v != ""}
