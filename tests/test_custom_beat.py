from deltabeat.lib.custom_beat import CustomBeat


def test_beat_length():
    empty = CustomBeat([], 1)
    assert empty.length() == 1
    assert len(empty.events()) == 0
