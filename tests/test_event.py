import deltabeat as dbt
import pytest


def test_create_event():
    e = dbt.Event(.2)
    assert e.pos == .2
    assert e.volume is None
    assert e.note is None
    assert e.duration is None

    e = dbt.Event(.5, .1, 'C4', .3)
    assert e.pos == .5
    assert e.volume == .1
    assert e.note == 'C4'
    assert e.duration == .3

    # Check that volume and duration as integers are converted to float
    e = dbt.Event(.5, volume=1, duration=1)
    assert e.volume == 1
    assert type(e.volume) == float
    assert e.duration == 1
    assert type(e.duration) == float


def test_create_bad_attributes():
    with pytest.raises(dbt.EventAttributeException):
        dbt.Event(0, volume='fish')

    with pytest.raises(dbt.EventAttributeException):
        dbt.Event(0, note=5)

    with pytest.raises(dbt.EventAttributeException):
        dbt.Event(0, duration=[1, 2, 3])


def test_clone_event():
    a = dbt.Event(.2, volume=.4, note='D5', duration=.9)
    b = a.clone_at(.4)

    assert a.pos == .2
    assert b.pos == .4
    assert a.volume == b.volume
    assert a.note == b.note
    assert a.duration == b.duration
