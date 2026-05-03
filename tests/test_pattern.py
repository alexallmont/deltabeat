import deltabeat as dbt
import pytest
from pytest import approx


def test_empty_motif():
    with pytest.raises(dbt.InvalidMotifException):
        dbt.Pattern(None)

    with pytest.raises(dbt.InvalidMotifException):
        # Should be list of motifs, not an instance
        dbt.Pattern(dbt.CustomMotif([], 1))

    empty = dbt.Pattern([dbt.CustomMotif([], 1), dbt.CustomMotif([], 2)])
    assert empty.length() == approx(3)
    assert len(empty.events()) == 0


def test_pattern():
    pattern = dbt.Pattern([
        dbt.CustomMotif(dbt.make_atomic_events([0, 0.1, 0.5]), 1),
        dbt.CustomMotif(dbt.make_atomic_events([0.2, 0.3]), 0.5),
        dbt.CustomMotif(dbt.make_atomic_events([0, 0.6]), 1)
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
