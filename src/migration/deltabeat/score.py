from .motif import Motif, MotifType


#FIXME
class Track(Motif):
  def __init__(self):
    super().__init__()
    self._motifs = []

  def type(self) -> MotifType: ...

  def count(self) -> int:
    ... # FIXME return self.motif.count()

  def pos(self, i: int):
    ... # FIXME return self.motif.pos(i)

  def data(self, i: int):
    ... # FIXME return self.motif.data(i)

  def duration(self) -> float:
    ... # FIXME return self.motif.duration()

  def rate(self, pos):
    ... # FIXME return super().rate(pos)

  def insert(self, pos: float, motif: Motif):
    ... # FIXME self._motifs.append((pos, motif))


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

  def render_midi():
    ...

  def render_audio():
    ...
