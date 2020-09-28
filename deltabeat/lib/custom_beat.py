from typing import List
import deltabeat.core as db


class CustomBeat(db.Beat):
    """
    Create a beat from a user-specified list of events and length.
    See core/make_events.py for convenient event list creation functions.
    """

    def __init__(self, event_list: List[db.Event], length: float = 1):
        """
        Create a beat from a list of events to play in given length.
        :param event_list: list of events with pos in range [0-length)
        :param length: length of this beat in relation to global tempo/length pair
        """
        self.event_list = event_list
        self.len = length

    def length(self) -> float:
        return self.len

    def events(self) -> List[db.Event]:
        return self.event_list
