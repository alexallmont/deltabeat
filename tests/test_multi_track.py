import deltabeat as dbt


def test_track():
    mt = dbt.MultiTrack()
    assert mt.num_tracks() == 0

    mt.add_track('foo')
    assert mt.num_tracks() == 1
    assert mt.tracks[0].name == 'foo'

    mt.add_track('bar')
    assert mt.num_tracks() == 2
    assert mt.tracks[1].name == 'bar'
