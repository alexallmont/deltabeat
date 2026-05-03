from typing import List
from .event import Event


class InvalidMotifException(Exception):
    """
    Report cases where a motif is expected but a different type was passed.
    """


class Motif:
    """
    Abstract base class for types of motifs. See /lib for concrete implementations.
    A derived motif must implement length and events. The 'length' of a motif is
    how long it plays for relative to a global tempo/length pair.
    Events returns a list of events that this motif produces, and is left entirely
    to the derived class to implement. For example, a list of events specified in
    the constructor, or a transformation on existing motifs.
    """

    def length(self) -> float:
        """
        The length of this implementation of motif. This is a fractional measure
        dependant on the global tempo/length pair, most often set to 1.
        :return: the length of this motif relative to global tempo/length pair
        """
        raise Exception(f'Motif::length not implemented for {self}')

    def events(self) -> List[Event]:
        """
        Return a list of events provided by this motif. Events may be user-specified
        or a transformation of existing motifs, depending the derived implementation.
        Each event's pos attribute should be in the half-open interval [0-length)
        :return:
        """
        raise Exception(f'Motif::events not implemented for {self}')
