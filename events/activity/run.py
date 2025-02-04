from events.activity.activity import Activity


class Run(Activity):
    def get_colour(self):
        return self.colours.get("Run")


    def get_activity_fields(self):
        fields = {
            "Description": self._get_description(),
            "Distance": self._get_distance_km(),
            "Pace": self._get_pace(),
            "Elevation": self._get_elevation_gain(),
            "Moving Time": self._get_moving_time(),
            "Avg Heart Rate": self._get_avg_heartrate(),
            "Avg Cadence": self._get_avg_cadence(),
        }
        return {k: v for k, v in fields.items() if v is not None}
