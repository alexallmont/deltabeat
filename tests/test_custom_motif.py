from deltabeat.lib.custom_motif import CustomMotif
from deltabeat.core.make_events import make_atomic_events


def test_empty_motif():
    empty = CustomMotif([], 1)
    assert empty.length() == 1
    assert len(empty.events()) == 0


def test_custom_motif():
    motif = CustomMotif(make_atomic_events([0, .25, .5, .75]), 1)
    assert motif.length() == 1
    assert len(motif.events()) == 4
    assert motif.events()[0].pos == 0
    assert motif.events()[1].pos == .25
    assert motif.events()[2].pos == .5
    assert motif.events()[3].pos == .75
