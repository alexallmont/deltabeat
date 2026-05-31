import pytest
from typing import Any

import deltabeat as dbt
from deltabeat.midi import name_to_index, note_on, note_off
from deltabeat.midi_const import NOTE_MIDI_CENTRE


@pytest.fixture
def arpeggio_events():
    notes = [name_to_index(n) for n in ["C4", "E4", "G4", "F4"]]
    events = []
    for i, note in enumerate(notes):
        events.append((i / len(notes), *note_on(0, note, 127)))
        events.append(((i + 1) / len(notes), *note_off(0, note, 127)))
    return events


def expected_arpeggio_events():
    midi_commands = [144, 128]
    midi_note_ids = [60, 64, 67, 65]
    pos = [x for i in range(4) for x in (i / 4, (i + 1) / 4)]
    data = [(cmd, midi_note_ids[i], 127) for i in range(4) for cmd in midi_commands]
    return pos, data


class MotifSplitRate(dbt.Motif):
    def count(self) -> int:
        return 4

    def pos(self, i: int) -> float:
        if i < 2:
            return i / 4
        else:
            return 0.5 + (i - 2) / 8

    def data(self, i: int) -> Any:
        # Just MIDI "on" commands channel 0; no "off" in basic tests
        return (144, NOTE_MIDI_CENTRE + i, 127)

    def duration(self) -> float:
        return 0.75

    def rate(self, u: float) -> float:
        if u < 0.5:
            return 1
        else:
            return 2
