import pytest

from deltabeat.core.motif import InvalidMotifException
from deltabeat.core.make_events import make_atomic_events
from deltabeat.lib.custom_motif import CustomMotif
from deltabeat.lib.pitch_motif import PitchMotif


def test_empty_motif():
    with pytest.raises(InvalidMotifException):
        PitchMotif(None, 1, 1, 1)

    with pytest.raises(InvalidMotifException):
        PitchMotif([], 1, 1, 1)

    empty = PitchMotif(CustomMotif([], 1), 2, .5, 1.5)
    assert empty.length() == 2
    assert len(empty.events()) == 0
    assert empty.from_scale == .5
    assert empty.to_scale == 1.5


def test_pitch_motif():
    motif = CustomMotif(make_atomic_events([i / 32 for i in range(32)]), 1)
    pitch = PitchMotif(motif, 2, 1, 2)

    assert pitch.length() == 2
    assert len(pitch.events()) == 32

    # FIXME add more rigorous testing to ensure tempo is well matched
    last_pos = 0
    for event in pitch.events():
        assert event.pos >= last_pos
        assert event.pos < pitch.length()
        last_pos = event.pos
