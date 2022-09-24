from enum import IntEnum, unique


# using IntEnums allows for sorting by preference smoothly
class AutoName(IntEnum):
    def __str__(self):
        return self.name.capitalize()


@unique
class StudioEventType(AutoName):
    TRIAL_LESSON = 0
    LESSON = 1
    CLASS = 2
    CLASS_PERFORMANCE = 3
    RECITAL = 4
    DRESS_RECITAL = 5
    OTHER = 6


@unique
class Instrument(AutoName):
    VIOLIN = 1
    VIOLA = 2
    FIDDLE = 3
