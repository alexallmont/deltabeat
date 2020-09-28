import pytest
from pytest import approx

from deltabeat.core.beat import InvalidBeatException
from deltabeat.core.make_events import make_atomic_events
from deltabeat.lib.custom_beat import CustomBeat
from deltabeat.lib.scale_beat import ScaleBeat


def test_empty_beat():
    with pytest.raises(InvalidBeatException):
        ScaleBeat(None, 1)

    with pytest.raises(InvalidBeatException):
        ScaleBeat([], 1)

    empty = ScaleBeat(CustomBeat([], 1.4), 1.6)
    assert empty.length() == approx(1.4 * 1.6)
    assert len(empty.events()) == 0


def test_scale_beat():
    motif = CustomBeat(make_atomic_events([i / 4 for i in range(4)]), 1)
    scale = ScaleBeat(motif, 2.5)

    assert scale.length() == 2.5
    assert len(scale.events()) == 4

    assert scale.events()[0].pos == approx(0)
    assert scale.events()[1].pos == approx(.625)
    assert scale.events()[2].pos == approx(1.25)
    assert scale.events()[3].pos == approx(1.875)
