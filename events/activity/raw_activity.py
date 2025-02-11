class RawActivity:
    activity = None
    type = None

    def __init__(self, activity: dict):
        self.activity = activity
        self.type = activity.get("type")

    ### Methods for retrieving activity fields. Should return the field value to display or None if not available

    def activity_has_distance(self):
        return "distance" in self.activity and self.activity.get("distance") > 0


    def get_distance_km(self):
        if not self.activity_has_distance():
            return None

        distance_km = "{:.2f}".format(round(self.activity["distance"] / 1000, 2))
        return f"{distance_km} km"


    def get_distance_m(self):
        if not self.activity_has_distance():
            return None

        distance_m = int(round(self.activity["distance"], 0))
        return f"{distance_m} m"


    def get_pace(self):
        if not self.activity_has_distance():
            return None

        distance_km = round(self.activity["distance"] / 1000, 2)
        activity_minutes = self.activity["moving_time"] / 60
        raw_pace = activity_minutes / distance_km
        pace_minutes, pace_seconds = divmod(raw_pace, 1)
        pace_seconds = round(pace_seconds * 0.6, 2)  # convert to seconds from decimal
        pace = f"{int(pace_minutes)}:{int(pace_seconds * 100):02d}"
        return f"{pace} /km"


    def get_pace_100m(self):
        if not self.activity_has_distance():
            return None

        distance = self.activity["distance"]
        activity_minutes = self.activity["moving_time"] / 60
        raw_pace = activity_minutes / distance * 100
        pace_minutes, pace_seconds = divmod(raw_pace, 1)
        pace_seconds = round(pace_seconds * 0.6, 2)  # convert to seconds from decimal
        pace = f"{int(pace_minutes)}:{int(pace_seconds * 100):02d}"
        return f"{pace} /100m"


    def get_avg_speed_kmh(self):
        if not self.activity_has_distance():
            return None

        activity_speed_kmh = round(self.activity["average_speed"] * 3.6, 1)  # convert from m/s
        return f"{activity_speed_kmh} km/h"


    def get_elevation_gain(self):
        if not "total_elevation_gain" in self.activity:
            return None

        elevation = self.activity.get("total_elevation_gain")
        elevation = int(round(elevation, 0))
        return f"{elevation} m"


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
        avg_cadence = self.activity.get("average_cadence")
        if not "average_cadence" in self.activity:
            return None

        is_cycling_activity = self.activity.get("type") in ["Ride", "VirtualRide", "EBikeRide"]
        if is_cycling_activity:
            return f"{round(avg_cadence)} rpm"
        else:
            # We need to double the cadence value for everything that isn't a cycling activity
            return f"{round(avg_cadence * 2)} spm"

