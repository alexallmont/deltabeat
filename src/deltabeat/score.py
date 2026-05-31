from typing import List

from .motif import Motif, MotifType


class Track(Motif):
    """
    `Track` is a lane of motifs in composition, allowing placement of
    references to motifs at arbitrary start positions.

    FIXME work in progress, still shaping API
    """

    def __init__(self, motif_type: MotifType):
        super().__init__()
        self._motif_type = motif_type
        self._motifs: List = []

    def type(self) -> MotifType:
        return self._motif_type

    def count(self) -> int:
        return 0  # FIXME impl

    def pos(self, i: int) -> float:
        return 0  # FIXME impl

    def data(self, i: int) -> tuple:
        return tuple()  # FIXME impl

    def duration(self) -> float:
        return 0  # FIXME impl

    def rate(self, pos) -> float:
        return 1  # FIXME impl

    def insert(self, pos: float, motif: Motif):
        pass  # FIXME impl


class MidiTrack(Track):
    def __init__(self, name=None):
        super().__init__()
        self.name = name

    def type(self) -> MotifType:
        return MotifType.MIDI


class Score:
    def __init__(self):
        self.tracks = []
        self.master_tempo = 120
        self.master_sample_rate = 44100

    def add_midi_track(self, name=None):
        self.tracks.append(MidiTrack(name))

    def render_midi(self):
        pass  # FIXME impl

    def render_audio(self):
        pass  # FIXME impl
