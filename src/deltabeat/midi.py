from typing import List

from .modifier import Modifier
from .motif import Motif, MotifType, Source
from . import midi_const


class MidiSource(Source):
    """
    Static MIDI notes, for example imported from .mid file
    """

    def __init__(self, duration=None, events=None):
        self._duration = 0
        self._events = list(events) if events is not None else []
        if duration:
            self._duration = duration
        elif events:
            self._duration = max([ev[0] for ev in self._events])

    def type(self) -> MotifType:
        return MotifType.MIDI

    def count(self) -> int:
        return len(self._events)

    def pos(self, i: int):
        return self._events[i][0]

    def data(self, i: int):
        return self._events[i][1:]

    def duration(self) -> float:
        return self._duration


class MidiEdit(MidiSource):
    """
    User-edited MIDI notes
    """

    def __init__(self, duration: float, events=None):
        super().__init__(duration)
        if events:
            self._build_notes_from_events(events)
        else:
            self._notes: List = []

    def add_note(self, pos, channel, note, velocity, duration):
        self._notes.append((pos, channel, note, velocity, duration))
        self._update_events()

    def _build_notes_from_events(self, events):
        # FIXME track on and off per channel/note pair to build notes
        pass

    def _update_events(self):
        self._events = []
        for pos, channel, note, velocity, duration in self._notes:
            self._events.append((pos, 0x90 | channel, note, velocity))
            self._events.append((pos + duration, 0x80 | channel, note, velocity))
        self._events.sort(key=lambda ev: ev[0])


class MidiModifier(Modifier):
    """
    Modifier particular to MIDI data
    """

    def __init__(self, motif: Motif):
        if motif.type() != MotifType.MIDI:
            raise RuntimeError("Midi modifiers expect MIDI motif")
        super().__init__(motif)


class MidiChannelFilter(MidiModifier):
    """
    Filter out particular channels from input MIDI

    Primary use case to extract a motif from a larger MIDI import
    """

    # FIXME impl
    pass


class MidiNoteSubstitute(MidiModifier):
    """
    Dynamically swap out MIDI notes

    Primary use case for dynamic performance, for example given an
    arpeggio in a particular key, move between preset mappings to
    change the key or position of notes whilst during playback.
    """

    # FIXME impl
    pass


def name_to_index(name: str):
    name_len = len(name)
    assert name_len >= 2 and name_len <= 3

    # Construct stable name casing for NOTE_TO_INDEX
    note = name[0].upper()
    index = midi_const.NOTE_TO_INDEX[note]
    octave = int(name[-1]) - midi_const.NOTE_MIDI_CENTRE_OCTAVE

    if len(name) == 3:
        if name[1] == "#":
            index += 1
        elif name[1].lower() == "b":
            index -= 1
        else:
            raise RuntimeError("Expecting sharp # or flat b symbol")

    midi_index = midi_const.NOTE_MIDI_CENTRE + (12 * octave) + index
    assert midi_index >= midi_const.NOTE_MIDI_START
    assert midi_index <= midi_const.NOTE_MIDI_END

    return midi_index


def note_on(channel: int, note: int, velocity: int):
    return (midi_const.MIDI_NOTE_ON | channel, note, velocity)


def note_off(channel: int, note: int, velocity: int):
    return (midi_const.MIDI_NOTE_OFF | channel, note, velocity)


def load_mid_motif(filename: str) -> MidiSource:
    """
    Import a .mid file int a MIDI source

    Very basic import at present, mostly for debugging.
    """
    import mido # import-untyped: ignore

    pos = 0
    time_sig_scale = 1
    tempo_scale = 2
    events = []

    for msg in mido.MidiFile(filename):
        pos += msg.time * time_sig_scale * tempo_scale / 4
        if msg.type == "set_tempo":
            tempo_scale = 1000000 / msg.tempo
        elif msg.type == "time_signature":
            time_sig_scale = msg.numerator / msg.denominator
        elif msg.type == "note_on":
            events.append((pos, *note_on(msg.channel, msg.note, msg.velocity)))
        elif msg.type == "note_off":
            events.append((pos, *note_off(msg.channel, msg.note, msg.velocity)))

    return MidiSource(pos, events)
