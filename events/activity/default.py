from events.activity.activity_colour import ActivityColour


class DefaultActivity:
    colour = ActivityColour.Default
    activity = None

    def __init__(self, activity):
        self.activity = activity

    def get_colour(self):
        return self.colour

    def get_activity_fields(self):
        fields = {
            "Description": self.activity.get_description(),
        }
        return {k: v for k, v in fields.items() if v is not None}
