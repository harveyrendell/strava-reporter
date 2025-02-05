from enum import Enum


class ActivityColour(Enum):
    Run = 0xFC4800,  # orange
    Ride = 0x3B8544,  # green
    VirtualRide = 0x3B8544,  # green
    Rumn = 0xFFE811,  # electric yellow
    Hike = 0x008000,  # forest green
    RockClimbing = 0xFF8000,  # rock colour?
    AlpineSki = 0xFEFEFE,  # snow
    BackcountrySki = 0xFEFEFE,  # snow
    NordicSki = 0xFEFEFE,  # snow
    Snowboard = 0xFEFEFE,  # snow
    Swim = 0x2F63BC,  # blue
    Workout = 0x00F00F,  # oof ouch owie
    WeightTraining = 0x91A0A2,  # dumbbell grey
    Default = 0xFC4800,  # also orange
