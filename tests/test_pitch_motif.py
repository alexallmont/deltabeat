import deltabeat as dbt
import pytest


def test_empty_motif():
    with pytest.raises(dbt.InvalidMotifException):
        dbt.PitchMotif(None, 1, 1, 1)

    with pytest.raises(dbt.InvalidMotifException):
        dbt.PitchMotif([], 1, 1, 1)

    empty = dbt.PitchMotif(dbt.CustomMotif([], 1), 2, .5, 1.5)
    assert empty.length() == 2
    assert len(empty.events()) == 0
    assert empty.from_scale == .5
    assert empty.to_scale == 1.5


def test_pitch_motif():
    motif = dbt.CustomMotif(dbt.make_atomic_events([i / 32 for i in range(32)]), 1)
    pitch = dbt.PitchMotif(motif, 2, 1, 2)

    assert pitch.length() == 2
    assert len(pitch.events()) == 32

    # FIXME add more rigorous testing to ensure tempo is well matched
    last_pos = 0
    for event in pitch.events():
        assert event.pos >= last_pos
        assert event.pos < pitch.length()
        last_pos = event.pos
