from enum import Enum, auto


# noinspection PyMethodParameters
class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return self.name.capitalize()


class StudioEventType(AutoName):
    LESSON = auto()
    CLASS = auto()
    CLASS_PERFORMANCE = auto()
    RECITAL = auto()
    DRESS_RECITAL = auto()
    OTHER = auto()


class Instrument(AutoName):
    VIOLIN = auto()
    FIDDLE = auto()
    VIOLA = auto()
