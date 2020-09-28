import pytest

from deltabeat.core.beat import InvalidBeatException
from deltabeat.lib.custom_beat import CustomBeat
from deltabeat.lib.repeat_beat import RepeatBeat


def test_empty_beat():
    with pytest.raises(InvalidBeatException):
        RepeatBeat(None, 1)

    with pytest.raises(InvalidBeatException):
        RepeatBeat([], 1)

    empty = RepeatBeat(CustomBeat([], 1), 1)
    assert empty.length() == 1
    assert len(empty.events()) == 0
