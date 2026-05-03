from typing import List
import deltabeat as dbt


class CustomMotif(dbt.Motif):
    """
    Create a motif from a user-specified list of events and length.
    See core/make_events.py for convenient event list creation functions.
    """

    def __init__(self, event_list: List[dbt.Event], length: float = 1):
        """
        Create a motif from a list of events to play in given length.
        :param event_list: list of events with pos in range [0-length)
        :param length: length of this motif in relation to global tempo/length pair
        """
        self.event_list = event_list
        self.len = length

    def length(self) -> float:
        return self.len

    def events(self) -> List[dbt.Event]:
        return self.event_list
