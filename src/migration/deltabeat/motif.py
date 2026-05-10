from enum import Enum


class MotifType(Enum):
  """
  """
  MIDI = 1
  AUDIO = 3


class Motif:
  """
  """
  def type(self) -> MotifType: ...
  def count(self) -> int: ...
  def pos(self, i: int): ...
  def data(self, i: int): ...
  def duration(self) -> float: ...
  def rate(self, pos: float): ...

  def __str__(self):
    exprs = []
    for i in range(self.count()):
      exprs.append(f"{self.pos(i)}: {self.data(i)}")
    return ", ".join(exprs)


class Source(Motif):
  """
  """
  def rate(self, pos):
    return 1.0

