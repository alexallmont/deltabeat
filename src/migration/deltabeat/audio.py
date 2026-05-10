from .core import Motif, MotifType, Source


class AudioSource(Source):
  """
  """
  def __init__(self):
    ...

  def type(self) -> MotifType:
    return MotifType.AUDIO

  def count(self) -> int:
    ...

  def pos(self, i: int):
    ...

  def data(self, i: int):
    ...

  def duration(self) -> float:
    ...
