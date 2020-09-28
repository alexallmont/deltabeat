from copy import copy


class Event:
    """
    A class for any type of event in a beat. Events must have a position, which
    is a float fraction relative to the length of the owning beat, e.g. pos
    could be [0-1) for beat of length 1.
    General use-cases per event are duration, note value and volume. The class
    allows these as optional public values
    """

    def __init__(self, pos, duration=None, note=None, volume=None):
        self.pos = pos
        self.duration = duration
        self.note = note
        self.volume = volume

    def clone_at(self, pos: float):
        """
        Return a new instance of this event at the new position
        :param pos: position fraction of new event
        :return: a clone of self with changed position and copied attributes
        """
        clone = Event(pos)
        clone.duration = copy(self.duration)
        clone.note = copy(self.note)
        clone.volume = copy(self.volume)
        return clone
