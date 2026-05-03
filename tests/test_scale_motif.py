import deltabeat as dbt
import pytest
from pytest import approx


def test_empty_motif():
    with pytest.raises(dbt.InvalidMotifException):
        dbt.ScaleMotif(None, 1)

    with pytest.raises(dbt.InvalidMotifException):
        dbt.ScaleMotif([], 1)

    empty = dbt.ScaleMotif(dbt.CustomMotif([], 1.4), 1.6)
    assert empty.length() == approx(1.4 * 1.6)
    assert len(empty.events()) == 0


def test_scale_motif():
    motif = dbt.CustomMotif(dbt.make_atomic_events([i / 4 for i in range(4)]), 1)
    scale = dbt.ScaleMotif(motif, 2.5)

    assert scale.length() == 2.5
    assert len(scale.events()) == 4

    assert scale.events()[0].pos == approx(0)
    assert scale.events()[1].pos == approx(.625)
    assert scale.events()[2].pos == approx(1.25)
    assert scale.events()[3].pos == approx(1.875)
