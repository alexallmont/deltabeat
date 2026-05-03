from pytest import approx
from deltabeat.core.make_events import make_atomic_events
from deltabeat.core.track import Track
from deltabeat.lib.custom_motif import CustomMotif


def test_track():
    track = Track('foo')
    assert track.name == 'foo'

    track.add_motif(CustomMotif(make_atomic_events([0, .3]), 1))
    assert track.length() == 1
    assert len(track.events()) == 2

    track.add_motif(CustomMotif(make_atomic_events([0, 1.2, 1.7]), 2))
    assert track.length() == 3
    assert len(track.events()) == 5

    assert track.events()[0].pos == 0
    assert track.events()[1].pos == .3
    assert track.events()[2].pos == approx(1)
    assert track.events()[3].pos == approx(2.2)
    assert track.events()[4].pos == approx(2.7)
