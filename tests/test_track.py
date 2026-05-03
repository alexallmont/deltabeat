import deltabeat as dbt
from pytest import approx


def test_track():
    track = dbt.Track('foo')
    assert track.name == 'foo'

    track.add_motif(dbt.CustomMotif(dbt.make_atomic_events([0, .3]), 1))
    assert track.length() == 1
    assert len(track.events()) == 2

    track.add_motif(dbt.CustomMotif(dbt.make_atomic_events([0, 1.2, 1.7]), 2))
    assert track.length() == 3
    assert len(track.events()) == 5

    assert track.events()[0].pos == 0
    assert track.events()[1].pos == .3
    assert track.events()[2].pos == approx(1)
    assert track.events()[3].pos == approx(2.2)
    assert track.events()[4].pos == approx(2.7)
