from typing import List
from ..core.beat import Beat
from ..core.beat import Event


class CustomBeat(Beat):
    """
    Create a beat from a user-specified list of events and length.
    See core/make_beats.py for convenient event list creation functions.
    """

    def __init__(self, event_list: List[Event], length: float = 1):
        self.event_list = event_list
        self.len = length

    def length(self) -> float:
        return self.len

    def events(self) -> List[Event]:
        return self.event_list
