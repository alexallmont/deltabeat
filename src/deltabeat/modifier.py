import numpy as np

from .motif import Motif, MotifType


class Modifier(Motif):
    """
    Motif modifier that transforms an underlying motif

    Modifiers are intended to be layered akin to image processing
    software to build up parts of a score. For example, a `Repeat`
    modifier will repeat its input motif *n* times, so it has *n*
    times more events, is *n* times longer and has *n* times more
    events.

    These can be combined to procedurally generate scores or to
    alter the timing of playback, for example for time warping of
    events.
    """

    def __init__(self, motif: Motif):
        self._motif = motif

    def type(self) -> MotifType:
        return self._motif.type()

    def count(self) -> int:
        return self._motif.count()

    def pos(self, i: int):
        return self._motif.pos(i)

    def data(self, i: int):
        return self._motif.data(i)

    def duration(self) -> float:
        return self._motif.duration()

    def rate(self, u: float):
        return self._motif.rate(u)


class Repeat(Modifier):
    """
    Repeat the input motif `repeat` times
    """

    def __init__(self, motif: Motif, repeat: int):
        super().__init__(motif)
        self._repeat = repeat

    def count(self) -> int:
        return self._motif.count() * self._repeat

    def pos(self, i: int):
        wrap = self._motif.count()
        return self._motif.pos(i % wrap) + (i // wrap) * self._motif.duration()

    def data(self, i: int):
        return self._motif.data(i % self._motif.count())

    def duration(self) -> float:
        return self._motif.duration() * self._repeat

    def rate(self, u: float):
        if self._motif.duration() == 0:
            return self._motif.rate(u)
        return self._motif.rate(u % self._motif.duration())


class ScalePositions(Modifier):
    """
    Scale input motif so events are stretched out

    `ScalePositions` preserves the playback rate of the underlying
    motif, but moves the notes to different relative positions.

    For example, if the input motif of duration 2 is playing at 120 BPM
    and `scale` is set to 3, then the output of this modifier is still
    playing at 120 BPM, but output duration is 6 and the positions of
    the events are scaled accordingly.
    """

    def __init__(self, motif: Motif, scale: float):
        super().__init__(motif)
        self._scale = scale
        self.factor = scale

    def pos(self, i: int):
        return self._motif.pos(i) * self._scale

    def duration(self) -> float:
        return self._motif.duration() * self._scale


class ScaleRate(Modifier):
    """
    Scale the playback rate of a motif

    `ScaleRate` changes the relative playback rate of the underlying
    motif.

    This is subtly different to `ScalePositions` which retains the
    relative tempo. Instead, scaling the rate is altering the tempo
    directly.

    For example, if the input motif of duration 6 is playing at 60 BPM
    and the scaling rate is 2, then the output motif is playing twice
    as fast so the duration will be 3 and positions scaled accordingly,
    but also the motif is playing at 120 BPM.
    """

    def __init__(self, motif: Motif, scale: float):
        super().__init__(motif)
        self._scale = scale
        self.factor = scale

    def duration(self) -> float:
        return self._motif.duration() / self._scale

    def pos(self, i: int):
        return self._motif.pos(i) / self._scale

    def rate(self, u: float):
        return self._motif.rate(u) * self._scale


class Trim(Modifier):
    """
    Trim an input motif to a different range

    Use a section of an underlying motif to generate a new motif. For
    example, if an input motif has duration 4 and consists of events
    every 0.25 (effectively 4 bars of beats every quarter note) and
    trim applies to `start` 1 and `end` 4, then the result has duration
    3 preserving the events in that range (effectively 3 bars of beats
    every quarter note).

    Note that this modifier copies events upon construction, so
    presently cannot be applied to dynamic underlying motifs.
    """

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
        return self._motif.pos(i + self._start_i) - self._start

    def data(self, i: int):
        return self._motif.data(i + self._start_i)

    def duration(self) -> float:
        return self._end - self._start

    def rate(self, u: float):
        return self._motif.rate(u + self._start)


class Quantize(Modifier):
    """
    FIXME pull events towards quantise points
    """

    pass


class Swing(Modifier):
    """
    FIXME pull events towards classic swing percent pattern
    """

    pass


class RateWarp(Modifier):
    """
    Warp an existing motif to shift between two speeds over a certain length. This is
    comparable to how a DJ touches or jogs vinyl to beat-match two rhythms and can be
    used to generate complex phased rhythms or to match up rhythms that are out of
    phase.

    For smooth pitching, from_scale should match the speed of the existing motif
    passed in, and to_scale should match the speed of the next motif to be played.
    In order to fit the number of motifs over the full length, the curve computed to
    match pitch may have to slow down the motif even though the final speed is faster.

    Degenerate cases are possible when trying to pitch excessively. For example,
    if trying to pitch between two very fast motifs in a space that is too small.
    In these instances the curve may take on an 'N' shape causing the next event in
    a motif to have a position before its predecessor. This is under review because
    it will cause the output to temporarily reverse, so events go out of order causing
    playback artefacts
    """

    def __init__(self, motif: Motif, duration: float, from_rate: float, to_rate: float):
        """
        Pitch a motif to scale between two speeds in a given length
        :param motif: existing motif to pitch
        :param length: fractional length to scale over
        :param from_scale: fractional relative speed of existing motif
        :param to_scale: fractional relative speed of motif to pitch to
        """
        super().__init__(motif)
        self._duration = duration
        self.len = duration
        self.from_rate = from_rate
        self.to_rate = to_rate
        self.from_scale = from_rate
        self.to_scale = to_rate
        self._coefficients = self._curve_coefficients()

    def duration(self):
        return self._duration

    def pos(self, i: int):
        return self._warp(self._motif.pos(i))

    def rate(self, u: float):
        return self._motif.rate(u) * self._warp_derivative(u)

    def _curve_coefficients(self):
        # Generate a curve that transforms the events to pitch the given range.
        # The curve computation is derived from five constraints, where fl and tl
        # are the 'from length' and 'to length' and fs and ts are the 'from scale' and
        # 'to scale' (scale being a relative measure of speed, or tempo):
        #   1. f(0)   = 0            - an input motif at 0 maps to an output motif at 0
        #   2. f(fl)  = tl           - likewise for motifs at end
        #   3. f'(0)  = fs           - tempo at 0 maps to requested scale
        #   4. f'(fl) = ts           - likewise for tempo at end
        #   5. g(fl) = fl * tl / 2   - ensure time is preserved
        #
        # f(x) is the mapping of positions, and f'(x) is the mapping of scale.
        # The last function g(x) is the integral of f between 0 and fl, i.e., the area
        # under the curve so the value over the domain [0,ft). For the motifs to line up,
        # the area under the curve must be exactly the same as a linear scaling, which
        # is just a line with a triangular area underneath of fl * tl / 2.
        #
        # The constrains require a quartic function as there can be up to 3 inflexions
        # in speed: 2 to go faster or slower at the start and the end, and; one more to
        # 'draw out' the motif in the middle to ensure the rhythm plays out the full
        # range of motifs, i.e. to fulfil the constraint 5 on g(x).
        #
        # Constraints 1 and 3 above give parameters a and b of the quartic. The other
        # coefficients are solved as a matrix derived from the system equations of
        # f(x), it's derivative f'(x), and sum g(x), along with constraints 2, 4 and 5.
        fl = self._motif.duration()
        tl = self._duration
        fs = self.from_rate
        ts = self.to_rate

        if fl == 0:
            self._coefficients = (0, fs, 0, 0, 0)
            return self._coefficients

        eqs = np.array(
            [
                [fl**2, fl**3, fl**4],
                [2 * fl, 3 * fl**2, 4 * fl**3],
                [fl**3 / 3, fl**4 / 4, fl**5 / 5],
            ]
        )
        sums = np.array(
            [
                tl - fs * fl,
                ts - fs,
                fl * tl / 2 - fs * fl**2 / 2,
            ]
        )
        c, d, e = np.linalg.solve(eqs, sums)
        return (0, fs, c, d, e)

    def _warp(self, x: float):
        a, b, c, d, e = self._coefficients
        return a + b * x + c * x**2 + d * x**3 + e * x**4

    def _warp_derivative(self, x: float):
        _, b, c, d, e = self._coefficients
        return b + 2 * c * x + 3 * d * x**2 + 4 * e * x**3
