class RawActivity:
    activity = None

    def __init__(self, activity):
        self.activity = activity

    ### Methods for retrieving activity fields. Should return the field value to display or None if not available

    def get_description(self):
        description = self.activity.get("description")
        if description:
            return description
        return None

    def get_distance_km(self):
        activity_has_distance = "distance" in self.activity and self.activity.get("distance") > 0
        if activity_has_distance:
            distance_km = round(self.activity["distance"] / 1000, 2)
            return f"{distance_km} km"
        return None

    def get_pace(self):
        activity_has_distance = "distance" in self.activity and self.activity.get("distance") > 0
        if not activity_has_distance:
            return None

        distance_km = round(self.activity["distance"] / 1000, 2)
        activity_minutes = self.activity["moving_time"] / 60
        raw_pace = activity_minutes / distance_km
        pace_minutes, pace_seconds = divmod(raw_pace, 1)
        pace_seconds = round(pace_seconds * 0.6, 2)  # convert to seconds from decimal
        pace = f"{int(pace_minutes)}:{int(pace_seconds * 100):02d}"
        return f"{pace} /km"
        # activity_speed_kmh = round(self.activity["average_speed"] * 3.6, 1)  # convert from m/s

    def get_elevation_gain(self):
        elevation = self.activity.get("total_elevation_gain")
        if elevation:
            return f"{elevation} m"
        return None

    def get_moving_time(self):
        if not "moving_time" in self.activity:
            return None

        hours, rem = divmod(self.activity["moving_time"], 3600)
        minutes, seconds = divmod(rem, 60)
        time_array = (
            [hours, "{:02d}".format(minutes), "{:02d}".format(seconds)]
            if hours
            else [minutes, "{:02d}".format(seconds)]
        )  # add leading zeroes in time format
        return ":".join(str(v) for v in time_array)

    def get_avg_heartrate(self):
        avg_heartrate = self.activity.get("average_heartrate")
        if avg_heartrate:
            return f"{round(avg_heartrate)} bpm"
        return None

    def get_avg_cadence(self):
        # We need to double the cadence value for everything that isn't a cycling activity
        is_cycling_activity = self.activity.get("type") in ["Ride", "VirtualRide", "EBikeRide"]
        avg_cadence = self.activity.get("average_cadence")

        if avg_cadence and not is_cycling_activity:
            return f"{round(avg_cadence * 2)} spm"
        elif avg_cadence:
            return f"{round(avg_cadence)} spm"
        return None
