from .motif import Motif, MotifType, Source
from .modifier import Modifier


class MidiSource(Source):
  """
  """
  def __init__(self, duration: float=0, events: list=[]):
    self._duration = duration
    self._events = events

  def type(self) -> MotifType:
    return MotifType.MIDI

  def count(self) -> int:
    return len(self._events)

  def pos(self, i: int):
    return self._events[i][0]

  def data(self, i: int):
    return self._events[i][1:]

  def duration(self) -> float:
    return self._duration


class MidiEdit(MidiSource):
  """
  """
  def __init__(self, range: float):
    super().__init__(range)
    self._notes = []

  def add_note(self, pos, channel, note, velocity, range):
    self._notes.append((pos, channel, note, velocity, range))
    self._update_events()

  def _update_events(self):
    self._events = []
    for pos, channel, note, velocity, range in self._notes:
      self._events.append((pos, 0x90 | channel, note, velocity))
      self._events.append((pos + range, 0x80 | channel, note, velocity))
    self._events.sort(key=lambda ev: ev[0])


class MidiModifier(Modifier):
  """
  """
  def __init__(self, motif: Motif):
    if motif.type() != MotifType.MIDI:
      raise RuntimeError("Midi modifiers expect MIDI mofif")
    super().__init__(motif)


class MidiChannelFilter(MidiModifier):
  """
  """
  # FIXME
  ...


class MidiNoteSubstibute(MidiModifier):
  """
  """
  # FIXME
  ...


def load_mid_motif(filename: str):
  import mido

  pos = 0
  time_sig_scale = 1
  tempo_scale = 2
  events = []

  for msg in mido.MidiFile(filename):
    pos += msg.time * time_sig_scale * tempo_scale / 4
    if msg.type == "set_tempo":
      tempo_scale = 1000000 / msg.tempo
    elif msg.type == "time_signature":
      time_sig_scale = msg.numerator / msg.denominator
    elif msg.type == "note_on":
      events.append((pos, 0x90 | msg.channel, msg.note, msg.velocity))
    elif msg.type == "note_off":
      events.append((pos, 0x80 | msg.channel, msg.note, msg.velocity))

  return MidiSource(pos, events)
