from conftest import expected_arpeggio_events


def test_conftest_arpeggio_events(arpeggio_events):
    pos = [event[0] for event in arpeggio_events]
    data = [event[1:] for event in arpeggio_events]
    exp_pos, exp_data = expected_arpeggio_events()
    assert pos == exp_pos
    assert data == exp_data
