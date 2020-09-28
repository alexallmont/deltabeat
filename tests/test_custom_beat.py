from deltabeat.lib.custom_beat import CustomBeat
from deltabeat.core.make_events import make_atomic_events


def test_empty_beat():
    empty = CustomBeat([], 1)
    assert empty.length() == 1
    assert len(empty.events()) == 0


def test_custom_beat():
    beat = CustomBeat(make_atomic_events([0, .25, .5, .75]), 1)
    assert beat.length() == 1
    assert len(beat.events()) == 4
    assert beat.events()[0].pos == 0
    assert beat.events()[1].pos == 0.25
    assert beat.events()[2].pos == 0.5
    assert beat.events()[3].pos == 0.75
