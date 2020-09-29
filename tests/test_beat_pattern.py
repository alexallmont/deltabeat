import pytest
from pytest import approx

from deltabeat.core.beat import InvalidBeatException
from deltabeat.core.make_events import make_atomic_events
from deltabeat.core.beat_pattern import BeatPattern
from deltabeat.lib.custom_beat import CustomBeat


def test_empty_beat():
    with pytest.raises(InvalidBeatException):
        BeatPattern(None)

    with pytest.raises(InvalidBeatException):
        # Should be list of beats, not an instance
        BeatPattern(CustomBeat([], 1))

    empty = BeatPattern([CustomBeat([], 1), CustomBeat([], 2)])
    assert empty.length() == approx(3)
    assert len(empty.events()) == 0


def test_beat_pattern():
    pattern = BeatPattern([
        CustomBeat(make_atomic_events([0, 0.1, 0.5]), 1),
        CustomBeat(make_atomic_events([0.2, 0.3]), 0.5),
        CustomBeat(make_atomic_events([0, 0.6]), 1)
    ])

    assert pattern.length() == 2.5
    assert len(pattern.events()) == 7

    assert pattern.events()[0].pos == 0
    assert pattern.events()[1].pos == .1
    assert pattern.events()[2].pos == .5
    assert pattern.events()[3].pos == approx(1.2)
    assert pattern.events()[4].pos == approx(1.3)
    assert pattern.events()[5].pos == approx(1.5)
    assert pattern.events()[6].pos == approx(2.1)
