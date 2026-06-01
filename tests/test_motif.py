from conftest import MotifRepeatN
import pytest

import deltabeat as dbt


def test_motif_chain():
    a = MotifRepeatN(1, 7, 2) # e.g. 1 event over 7 duration at rate 2
    b = MotifRepeatN(2, 3, 4)
    c = MotifRepeatN(3, 5, 8)
    m = dbt.MotifChain(a, b, c)

    assert m.count() == 6
    assert m.duration() == 15

    # Check chain motif start positions
    assert m.pos(0) == 0
    assert m.pos(1) == 7
    assert m.pos(3) == 10

    # Checks intermediary positions
    assert m.pos(2) == 7 + 3 / 2  # second motif is 3 long split into 2 events
    assert m.pos(4) == 10 + 5 / 3  # fourth motif is 5 long split into 3 events
    assert m.pos(5) == 10 + 2 * 5 / 3  # .. * 2 for next event

    # Check that internals get right mofif at frac position
    motifs_at_frac = [m._motif_at_frac(i / 15)[0] for i in range(15)]
    assert all(motifs_at_frac[i] == a for i in range(7))
    assert all(motifs_at_frac[i] == b for i in range(7, 10))
    assert all(motifs_at_frac[i] == c for i in range(10, 15))

    # Check that internals get right relative position given overall frac position
    relative_u_at_frac = [m._motif_at_frac(i / 15)[1] for i in range(15)]
    assert relative_u_at_frac[:7] == pytest.approx([i / 7 for i in range(7)])
    assert relative_u_at_frac[7:10] == pytest.approx([i / 3 for i in range(3)])
    assert relative_u_at_frac[10:15] == pytest.approx([i / 5 for i in range(5)])

    # Check the rates are correct for each motif in chain given overall frac position
    rate_at_frac = [m.rate(i / 15) for i in range(15)]
    assert rate_at_frac[:7] == [2] * 7
    assert rate_at_frac[7:10] == [4] * 3
    assert rate_at_frac[10:15] == [8] * 5
