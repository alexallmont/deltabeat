from .beat import Beat
from .pattern import Pattern


class Track(Pattern):
    """
    A track is a named beat pattern, to which beats may be dynamically added.
    """

    def __init__(self, name: str):
        """
        Create a new track for dynamically maintaining beats
        :param name: track name used in multitrack
        """
        super().__init__([])
        self.name = name

    def add_beat(self, beat: Beat):
        self.beats.append(beat)
