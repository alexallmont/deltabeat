import pytest
from pytest import approx

from deltabeat.core.beat import InvalidBeatException
from deltabeat.core.make_events import make_volume_events
from deltabeat.lib.custom_beat import CustomBeat
from deltabeat.lib.repeat_beat import RepeatBeat


def test_empty_beat():
    with pytest.raises(InvalidBeatException):
        RepeatBeat(None, 1)

    with pytest.raises(InvalidBeatException):
        RepeatBeat([], 1)

    empty = RepeatBeat(CustomBeat([], 1), 1)
    assert empty.length() == 1
    assert len(empty.events()) == 0


def test_repeat_beat():
    # Test repeat on volume events to check that events have cloned correctly
    motif = CustomBeat(make_volume_events([(0, .6), (.1, .7)]), .4)
    repeat = RepeatBeat(motif, 3)

    assert repeat.length() == approx(1.2)  # 3 * 0.4
    assert len(repeat.events()) == 6

    assert repeat.events()[0].pos == approx(0)
    assert repeat.events()[1].pos == approx(.1)
    assert repeat.events()[2].pos == approx(.4)
    assert repeat.events()[3].pos == approx(.5)
    assert repeat.events()[4].pos == approx(.8)
    assert repeat.events()[5].pos == approx(.9)

    assert repeat.events()[0].volume == .6
    assert repeat.events()[1].volume == .7
    assert repeat.events()[2].volume == .6
    assert repeat.events()[3].volume == .7
    assert repeat.events()[4].volume == .6
    assert repeat.events()[5].volume == .7
