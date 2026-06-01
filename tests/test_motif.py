from conftest import MotifRepeatN
import deltabeat as dbt


def test_motif_chain():
    a = MotifRepeatN(1, 7)
    b = MotifRepeatN(2, 3)
    c = MotifRepeatN(3, 5)
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

    assert m._motif_at_frac(0) == (a, 0)
    assert m._motif_at_frac(1 / 15) == (a, 1/7)
    assert m._motif_at_frac(2 / 15) == (a, 2/7)
    assert m._motif_at_frac(3 / 15) == (a, 3/7)
    assert m._motif_at_frac(4 / 15) == (a, 4/7)
    assert m._motif_at_frac(5 / 15) == (a, 5/7)
    assert m._motif_at_frac(6 / 15) == (a, 6/7)
    assert m._motif_at_frac(7 / 15) == (b, 0)
    assert m._motif_at_frac(8 / 15) == (b, 1/3)
    assert m._motif_at_frac(9 / 15) == (b, 2/3)
    assert m._motif_at_frac(10 / 15) == (c, 0)
    assert m._motif_at_frac(11 / 15) == (c, 1/5)
    assert m._motif_at_frac(12 / 15) == (c, 2/5)
    assert m._motif_at_frac(13 / 15) == (c, 3/5)
    assert m._motif_at_frac(14 / 15) == (c, 4/5)
