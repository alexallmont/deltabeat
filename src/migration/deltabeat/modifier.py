from .core import Motif, MotifType


class Modifier(Motif):
  def __init__(self, motif: Motif):
    self._motif = motif

  def type(self) -> MotifType:
    return self._motif.type()

  def count(self) -> int:
    return self.motif.count()

  def pos(self, i: int):
    return self.motif.pos(i)

  def data(self, i: int):
    return self.motif.data(i)

  def duration(self) -> float:
    return self.motif.duration()

  def rate(self, pos):
    return super().rate(pos)


class Repeat(Modifier):
  def __init__(self, motif: Motif, repeat: int):
    super().__init__(motif)
    self._repeat = repeat

  def count(self) -> int:
    return self.motif.count() * self._repeat

  def pos(self, i: int):
    wrap = self.motif.count()
    return self.motif.pos(i % wrap) + (i // wrap) * self.motif.duration()

  def data(self, i: int):
    return self.motif.data(i % self.motif.count())

  def duration(self) -> float:
    return self.motif.duration() * self._repeat


class ScalePositions(Modifier):
  def __init__(self, motif: Motif, scale: float):
    super().__init__(motif)
    self._scale = scale

  def pos(self, i: int):
    return self.motif.pos(i) * self._scale

  def duration(self) -> float:
    return self.motif.duration() * self._scale


class ScaleRate(Modifier):
  def __init__(self, motif: Motif, scale: float):
    super().__init__(motif)
    self._scale = scale

  def duration(self) -> float:
    return self.motif.duration() / self._scale

  def rate(self, pos: float):
    return self.motif.rate(pos) * self._scale


class Trim(Modifier):
  def __init__(self, motif: Motif, start: float, end: float):
    super().__init__(motif)
    self._start = start
    self._end = end
    self._start_i = 0
    self._count = 0
    self.update()

  def update(self):
    m = self._motif
    self._start_i = next(i for i in range(m.count()) if m.pos(i) >= self._start)
    self._count = sum(1 for i in range(m.count()) if m.pos(i) >= self._start and m.pos(i) < self._end)

  def count(self):
    return self._count

  def pos(self, i: int):
    return self.motif.pos(i - self._start_i)

  def data(self, i: int):
    return self.motif.data(i - self._start_i)

  def duration(self) -> float:
    return self._end - self._start

  def rate(self, pos: float):
    # FIXME review adjusted rate input
    return self.motif.rate(pos - self._start)


class LeftAlign(Modifier):
  def __init__(self, motif: Motif, range: float):
    super().__init__(motif)
    self._duration = range
    # FIXME does not respect dependency changes
    self._count = sum(1 for i in motif.count() if motif.pos(i) < range)

  def count(self):
    return self._count

  def duration(self) -> float:
    return self._duration

  def rate(self, pos: float):
    pos = min(pos, self._motif.duration())
    return self.motif.rate(pos)


class Quantize(Modifier):
  ...


class Swing(Modifier):
  ...


class RateWarp(Modifier):
  ...
