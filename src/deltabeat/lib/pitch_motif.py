from typing import List
import numpy as np
import deltabeat as dbt


class PitchMotif(dbt.Motif):
    """
    Pitch an existing motif to shift between two speeds over a certain length. This is
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
    a motif to have a position before its predecessor. This will cause the output to
    temporarily reverse, so events go out of order.
    """

    def __init__(self, motif: dbt.Motif, length: float, from_scale: float, to_scale: float):
        """
        Pitch a motif to scale between two speeds in a given length
        :param motif: existing motif to pitch
        :param length: fractional length to scale over
        :param from_scale: fractional relative speed of existing motif
        :param to_scale: fractional relative speed of motif to pitch to
        """
        if not issubclass(type(motif), dbt.Motif):
            raise dbt.InvalidMotifException(f'Invalid type {type(motif)} for PitchMotif')

        self.motif = motif
        self.len = length
        self.from_scale = from_scale
        self.to_scale = to_scale

    def length(self):
        return self.len

    def events(self) -> List[dbt.Event]:
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
        #
        fl = self.motif.length()
        tl = self.len
        fs = self.from_scale
        ts = self.to_scale
        eqs = np.array([[fl**2, fl**3, fl**4], [2*fl, 3*fl**2, 4*fl**3], [fl**3/3, fl**4/4, fl**5/5]])
        sums = np.array([tl - fs*fl, ts - fs, fl*tl/2 - fs*fl**2/2])
        # FIXME raise exception for degenerate curves with no valid determinant.
        coefficients = np.linalg.solve(eqs, sums)

        # Generate the polynomial f(x) from the calculation.
        a = 0
        b = fs
        c = coefficients[0]
        d = coefficients[1]
        e = coefficients[2]

        def f(x):
            return a + b * x + c * x**2 + d * x**3 + e * x**4

        result = []
        for ev in self.motif.events():
            result.append(ev.clone_at(f(ev.pos)))
        return result
