from events.activity.activity_colour import ActivityColour


class RunActivity:
    colour = ActivityColour.Run
    activity = None

    def __init__(self, activity):
        self.activity = activity

    def get_activity_fields(self):
        fields = {
            "Description": self.activity.get_description(),
            "Distance": self.activity.get_distance_km(),
            "Pace": self.activity.get_pace(),
            "Elevation": self.activity.get_elevation_gain(),
            "Moving Time": self.activity.get_moving_time(),
            "Avg Heart Rate": self.activity.get_avg_heartrate(),
            "Avg Cadence": self.activity.get_avg_cadence(),
        }
        return {k: v for k, v in fields.items() if v is not None}
