from deltabeat.core.make_events import make_atomic_events
from deltabeat.core.make_events import make_volume_events


def test_make_atomic():
    empty = make_atomic_events([])
    assert len(empty) == 0

    events = make_atomic_events([0, .5])
    assert len(events) == 2
    assert events[0].pos == 0
    assert events[0].volume is None
    assert events[0].duration is None
    assert events[0].note is None
    assert events[1].pos == .5


def test_make_volume():
    empty = make_volume_events([])
    assert len(empty) == 0

    events = make_volume_events([(.1, .2), (.9, .4)])
    assert len(events) == 2
    assert events[0].pos == .1
    assert events[0].volume == .2
    assert events[0].duration is None
    assert events[0].note is None
    assert events[1].pos == .9
    assert events[1].volume == .4
    assert events[1].duration is None
    assert events[1].note is None
