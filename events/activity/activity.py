from abc import ABC, abstractmethod


class Activity(ABC):
    # See https://developers.strava.com/docs/reference/#api-models-ActivityType
    colours = {
        "Run": 0xFC4800,  # orange
        "Ride": 0x3B8544,  # green
        "VirtualRide": 0x3B8544,  # green
        "EBikeRide": 0xFFE811,  # electric yellow
        "Hike": 0x008000,  # forest green
        "RockClimbing": 0xFF8000,  # rock colour?
        "AlpineSki": 0xFEFEFE,  # snow
        "BackcountrySki": 0xFEFEFE,  # snow
        "NordicSki": 0xFEFEFE,  # snow
        "Snowboard": 0xFEFEFE,  # snow
        "Swim": 0x2F63BC,  # blue
        "Workout": 0x00F00F,  # oof ouch owie
        "WeightTraining": 0x91A0A2,  # dumbbell grey
        "default": 0xFC4800,  # also orange
    }
    activity = None

    def __init__(self, activity):
        self.activity = activity

    @abstractmethod
    def get_colour(self):
        return self.colours.get("default")

    @abstractmethod
    def get_activity_fields(self):
        return {}

    ### Methods for retrieving activity fields. Should return the field value to display or None if not available

    def _get_description(self):
        description = self.activity.get("description")
        if description:
            return description
        return None

    def _get_distance_km(self):
        activity_has_distance = "distance" in self.activity and self.activity.get("distance") > 0
        if activity_has_distance:
            distance_km = round(self.activity["distance"] / 1000, 2)
            return f"{distance_km} km"
        return None

    def _get_pace(self):
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

    def _get_elevation_gain(self):
        elevation = self.activity.get("total_elevation_gain")
        if elevation:
            return f"{elevation} m"
        return None

    def _get_moving_time(self):
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

    def _get_avg_heartrate(self):
        avg_heartrate = self.activity.get("average_heartrate")
        if avg_heartrate:
            return f"{round(avg_heartrate)} bpm"
        return None

    def _get_avg_cadence(self):
        # We need to double the cadence value for everything that isn't a cycling activity
        is_cycling_activity = self.activity.get("type") in ["Ride", "VirtualRide", "EBikeRide"]
        avg_cadence = self.activity.get("average_cadence")

        if avg_cadence and not is_cycling_activity:
            return f"{round(avg_cadence * 2)} spm"
        elif avg_cadence:
            return f"{round(avg_cadence)} spm"
        return None
