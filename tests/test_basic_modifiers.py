import pytest

from conftest import MotifSplitRate
import deltabeat as dbt


@pytest.mark.parametrize("repeats", [1, 2, 3])
def test_modifier_repeat(arpeggio_events, repeats):
    a = dbt.MidiSource(events=arpeggio_events)
    b = dbt.Repeat(a, repeats)

    assert b.count() == a.count() * repeats
    assert b.duration() == a.duration() * repeats

    expected_pos = [a.pos(i % a.count()) + a.duration() * (i // a.count()) for i in range(b.count())]
    assert [b.pos(i) for i in range(b.count())] == expected_pos
    assert [b.data(i) for i in range(b.count())] == [a.data(i % a.count()) for i in range(b.count())]


def test_modifier_repeat_rate():
    a = MotifSplitRate()
    b = dbt.Repeat(a, 2)

    assert b.count() == a.count() * 2
    assert b.duration() == a.duration() * 2

    # Positions offset whilst each repeat's data is the same
    assert [b.pos(i + 4) for i in range(4)] == [b.pos(i) + a.duration() for i in range(4)]
    assert [b.data(i + 4) for i in range(4)] == [b.data(i) for i in range(4)]

    # Rates preserved in repeats
    assert [b.rate(b.pos(i + 4)) for i in range(4)] == [b.rate(b.pos(i)) for i in range(4)]


@pytest.mark.parametrize("scale", [1, 2, 3])
def test_modifier_scale_position(scale):
    a = MotifSplitRate()
    b = dbt.ScalePositions(a, scale)

    assert b.count() == a.count()
    assert b.duration() == a.duration() * scale

    # Positions scaled with all data remaining the same
    assert [b.pos(i) for i in range(4)] == [a.pos(i) * scale for i in range(4)]
    assert [b.data(i) for i in range(4)] == [a.data(i) for i in range(4)]

    # Rates preserved after scaling
    assert [b.rate(b.pos(i)) for i in range(4)] == [a.rate(b.pos(i)) for i in range(4)]


@pytest.mark.parametrize("scale", [1, 2, 3])
def test_modifier_scale_rate(scale):
    a = MotifSplitRate()
    b = dbt.ScaleRate(a, scale)

    assert b.count() == a.count()
    assert b.duration() == a.duration() / scale

    # Positions scaled with all data remaining the same
    assert [b.pos(i) for i in range(4)] == [a.pos(i) / scale for i in range(4)]
    assert [b.data(i) for i in range(4)] == [a.data(i) for i in range(4)]

    # Playback rate is scaled
    expected_rate = [a.rate(a.pos(i) / a.duration()) * scale for i in range(4)]
    assert [b.rate(b.pos(i) / b.duration()) for i in range(4)] == expected_rate


def test_modifier_trim_to_lhs():
    a = MotifSplitRate()
    b = dbt.Trim(a, 0, 0.5)

    assert b.count() == 2
    assert b.duration() == 0.5

    # Positions, data and rate is preserved
    assert [b.pos(i) for i in range(2)] == [a.pos(i) for i in range(2)]
    assert [b.data(i) for i in range(2)] == [a.data(i) for i in range(2)]
    assert [b.rate(b.pos(i)) for i in range(2)] == [a.rate(a.pos(i)) for i in range(2)]


def test_modifier_trim_to_rhs():
    a = MotifSplitRate()
    b = dbt.Trim(a, 0.5, 0.75)

    assert b.count() == 2
    assert b.duration() == 0.25

    # Positions, data and rate is preserved
    assert [b.pos(i) for i in range(2)] == [a.pos(i + 2) - 0.5 for i in range(2)]
    assert [b.data(i) for i in range(2)] == [a.data(i + 2) for i in range(2)]
    assert [b.rate(b.pos(i)) for i in range(2)] == [a.rate(a.pos(i + 2)) for i in range(2)]
