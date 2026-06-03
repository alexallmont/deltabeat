import pytest

from conftest import expected_arpeggio_events
import deltabeat as dbt
from deltabeat.midi import name_to_index
from deltabeat.midi_const import INDEX_TO_NOTES


def test_midi_name_to_index():
    # Test centre and extremes
    assert name_to_index("C4") == 60
    assert name_to_index("A0") == 21
    assert name_to_index("G9") == 127

    # Demonstrate sharp and flat syntax
    assert name_to_index("F#5") == 78
    assert name_to_index("Bb8") == 118
    assert name_to_index("Gb2") == 42

    # Check outliers
    with pytest.raises(AssertionError):
        name_to_index("Ab0")

    with pytest.raises(AssertionError):
        name_to_index("G#9")

    # Check all possible notes
    for octave in range(10):
        for index in range(12):
            # Must be in range [A0, G9]
            greater_eq_a0 = octave > 1 or index >= 9
            less_eq_g9 = octave < 9 or index <= 7
            if greater_eq_a0 and less_eq_g9:
                relative_octave = octave - 4  # start from e.g C4 not C0
                expected_index = 60 + (12 * relative_octave) + index

                note_or_sharp = f"{INDEX_TO_NOTES[index][0]}{octave}"
                assert name_to_index(note_or_sharp) == expected_index

                note_or_flat = f"{INDEX_TO_NOTES[index][-1]}{octave}"
                assert name_to_index(note_or_flat) == expected_index


@pytest.mark.parametrize("duration, expected_duration", [(None, 0), (1, 1)])
def test_midi_source_empty(duration, expected_duration):
    ms = dbt.MidiSource(duration=duration)
    assert ms.type() == dbt.MotifType.MIDI
    assert ms.count() == 0
    assert ms.duration() == expected_duration
    assert ms.rate(0) == 1.0
    assert ms.rate(1) == 1.0


@pytest.mark.parametrize("duration, expected_duration", [(None, 1), (2, 2)])
def test_midi_source_from_events(duration, expected_duration, arpeggio_events):
    ms = dbt.MidiSource(duration=duration, events=arpeggio_events)
    assert ms.type() == dbt.MotifType.MIDI
    assert ms.count() == 8
    assert ms.duration() == expected_duration
    assert ms.rate(0) == 1.0
    assert ms.rate(1) == 1.0

    exp_pos, exp_data = expected_arpeggio_events()
    assert [ms.pos(i) for i in range(8)] == exp_pos
    assert [ms.data(i) for i in range(8)] == exp_data
