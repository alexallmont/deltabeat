class EventAttributeException(Exception):
    """
    Report type inconsistencies when setting an event's attributes.
    """


class Event:
    """
    A class for any type of event in a beat. Events must have a position, which
    is a float fraction relative to the length of the owning beat, e.g. pos
    could be [0-1) for beat of length 1.
    General use-cases per event are duration, note value and volume. The class
    allows these as optional public values
    """

    def __init__(self, pos: float, volume=None, note=None, duration=None):
        self.pos = pos

        if volume and not isinstance(volume, (int, float)):
            raise EventAttributeException(f'Expecting float for volume, not {type(volume)}')

        if note and type(note) is not str:
            raise EventAttributeException(f'Expecting string for note, not {type(note)}')

        if duration and not isinstance(duration, (int, float)):
            raise EventAttributeException(f'Expecting float for duration, not {type(duration)}')

        self.volume = float(volume) if volume else None
        self.note = note
        self.duration = float(duration) if duration else None

    def clone_at(self, pos: float):
        """
        Return a new instance of this event at the new position
        :param pos: position fraction of new event
        :return: a clone of self with changed position and copied attributes
        """
        clone = Event(pos)
        clone.duration = self.duration
        clone.note = self.note
        clone.volume = self.volume
        return clone
