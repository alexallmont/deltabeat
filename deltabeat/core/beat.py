from typing import List
from .event import Event


class Beat:
    """
    Abstract base class for types of beats. See /lib for concrete implementations.
    A derived beat must implement length and events. The 'length' of a beat is
    how long it plays for relative to a global tempo/length pair.
    Events returns a list of events that this beat produces, and is left entirely
    to the derived class to implement. For example, a list of events specified in
    the constructor, or a transformation on existing beats.
    """

    def length(self) -> float:
        """
        The length of this implementation of beat. This is a fractional measure
        dependant on the global tempo/length pair, most often set to 1.
        :return: the length of this beat relative to global tempo/length pair
        """
        raise Exception(f'Beat::length not implemented for {self}')

    def events(self) -> List[Event]:
        """
        Return a list of events provided by this beat. Events may be user-specified
        or a transformation of existing beats, depending the derived implementation.
        Each event's pos attribute should be in the half-open interval [0-length)
        :return:
        """
        raise Exception(f'Beat::events not implemented for {self}')
