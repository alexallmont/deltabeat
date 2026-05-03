import deltabeat as dbt
import pytest
from pytest import approx


def test_empty_motif():
    with pytest.raises(dbt.InvalidMotifException):
        dbt.RepeatMotif(None, 1)

    with pytest.raises(dbt.InvalidMotifException):
        dbt.RepeatMotif([], 1)

    empty = dbt.RepeatMotif(dbt.CustomMotif([], 1), 1)
    assert empty.length() == 1
    assert len(empty.events()) == 0


def test_repeat_motif():
    # Test repeat on volume events to check that events have cloned correctly
    motif = dbt.CustomMotif(dbt.make_volume_events([(0, .6), (.1, .7)]), .4)
    repeat = dbt.RepeatMotif(motif, 3)

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
