import pytest

from conftest import expected_arpeggio_events, MotifRepeatN


def test_conftest_arpeggio_events(arpeggio_events):
    pos = [event[0] for event in arpeggio_events]
    data = [event[1:] for event in arpeggio_events]
    exp_pos, exp_data = expected_arpeggio_events()
    assert pos == exp_pos
    assert data == exp_data


@pytest.mark.parametrize("count", [1, 3, 4])
@pytest.mark.parametrize("duration", [1, 2])
def test_motif_repeat_n(count, duration):
    m = MotifRepeatN(count, duration)
    assert m.count() == count
    assert m.duration() == duration
    assert [m.pos(i) for i in range(count)] == [i * duration / count for i in range(count)]


def test_motif_split_rate():
    # FIXME impl
    pass